"""
 Copyright (C) 2023, Akridata, Inc - All Rights Reserved.
 Unauthorized copying of this file, via any medium is strictly prohibited
"""

import json
from contextlib import suppress
from typing import Any, Dict, List, Optional, Tuple, Union

import akridata_akrimanager_v2 as am
import akridata_dsp as dsp
import pandas as pd
import urllib3
from akridata_akrimanager_v2.models.condition import Condition
from PIL import Image
from yarl import URL

from akride._utils.background_task_helper import BackgroundTask
from akride._utils.proxy_utils import get_env_proxy_for_url
from akride._utils.retry_helper import get_http_retry
from akride.background_task_manager import BackgroundTaskManager
from akride.core import constants
from akride.core._entity_managers.catalog_manager import CatalogManager
from akride.core._entity_managers.dataset_manager import DatasetManager
from akride.core._entity_managers.job_manager import JobManager
from akride.core._entity_managers.resultset_manager import ResultsetManager
from akride.core._entity_managers.subscriptions_manager import (
    SubscriptionsManager,
)
from akride.core.entities.catalogs import Catalog
from akride.core.entities.datasets import Dataset
from akride.core.entities.entity import Entity
from akride.core.entities.jobs import Job, JobSpec
from akride.core.entities.pipeline import Pipeline
from akride.core.entities.resultsets import Resultset
from akride.core.exceptions import (
    ErrorMessages,
    InvalidAuthConfigError,
    UserError,
)
from akride.core.models.catalog_details import CatalogDetails
from akride.core.models.progress_info import ProgressInfo
from akride.core.types import (
    AnalyzeJobParams,
    CatalogTable,
    ClientManager,
    ClusterRetrievalSpec,
    Column,
    ConfusionMatrixCellSpec,
    CoresetSamplingSpec,
    JobStatistics,
    JoinCondition,
    SampleInfoList,
    SimilaritySearchSpec,
)

from akride.core.enums import (  # isort:skip
    ClusterAlgoType,
    EmbedAlgoType,
    JobContext,
    JobStatisticsContext,
    JobType,
    FeaturizerType,
    CatalogTableType,
)


class AkriDEClient:  # pylint:disable=R0902
    """Client class to connect to DataExplorer"""

    def __init__(
        self,
        saas_endpoint: Optional[str] = None,
        api_key: Optional[str] = None,
        sdk_config_tuple: Optional[Tuple[str, str]] = None,
        sdk_config_dict: Optional[dict] = None,
        sdk_config_file: Optional[str] = None,
    ):
        """
        Initializes the AkriDEClient with the saas_endpoint and api_key values
        The init params could be passed in different ways, incase multiple
        options are used to pass the init params the order of preference
        would be
        1. Positional params (saas_endpoint, api_key)
        2. sdk_config_tuple
        3. sdk_config
        4. sdk_config_file

        Get the sdk config by signing in to Data Explorer UI and navigating to
        Utilities → Get CLI/SDK config.

        For detailed information on how to download the SDK config refer
        https://docs.akridata.ai/docs/download-config-saas

        Parameters

        Parameters
        ----------
        saas_endpoint: str
            Dataexplorer endpoint, if None defaults to https://app.akridata.ai
        api_key: str
            api_key value obtained from Dataexplorer
        sdk_config_tuple: tuple
            A tuple consisting of saas_endpoint and api_key in that order
        sdk_config_dict: dict
            dictionary containing "saas_endpoint" and "api_key"
        sdk_config_file: str
            Path to the the SDK config file downloaded from Dataexplorer

        Raises
        ---------
            InvalidAuthConfigError: if api-key/host is invalid
            ServerNotReachableError: if the server is unreachable
        """
        try:
            app_endpoint, access_key = self._get_auth_config(
                saas_endpoint=saas_endpoint,
                api_key=api_key,
                sdk_config_tuple=sdk_config_tuple,
                sdk_config_dict=sdk_config_dict,
                sdk_config_file=sdk_config_file,
            )
        except Exception as ex:
            raise InvalidAuthConfigError(
                message=ErrorMessages.SDK_USER_ERR_01_INVALID_AUTH
            ) from ex
        if app_endpoint is None or access_key is None:
            raise InvalidAuthConfigError(
                message=ErrorMessages.SDK_USER_ERR_01_INVALID_AUTH
            )
        proxy, proxy_headers = self._get_proxy_url_and_headers(app_endpoint)
        app_endpoint: str = app_endpoint.split(sep="//")[1]
        self.host = app_endpoint
        self.api_key = access_key

        dsp_conf = dsp.Configuration(
            host=f"https://{app_endpoint}/ds-core",
        )
        dsp_conf.proxy = proxy  # type: ignore
        dsp_conf.proxy_headers = proxy_headers  # type: ignore
        default_retries = get_http_retry()
        dsp_conf.retries = default_retries  # type:ignore
        dsp_client = dsp.ApiClient(
            configuration=dsp_conf,
            header_name="X-API-KEY",
            header_value=access_key,
        )

        am_conf = am.Configuration(
            host=f"https://{app_endpoint}/api",
        )
        am_conf.proxy = proxy  # type: ignore
        am_conf.proxy_headers = proxy_headers  # type: ignore
        am_conf.retries = default_retries  # type:ignore
        am_client = am.ApiClient(
            configuration=am_conf,
            header_name="X-API-KEY",
            header_value=access_key,
        )

        task_manager = BackgroundTaskManager()

        cli_manager = ClientManager(
            am_client=am_client,
            dsp_client=dsp_client,
            background_task_manager=task_manager,
        )
        self.jobs = JobManager(cli_manager)
        self.resultsets = ResultsetManager(cli_manager)
        self.catalogs = CatalogManager(cli_manager)
        self.datasets = DatasetManager(cli_manager=cli_manager)
        self.subscriptions = SubscriptionsManager(cli_manager=cli_manager)

        # Check if the api-key is valid
        self.subscriptions.get_server_version()
        print("AkriDEClient initialized")

    def _get_auth_config(
        self,
        saas_endpoint,
        api_key,
        sdk_config_tuple,
        sdk_config_dict,
        sdk_config_file,
    ):
        saas_ep, auth_key = None, None
        if api_key:
            if saas_endpoint is None:
                saas_ep = constants.Constants.DEFAULT_SAAS_ENDPOINT
            else:
                saas_ep = saas_endpoint
            auth_key = api_key
        elif sdk_config_tuple:
            saas_ep, auth_key = sdk_config_tuple
        elif sdk_config_dict:
            saas_ep, auth_key = (
                sdk_config_dict["saas_endpoint"],
                sdk_config_dict["api_key"],
            )
        elif sdk_config_file:
            with open(sdk_config_file, "r", encoding="utf-8") as api_conf:
                auth_config = json.load(api_conf)
                saas_ep, auth_key = (
                    auth_config["saas_endpoint"],
                    auth_config["api_key"],
                )
        else:
            raise TypeError(
                "AkriDEClient Initialization requires one of the following "
                " options: 'sdk_config_tuple','sdk_config_dict' "
                "or 'sdk_config_file'  "
            )

        return saas_ep, auth_key

    def _get_proxy_url_and_headers(
        self, host
    ) -> Tuple[Optional[str], Optional[Dict[str, str]]]:
        try:
            with suppress(LookupError):
                url = URL(host)
                proxy_url, proxy_basic_auth = get_env_proxy_for_url(url)
                if proxy_basic_auth:
                    return proxy_url.human_repr(), urllib3.make_headers(
                        proxy_basic_auth=proxy_basic_auth
                    )
                return proxy_url.human_repr(), None
            return None, None
        except Exception as e:
            raise e

    def get_server_version(self) -> str:
        """Get Dataexplorer server version

        Returns:
            str: server version
        """
        return self.subscriptions.get_server_version()

    #
    # Dataset API
    #

    def get_datasets(self, attributes: Dict[str, Any] = {}) -> List[Entity]:
        """
        Retrieves information about datasets that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any], optional
            The filter specification. It may have the following
            optional fields:
                search_key : str
                    Filter across fields like dataset id, and dataset name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing datasets.
        """
        return self.datasets.get_entities(attributes)  # type: ignore

    def get_dataset_by_name(self, name: str) -> Optional[Entity]:
        """
        Retrieves a dataset with the given name.

        Parameters
        ----------
        name : str
            The name of the dataset to retrieve.

        Returns
        -------
        Entity
            The Entity object
            representing the dataset.
        """
        return self.datasets.get_entity_by_name(name)

    def create_dataset(self, spec: Dict[str, Any]) -> Entity:
        """
        Creates a new dataset entity.

        Parameters
        ----------
        spec : Dict[str, Any]
            The dataset spec. The spec should have the following fields:
                dataset_name : str
                    The name of the new dataset.
                dataset_namespace : str, optional
                    The namespace for the dataset, by default 'default'.
                data_type : DataType, optional
                    The type of data to store in the dataset, by default
                    DataType.IMAGE.
                glob_pattern : str, optional
                    The glob pattern for the dataset, by default
                    '*(png|jpg|gif|jpeg|tiff|tif|bmp)'.
                overwrite : bool, optional
                    Overwrite if a dataset with the same name exists.

        Returns
        -------
        Entity
            The created entity
        """
        return self.datasets.create_entity(spec)

    def delete_dataset(self, dataset: Dataset) -> bool:
        """
        Deletes a dataset object.

        Parameters
        ----------
        dataset : Dataset
            The dataset object to delete.

        Returns
        -------
        bool
            Indicates whether this entity was successfully deleted
        """
        return self.datasets.delete_entity(dataset)

    def ingest_dataset(
        self,
        dataset: Dataset,
        data_directory: str,
        use_patch_featurizer: bool = True,
        with_clip_featurizer: bool = False,
        async_req: bool = False,
        catalog_details: Optional[CatalogDetails] = None,
    ) -> Optional[BackgroundTask]:
        """
        Starts an asynchronous ingest task for the specified dataset.

        Parameters
        ----------
        dataset : Dataset
            The dataset to ingest.
        data_directory : str
            The path to the directory containing the dataset files.
        use_patch_featurizer: bool, optional
            Ingest dataset to enable patch-based similarity searches.
        with_clip_featurizer: bool, optional
            Ingest dataset to enable text prompt based search.
        async_req: bool, optional
            Whether to execute the request asynchronously.
        catalog_details: Optional[CatalogDetails]
            Parameters details for creating a catalog

        Returns
        -------
        BackgroundTask
            A task object
        """
        featurizer_type = (
            FeaturizerType.PATCH
            if use_patch_featurizer
            else FeaturizerType.FULL_IMAGE
        )

        return self.datasets.ingest_dataset(
            dataset=dataset,
            data_directory=data_directory,
            featurizer_type=featurizer_type,
            catalog_details=catalog_details,
            with_clip_featurizer=with_clip_featurizer,
            async_req=async_req,
        )

    def import_catalog(
        self,
        dataset: Dataset,
        table_name: str,
        csv_file_path: str,
        create_view: bool = True,
        file_name_column: Optional[str] = None,
        pipeline_name: Optional[str] = None,
    ) -> bool:
        """
        Method for importing an external catalog into a dataset.

        Parameters
        ----------
        dataset : Dataset
            The dataset to import the catalog into.
        table_name : str
            The name of the table to create for the catalog.
        csv_file_path : str
            The path to the CSV file containing the catalog data.
        create_view: bool default: True
            Create a view with imported catalog and primary catalog table
        file_name_column: str
            Name of the column in the csv file that
            contains the absolute filename
        pipeline_name: str
            Name of pipeline whose primary table will be joined with the
            imported table. Ignored if create_view is false
        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        if create_view and not file_name_column:
            raise ValueError(
                "View creation requires `file_name_column` to be specified"
            )

        success = self.catalogs.import_catalog(
            dataset, table_name, csv_file_path
        )
        if success and create_view:
            # find the attached image pipeline to figure out which primary
            # table is to be used to to create a view
            pipelines: List[Pipeline] = self.get_attached_pipelines(
                dataset=dataset
            )
            image_pipeline = None
            if pipeline_name is None:
                image_pipeline: Optional[
                    Pipeline
                ] = self.datasets._get_default_image_pipeline(
                    attached_pipelines=pipelines
                )
            else:
                for pipeline in pipelines:
                    pipeline: Pipeline
                    if pipeline.get_name() == pipeline_name:
                        image_pipeline = pipeline
                        break
            if not image_pipeline:
                raise UserError(
                    message=f"No pipeline {pipeline_name} attached,"
                    " If view creation is not "
                    " needed, disable it by setting `create_view` to False"
                )
            left_table = CatalogTable(
                table_name="primary",
                table_type=CatalogTableType.INTERNAL,
                pipeline_id=image_pipeline.get_id(),
            )
            right_table = CatalogTable(
                table_name=table_name, table_type=CatalogTableType.INTERNAL
            )
            join_condition = JoinCondition(
                left_column="file_name", right_column=file_name_column
            )
            _ = self.create_view(
                view_name=f"{table_name}_primary_view",
                description="Auto created view joining {table_name} "
                "with {pipeline_name} primary table",
                dataset=dataset,
                left_table=left_table,
                right_table=right_table,
                join_condition=join_condition,
            )
        return True

    def add_to_catalog(
        self, dataset: Dataset, table_name: str, csv_file_path: str
    ) -> bool:
        """
        Adds new items to an existing catalog.

        Parameters
        ----------
        dataset : Dataset
            The dataset to import the catalog into.
        table_name : str
            The name of the table to create for the catalog.
        csv_file_path : str
            The path to the CSV file containing new catalog data.

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        return self.catalogs.add_to_catalog(
            dataset,
            table_name,
            csv_file_path,
        )

    def delete_catalog(self, catalog: Catalog) -> bool:
        """
        Deletes a catalog object.

        Parameters
        ----------
        catalog : Catalog
            The catalog object to delete.

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        return self.catalogs.delete_entity(catalog)

    def get_catalogs(self, attributes: Dict[str, Any] = {}) -> List[Entity]:
        """
        Retrieves information about catalogs that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any]
            The filter specification. It may have the following optional
            fields:
                name : str
                    filter by catalog name
                status : str
                    filter by catalog status, can be one of
                    "active","inactive", "refreshing", "offline",
                    "invalid-config"

        Returns
        -------
        List[Entity]
            A list of Entity objects representing catalogs.
        """
        return self.catalogs.get_entities(attributes)

    def get_catalog_by_name(
        self, dataset: Dataset, name: str
    ) -> Optional[Entity]:
        """
        Retrieves a catalog with the given name.

        Parameters
        ----------
        dataset : Dataset
            The dataset to retrieve the catalog from.
        name : str
            The name of the catalog to retrieve.

        Returns
        -------
        Entity
            The Entity object representing the catalog.
        """
        return self.catalogs.get_catalog_by_name(dataset, name)

    def get_resultsets(self, attributes: Dict[str, Any] = {}) -> List[Entity]:
        """
        Retrieves information about resultsets that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any], optional
            The filter specification. It may have the following
            optional fields:
                search_key : str
                    Filter across fields like dataset id, and dataset name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing resultsets.
        """
        return self.resultsets.get_entities(attributes)  # type: ignore

    def get_resultset_by_name(self, name: str) -> Optional[Entity]:
        """
        Retrieves a resultset with the given name.

        Parameters
        ----------
        name : str
            The name of the resultset to retrieve.

        Returns
        -------
        Entity
            The Entity object representing the resultset.
        """
        return self.resultsets.get_entity_by_name(name)

    def get_resultset_samples(self, resultset: Resultset) -> SampleInfoList:
        """
        Retrieves the samples of a resultset

        Parameters
        ----------
        resultset : Resultset
            The Resultset object to get samples for.

        Returns
        -------
        SampleInfoList
            A SampleInfoList object.
        """
        return self.resultsets.get_samples(resultset)

    def create_resultset(self, spec: Dict[str, Any]) -> Entity:
        """
        Creates a new resultset entity.

        Parameters
        ----------
        spec : Dict[str, Any]
            The resultset spec. The spec should have the following fields:
                job: Job
                    The associated job object.
                name : str
                    The name of the new resultset.
                samples: SampleInfoList
                    The samples to be included in this resultset.

        Returns
        -------
        Entity
            The created entity
        """
        return self.resultsets.create_entity(spec)  # type: ignore

    def update_resultset(
        self,
        resultset: Resultset,
        add_list: Optional[SampleInfoList] = None,
        del_list: Optional[SampleInfoList] = None,
    ) -> bool:
        """
        Updates a resultset.

        Parameters
        ----------
        resultset: Resultset
            The resultset to be updated.
        add_list: SampleInfoList, optional
            The list of samples to be added.
        del_list: SampleInfoList, optional
            The list of samples to be deleted.

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        return self.resultsets.update_resultset(resultset, add_list, del_list)

    def delete_resultset(self, resultset: Resultset) -> bool:
        """
        Deletes a resultset object.

        Parameters
        ----------
        resultset : Resultset
            The resultset object to delete.

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        return self.resultsets.delete_entity(resultset)  # type: ignore

    #
    # Job API
    #

    def create_job_spec(
        self,
        dataset: Dataset,
        job_type: Union[str, JobType] = JobType.EXPLORE,
        job_name: str = "",
        predictions_file: str = "",
        cluster_algo: Union[str, ClusterAlgoType] = ClusterAlgoType.HDBSCAN,
        embed_algo: Union[str, EmbedAlgoType] = EmbedAlgoType.UMAP,
        num_clusters: Optional[int] = None,
        max_images: int = 1000,
        catalog_table: Optional[CatalogTable] = None,
        analyze_params: Optional[AnalyzeJobParams] = None,
        pipeline: Optional[Pipeline] = None,
        filters: List[Condition] = None,  # type: ignore
    ) -> JobSpec:
        """
        Creates a JobSpec object that specifies how a job is to be created.

        Parameters:
        -----------
        dataset: Dataset
            The dataset to explore.
        job_type : JobType, optional
            The job type
        job_name : str, optional
            The name of the job to create. A unique name will be generated
            if this is not given.
        predictions_file: str, optional
            The path to the catalog file containing predictions and ground
            truth. This file must be formatted according to the specification
            at:
         https://docs.akridata.ai/docs/analyze-job-creation-and-visualization
        cluster_algo : ClusterAlgoType, optional
            The clustering algorithm to use.
        embed_algo : EmbedAlgoType, optional
            The embedding algorithm to use.
        num_clusters : int, optional
            The number of clusters to create.
        max_images : int, optional
            The maximum number of images to use.
        catalog_table: CatalogTable, optional
            The catalog to be used for creating this explore job. This defaults
            to the internal primary catalog that is created automatically when
            a dataset is created.
            default: "primary"
        analyze_params: AnalyzeJobParams, optional
            Analyze job related configuration parameters
        filters : List[Condition], optional
            The filters to be used to select a subset of samples for this job.
            These filters are applied to the catalog specified by catalog_name.
        """
        if pipeline is None:
            pipelines: List[Pipeline] = self.get_attached_pipelines(
                dataset=dataset
            )
            pipeline = self.datasets._get_default_image_pipeline(
                attached_pipelines=pipelines
            )
        if catalog_table is None:
            catalog_table = CatalogTable(table_name="primary")
        return JobSpec(
            dataset=dataset,
            job_type=job_type,
            job_name=job_name,
            predictions_file=predictions_file,
            cluster_algo=cluster_algo,
            embed_algo=embed_algo,
            num_clusters=num_clusters,
            max_images=max_images,
            catalog_table=catalog_table,
            filters=filters,
            pipeline=pipeline,
            analyze_params=analyze_params,
        )

    def create_job(self, spec: JobSpec) -> Job:
        """
        Creates an explore job for the specified dataset.

        Parameters:
        -----------
        dataset: Dataset
            The dataset to explore.
        spec: JobSpec
            The job specification.

        Returns:
        --------
        Job
            The newly created Job object.
        """
        return self.jobs.create_entity(spec)  # type: ignore

    def delete_job(self, job: Job) -> bool:
        """
        Deletes a job object.

        Parameters
        ----------
        job : Job
            The job object to delete.

        Returns
        -------
        bool
            Indicates whether the operation was successful.
        """
        raise NotImplementedError

    def get_job_by_name(self, name: str) -> Job:
        """
        Retrieves a job with the given name.

        Parameters
        ----------
        name : str
            The name of the job to retrieve.

        Returns
        -------
        Entity
            The Entity object representing the job.
        """
        return self.jobs.get_entity_by_name(name)  # type: ignore

    def get_jobs(self, attributes: Dict[str, Any] = {}) -> List[Entity]:
        """
        Retrieves information about jobs that have the given attributes.

        Parameters
        ----------
        attributes: Dict[str, Any]
            The filter specification. It may have the following
            optional fields:
                data_type : str
                    The data type to filter on. This can be 'IMAGE' or 'VIDEO'.
                job_type : str
                    The job type to filter on - 'EXPLORE', 'ANALYZE' etc.
                search_key : str
                    Filter jobs across fields like job name, dataset id, and
                    dataset name.

        Returns
        -------
        List[Entity]
            A list of Entity objects representing jobs.
        """
        return self.jobs.get_entities(attributes)  # type: ignore

    def get_thumbnail_images(
        self, samples: SampleInfoList
    ) -> List[Image.Image]:
        """
        Retrieves the thumbnail images corresponding to the samples.

        Parameters
        ----------
        samples : SampleInfoList
            The samples to retrieve thumbnails for.

        Returns
        -------
        List[Image.Image]
            A list of thumbnail images.
        """
        if samples.job_id:
            return self.jobs.get_thumbnail_images(samples)
        return self.resultsets.get_thumbnail_images(samples)

    def get_fullres_images(self, samples: SampleInfoList) -> List[Image.Image]:
        """
        Retrieves the full-resolution images for the provided job.

        Parameters
        ----------
        samples : SampleInfoList
            The samples to retrieve images for.

        Returns
        -------
        List[Image.Image]
            A list of images.
        """
        return self.jobs.get_fullres_images(samples)

    def get_fullres_image_urls(self, samples: SampleInfoList) -> Dict:
        """
        Retrieves the full-resolution image urls for the give samples.

        Parameters
        ----------
        samples : SampleInfoList
            The samples to retrieve full res image urls for.

        Returns
        -------
        Dict
            A dictionary containing the full-resolution image URLs for
            each sample.
        """
        if not samples:
            raise ValueError("'samples' cannot be None")
        if not isinstance(samples, SampleInfoList):
            raise TypeError(
                f"Invalid argument type: {type(samples)}."
                f"Expected type: SampleInfoList".format(type(samples))
            )
        return self.jobs.get_fullres_image_urls(samples)

    def get_catalog_tags(self, samples: SampleInfoList) -> pd.DataFrame:
        """
        Retrieves the catalog tags corresponding to the given samples.

        Parameters
        ----------
        samples : SampleInfoList
            The samples to retrieve catalog tags for.

        Returns
        -------
        pd.DataFrame
            A dataframe of catalog tags.
        """
        return self.catalogs.get_catalog_tags(samples)

    def get_job_statistics(
        self, job: Job, context: JobStatisticsContext, **kwargs
    ) -> JobStatistics:
        """
        Retrieves statistics info from an analyze job.

        Parameters
        ----------
        job : Job
            The Job object to get statistics for.
        context: JobStatisticsContext
            The type of statistics to retrieve.
        **kwargs: Additional keyword arguments
        Supported keyword arguments
            iou_config_threshold: float, optional
                Threshold value for iou config
            confidence_score_threshold: float, optional
                Threshold value for confidence score

        Returns
        -------
        JobStatistics
            A job statistics object.
        """
        return self.jobs.get_job_statistics(job, context, **kwargs)

    def get_job_samples(
        self,
        job: Job,
        job_context: JobContext,
        spec: Union[
            SimilaritySearchSpec,
            ConfusionMatrixCellSpec,
            ClusterRetrievalSpec,
            CoresetSamplingSpec,
        ],
        **kwargs,
    ) -> SampleInfoList:
        """
        Retrieves the samples according to the given specification.

        Parameters
        ----------
        job : Job
            The Job object to get samples for.
        job_context: JobContext
            The context in which the samples are requested for.
        spec: Union[
            SimilaritySearchSpec,
            ConfusionMatrixCellSpec,
            ClusterRetrievalSpec,
            CoresetSamplingSpec
        ]
            The job context spec.
        **kwargs: Additional keyword arguments
        Supported keyword arguments
            iou_config_threshold: float, optional
                Threshold value for iou config
            confidence_score_threshold: float, optional
                Threshold value for confidence score
        Returns
        -------
        SampleInfoList
            A SampleInfoList object.
        """
        return self.jobs.get_samples(job, job_context, spec, **kwargs)

    def get_job_samples_from_file_path(
        self,
        job: Job,
        file_info: List[str],
    ) -> Dict:
        """
        Retrieves the samples according to the given specification.

        Parameters
        ----------
        job : Job
            The Job object to get samples for.
            The job context spec.
        file_info: List[str]
            List of file_paths for the images of interest
        Returns
        -------
        Dict
            dictionary of map between file_path and point_ids
        """
        return self.jobs.get_samples_from_file_path(job, file_info)

    def get_job_display_panel(
        self,
        job: Job,
    ) -> str:
        """
        Retrieves the job panel URI the Data Explorer.

        Parameters
        ----------
        job : Job
            The Job object to be queried.
        Returns
        -------
        str
            The job panel URL.
        """

        return (
            f"https://{self.host}/"
            f"{self.jobs.get_job_display_panel_uri(job)}"
        )

    #
    # Common API
    #

    def get_progress_info(self, task: BackgroundTask) -> ProgressInfo:
        """
        Gets the progress of the specified task.

        Parameters
        ----------
        task : BackgroundTask
            The task object to retrieve the progress information for.

        Returns
        -------
        ProgressInfo
            The progress information
        """
        return task.get_progress_info()

    def wait_for_completion(self, task: BackgroundTask) -> ProgressInfo:
        """
        Waits for the specified task to complete.

        Parameters
        ----------
        task : BackgroundTask
            The ID of the job to wait for.

        Returns
        -------
        ProgressInfo
            The progress information
        """
        return task.wait_for_completion()

    def create_view(
        self,
        view_name: str,
        description: Optional[str],
        dataset: Dataset,
        left_table: CatalogTable,
        right_table: CatalogTable,
        join_condition: JoinCondition,
    ) -> str:  # -> Any | None:# -> Any | None:
        """Create a SQL view for visualization

        Args:
            view_name (str): Name of the view to create
            description (Optional[str]): Description text
            dataset (Dataset): Dataset object
            left_table (TableInfo): Left Table of the create view query
            right_table (TableInfo): Right Table of the create view query
            join_condition (JoinCondition): JoinCondition which includes the
            column from the left and the right table

        Returns:
            str: view id
        """
        return self.catalogs.create_view(
            view_name,
            description,
            dataset,
            left_table,
            right_table,
            join_condition,
        )

    def get_attached_pipelines(
        self, dataset: Dataset, version: Optional[str] = None
    ) -> List[Pipeline]:
        """Get pipelines attached for dataset given a dataset version

        Args:
            dataset (Dataset): Dataset object
            version (str, optional): Dataset version. Defaults to None in which
            case the latest version would be used

        Returns:
            List[Pipeline]: List of pipelines attached with the dataset
        """
        return self.datasets.get_attached_pipelines(dataset, version)

    def get_all_columns(
        self, dataset: Dataset, table: CatalogTable
    ) -> List[Column]:
        """Returns all columns for a table/view

        Args:
            dataset (Dataset): Dataset object
            table (TableInfo): Table Information

        Returns:
            List[Column]: List of columns of the table
        """
        return self.catalogs.get_all_columns(dataset, table)
