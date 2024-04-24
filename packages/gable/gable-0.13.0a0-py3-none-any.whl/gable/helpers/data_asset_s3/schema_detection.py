import json
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

import boto3
import click
import pandas as pd
from gable.helpers.data_asset_s3 import (
    NativeS3Converter,
    discover_patterns_from_s3_bucket,
)
from gable.helpers.emoji import EMOJI
from loguru import logger

NUM_ROWS_TO_SAMPLE = 1000
CHUNK_SIZE = 100
NUM_FILES_TO_SAMPLE = 1000


def get_df_from_s3_files(
    s3_urls: list[str], s3_opts: Optional[dict] = None
) -> list[pd.DataFrame]:
    """
    Read data from given S3 file urls (only CSV and JSON currently supported) and return pandas DataFrames.
    Args:
        s3_urls (list[str]): List of S3 URLs.
        s3_opts (dict): S3 storage options. - only needed for tests using moto mocking
    Returns:
        list[pd.DataFrame]: List of pandas DataFrames.
    """
    result = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for url in s3_urls:
            futures.append(executor.submit(read_s3_file, url, s3_opts))
        for future in futures:
            df = future.result()
            if df is not None:
                result.append(df)
    return result


def read_s3_file(url: str, s3_opts: Optional[dict] = None) -> Optional[pd.DataFrame]:
    logger.info(f"Reading from S3 file: {url}")
    try:
        if url.endswith(".csv"):
            return get_csv_df(url, s3_opts)
        elif url.endswith(".json"):
            df = pd.concat(
                pd.read_json(
                    url,
                    lines=True,
                    chunksize=CHUNK_SIZE,
                    nrows=NUM_ROWS_TO_SAMPLE,
                    storage_options=s3_opts,
                ),
                ignore_index=True,
            )
            return flatten_json(df)
        else:
            logger.info(f"Unsupported file format: {url}")
            return None
    except Exception as e:
        # Swallowing exceptions to avoid failing processing other files
        logger.opt(exception=e).error(f"Error reading file {url}: {e}")
        return None


def get_csv_df(url: str, s3_opts: Optional[dict] = None) -> pd.DataFrame:
    """
    Read CSV file from S3 and return a pandas DataFrame. Special handling for CSV files with and without headers.
    """
    df_header = pd.concat(
        pd.read_csv(
            url,
            chunksize=CHUNK_SIZE,
            nrows=NUM_ROWS_TO_SAMPLE,
            storage_options=s3_opts,
        ),
        ignore_index=True,
    )
    df_no_header = pd.concat(
        pd.read_csv(
            url,
            header=None,
            chunksize=CHUNK_SIZE,
            nrows=NUM_ROWS_TO_SAMPLE,
            storage_options=s3_opts,
        ),
        ignore_index=True,
    )
    return (
        df_header
        if tuple(df_no_header.dtypes) != tuple(df_header.dtypes)
        else df_no_header
    )


def flatten_json(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flattens any nested JSON data to a single column
    {"customerDetails": {"technicalContact": {"email": "...."}}}" => customerDetails.technicalContact.email
    """
    json_struct = json.loads(df.to_json(orient="records"))  # type: ignore
    return pd.json_normalize(json_struct)


def get_s3_client():
    return boto3.client("s3")


def append_s3_url_prefix(bucket: str, url: str) -> str:
    return "s3://" + bucket + "/" + url if not url.startswith("s3://") else url


def detect_s3_data_assets(
    bucket: str,
    include: Optional[list[str]] = None,
    dry_run: bool = False,
):
    schemas: dict[str, dict] = {}
    client = get_s3_client()
    patterns_to_urls = discover_patterns_from_s3_bucket(client, bucket, include=include)
    for pattern, urls in patterns_to_urls.items():
        s3_urls = [append_s3_url_prefix(bucket, url) for url in urls]
        dfs = get_df_from_s3_files(s3_urls)
        if len(dfs) > 0:
            schemas[pattern] = merge_schemas(
                [NativeS3Converter().to_recap(df, pattern) for df in dfs]
            )

    if len(schemas) == 0:
        raise click.ClickException(
            f"{EMOJI.RED_X.value} No data assets found to register! You can use the --debug or --trace flags for more details.",
        )

    logger.info(f"{EMOJI.GREEN_CHECK.value} {len(schemas)} S3 data asset(s) found:")
    for pattern, schema in schemas.items():
        logger.info(f"Pattern: {pattern}\nSchema: {json.dumps(schema, indent=4)}")

    if dry_run:
        logger.info("Dry run mode. Data asset registration not performed.")
    else:
        logger.info(
            "Only dry run mode available for S3 data assets.  Data asset registration not performed."
        )


def merge_schemas(schemas: list[dict]) -> dict:
    """
    Merge multiple schemas into a single schema.
    Args:
        schemas (list[dict]): List of schemas.
    Returns:
        dict: Merged schema.
    """
    # Dictionary of final fields, will be turned into a struct type at the end
    result_dict: dict[str, dict] = {}
    for schema in schemas:
        for field in schema["fields"]:
            field_name = field["name"]
            # If the field is not yet in the result, just add it
            if field_name not in result_dict:
                result_dict[field_name] = field
            elif field != result_dict[field_name]:
                # If both types are structs, recursively merge them
                if (
                    field["type"] == "struct"
                    and result_dict[field_name]["type"] == "struct"
                ):
                    result_dict[field_name] = {
                        "fields": merge_schemas([result_dict[field_name], field])[
                            "fields"
                        ],
                        "name": field_name,
                        "type": "struct",
                    }
                else:
                    # Merge the two type into a union, taking into account that one or both of them
                    # may already be unions
                    result_types = (
                        result_dict[field_name]["types"]
                        if result_dict[field_name]["type"] == "union"
                        else [result_dict[field_name]]
                    )
                    field_types = (
                        field["types"] if field["type"] == "union" else [field]
                    )
                    result_dict[field_name] = {
                        "type": "union",
                        "types": get_distinct_dictionaries(
                            remove_names(result_types) + remove_names(field_types)
                        ),
                        "name": field_name,
                    }

    return {"fields": list(result_dict.values()), "type": "struct"}


def get_distinct_dictionaries(dictionaries: list[dict]) -> list[dict]:
    """
    Get distinct dictionaries from a list of dictionaries.
    Args:
        dictionaries (list[dict]): List of dictionaries.
    Returns:
        list[dict]: List of distinct dictionaries.
    """
    # Sort for testing so we have deterministic results
    return sorted(
        [dict(t) for t in {tuple(d.items()) for d in dictionaries}],
        key=lambda x: x["type"],
    )


def remove_names(list: list[dict]) -> list[dict]:
    """
    Remove names from a list of dictionaries.
    Args:
        list (dict): List of dictionaries.
    Returns:
        dict: List of dictionaries without names.
    """
    for t in list:
        if "name" in t:
            del t["name"]
    return list
