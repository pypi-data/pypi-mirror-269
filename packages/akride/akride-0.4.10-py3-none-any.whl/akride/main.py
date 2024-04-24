import argparse

from akride.client import AkriDEClient


def main():
    # Create argument parser
    parser = argparse.ArgumentParser(description="Akride ingestion utility.")
    sub_parser = parser.add_subparsers(
        help="sub command", dest="command", required=True
    )
    ingest_parser = sub_parser.add_parser("ingest", help="ingest data")

    ingest_parser.add_argument(
        "-d", "--dataset_name", required=True, type=str, help="Dataset Name"
    )

    ingest_parser.add_argument(
        "-f",
        "--featurizer_type",
        default="patch",
        type=str,
        help="Featurizer type",
    )

    ingest_parser.add_argument(
        "-c", "--with_clip", default="yes", type=str, help="CLIP needed"
    )

    ingest_parser.add_argument(
        "-i",
        "--input_dir",
        required=True,
        type=str,
        help="Input directory path",
    )

    ingest_parser.add_argument(
        "-e", "--endpoint", required=True, type=str, help="Saas endpoint"
    )
    ingest_parser.add_argument(
        "-a", "--api_key", required=True, type=str, help="Api key"
    )

    # Parse arguments
    args = parser.parse_args()
    dataset_name = args.dataset_name
    featurizer_type = args.featurizer_type
    with_clip = args.with_clip
    input_dir = args.input_dir
    endpoint = args.endpoint
    api_key = args.api_key

    # Initialize client
    de_client = AkriDEClient(saas_endpoint=endpoint, api_key=api_key)

    # Fetch dataset by name
    dataset = de_client.get_dataset_by_name(dataset_name)

    # Start ingestion
    de_client.ingest_dataset(
        dataset=dataset,
        data_directory=input_dir,
        use_patch_featurizer=featurizer_type == "patch",
        with_clip_featurizer=with_clip == "yes",
    )


if __name__ == "__main__":
    main()
