# Function to determine matching sources
import json
from importlib import resources
from typing import Any, Dict, cast

import pandas as pd


def determine_source(row: pd.Series) -> str:
    sources = []
    # Check if all are equal
    if row["gnps_IK2D"] == row["sirius_IK2D"] == row["isdb_IK2D"]:
        return "GNPS,ISDB,SIRIUS"
    if row["gnps_IK2D"] == row["sirius_IK2D"]:
        sources.append("GNPS")
        sources.append("SIRIUS")
    if row["gnps_IK2D"] == row["isdb_IK2D"]:
        sources.append("GNPS")
        sources.append("ISDB")
    if row["sirius_IK2D"] == row["isdb_IK2D"]:
        sources.append("ISDB")
        sources.append("SIRIUS")
        # Check individual sources
    if "GNPS" not in sources and pd.notna(row["gnps_IK2D"]):
        sources.append("GNPS")
    if "SIRIUS" not in sources and pd.notna(row["sirius_IK2D"]):
        sources.append("SIRIUS")
    if "ISDB" not in sources and pd.notna(row["isdb_IK2D"]):
        sources.append("ISDB")
    return "|".join(sorted(set(sources)))


# Function to count the sources
def count_sources(source_str: str) -> int:
    if source_str:
        # Count unique source names (they are | separated)
        return len(set(source_str.split("|")))
    return 0


def table_pruner(df: pd.DataFrame, columns: list, remove: bool = False) -> pd.DataFrame:
    """
    Function to remove or keep only specified columns from a DataFrame.

    Args:
        df (pandas.DataFrame): Input DataFrame.
        columns (list): List of columns to either remove or keep.
        remove (bool): If True, removes specified columns. If False, keeps only specified columns.

    Returns:
        pandas.DataFrame: DataFrame after columns have been either removed or retained.
    """
    if remove:
        # Drop specified columns and return the DataFrame
        return df.drop(columns=columns, axis=1)
    else:
        # Keep only specified columns and return the DataFrame
        return df[columns]


def load_configuration(config_filename: str) -> Dict[str, Any]:
    """
    Function to load configuration from a JSON file.

    Args:
        config_filename (str): Filename of the configuration file to load.

    Returns:
        Dict[str, Any]: Configuration dictionary.
    """
    package = "met_annot_unifier.config"

    # New way to access resources using importlib.resources
    resource_path = resources.files(package) / config_filename
    print(f"Resource path: {resource_path}")
    with resource_path.open("r", encoding="utf-8") as config_file:
        config = json.load(config_file)

    # current_path = Path(__file__).resolve()
    # print(f"Current file path: {current_path}")
    # print(f"Current working directory: {Path.cwd()}")

    # Cast the loaded config to Dict[str, Any] to satisfy type checkers
    return cast(Dict[str, Any], config)
