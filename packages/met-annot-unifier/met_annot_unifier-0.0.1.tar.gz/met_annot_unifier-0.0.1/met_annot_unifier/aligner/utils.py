# Function to determine matching sources
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
    return ",".join(sorted(set(sources)))


# Function to count the sources
def count_sources(source_str: str) -> int:
    if source_str:
        # Count unique source names (they are comma-separated)
        return len(set(source_str.split(",")))
    return 0
