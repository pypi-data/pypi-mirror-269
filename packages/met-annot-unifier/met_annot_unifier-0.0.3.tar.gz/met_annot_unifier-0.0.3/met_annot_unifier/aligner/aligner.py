from functools import reduce
from typing import Optional

import pandas as pd

from met_annot_unifier.aligner.parser import (
    extract_feature_id,
    prefix_columns,
    process_gnps_data,
    process_isdb_data,
    process_sirius_data,
    standardize_column_names,
)
from met_annot_unifier.aligner.utils import count_sources, determine_source
from met_annot_unifier.exceptions import DataFileError


def align_data_vertically(
    gnps_file: Optional[str] = None, sirius_file: Optional[str] = None, isdb_file: Optional[str] = None
) -> pd.DataFrame:
    """
    Aligns and merges data from GNPS, Sirius, and ISDB datasets optionally. Files can be provided for any subset of these datasets.
    The function standardizes column names, prefixes them to indicate their source, merges the data based on 'feature_id'
    and 'IK2D', and then creates consolidated 'Sources' and 'SMILES' columns.

    Args:
        gnps_file (str, optional): File path for the GNPS data in TSV format.
        sirius_file (str, optional): File path for the Sirius data in TSV format.
        isdb_file (str, optional): File path for the ISDB data in TSV format.

    Returns:
        pd.DataFrame: A DataFrame with aligned and merged data from the provided sources.

    Example:
        >>> gnps_file = 'path/to/gnps_data.tsv'
        >>> sirius_file = 'path/to/sirius_data.tsv'
        >>> aligned_data = align_data_vertically(gnps_file=gnps_file, sirius_file=sirius_file)
        >>> print(aligned_data.columns)
        Index(['feature_id', 'IK2D', 'Sources', 'SMILES', ...], dtype='object')
    """

    data_frames = []

    if gnps_file:
        gnps_data = process_gnps_data(gnps_file)
        data_frames.append(gnps_data)

    if sirius_file:
        sirius_data = process_sirius_data(sirius_file)
        data_frames.append(sirius_data)

    if isdb_file:
        isdb_data = process_isdb_data(isdb_file)
        data_frames.append(isdb_data)

    # Ensure that at least one data frame has been loaded
    if not data_frames:
        raise DataFileError()

    # Concatenate all available data frames
    combined_data = pd.concat(data_frames, axis=0, ignore_index=True)
    # Group by 'feature_id' and 'IK2D' and combine the annotations
    merged_data = combined_data.groupby(["feature_id", "IK2D"], as_index=False).agg(
        lambda x: ", ".join(x.dropna().astype(str).unique())
    )

    # Create the 'Sources' column
    source_columns = [col for col in merged_data.columns if col.endswith("annotation_source")]
    merged_data["Sources"] = merged_data.apply(
        lambda row: "|".join(sorted(filter(None, [row.get(col) for col in source_columns]))), axis=1
    )
    merged_data.drop(columns=source_columns, inplace=True)

    # Handle the SMILES column
    smiles_columns = [col for col in merged_data.columns if "SMILES" in col]
    merged_data["SMILES"] = merged_data.apply(
        lambda row: next((row[col] for col in smiles_columns if row[col]), None), axis=1
    )

    # Select and reorder columns
    selected_columns = ["feature_id", "IK2D", "Sources", "SMILES"]
    merged_data = merged_data[selected_columns + [col for col in merged_data.columns if col not in selected_columns]]

    return merged_data


def align_data_horizontally(
    gnps_file: Optional[str] = None, sirius_file: Optional[str] = None, isdb_file: Optional[str] = None
) -> pd.DataFrame:
    """
    Aligns and merges data from GNPS, Sirius, and ISDB datasets, if provided. This function merges the data horizontally,
    keeping the data in a wide format. The function standardizes column names, prefixes them to indicate their source,
    and merges the data based on 'feature_id'.

    Args:
    gnps_file (Optional[str]): File path for the GNPS data in TSV format.
    sirius_file (Optional[str]): File path for the Sirius data in TSV format.
    isdb_file (Optional[str]): File path for the ISDB data in TSV format.

    Returns:
    pd.DataFrame: A DataFrame with aligned and merged data from the provided sources.
    """

    data_frames = []

    if gnps_file:
        gnps_data = pd.read_csv(gnps_file, sep="\t")
        gnps_data = standardize_column_names(gnps_data, "InChIKey-Planar", "IK2D")
        gnps_data = standardize_column_names(gnps_data, "#Scan#", "feature_id")
        gnps_data = standardize_column_names(gnps_data, "Smiles", "SMILES")
        gnps_data = prefix_columns(gnps_data, "gnps_", exclude_columns=[])
        gnps_data = standardize_column_names(gnps_data, "gnps_feature_id", "feature_id")
        data_frames.append(gnps_data)

    if sirius_file:
        # Read and process Sirius data
        sirius_data = pd.read_csv(sirius_file, sep="\t")
        sirius_data = standardize_column_names(sirius_data, "InChIkey2D", "IK2D")
        sirius_data = standardize_column_names(sirius_data, "id", "feature_id")
        sirius_data = standardize_column_names(sirius_data, "smiles", "SMILES")
        sirius_data = prefix_columns(sirius_data, "sirius_", exclude_columns=[])
        sirius_data = extract_feature_id(sirius_data, "sirius_feature_id")
        sirius_data = standardize_column_names(sirius_data, "sirius_feature_id", "feature_id")
        data_frames.append(sirius_data)

    if isdb_file:
        isdb_data = pd.read_csv(isdb_file, sep="\t")
        isdb_data = standardize_column_names(isdb_data, "short_inchikey", "IK2D")
        isdb_data = standardize_column_names(isdb_data, "feature_id", "feature_id")
        isdb_data = standardize_column_names(isdb_data, "structure_smiles", "SMILES")
        isdb_data = prefix_columns(isdb_data, "isdb_", exclude_columns=[])
        isdb_data = standardize_column_names(isdb_data, "isdb_feature_id", "feature_id")
        data_frames.append(isdb_data)

    if not data_frames:
        raise DataFileError()

    # Merge the dataframes horizontally on 'feature_id'
    merged_data = reduce(lambda left, right: pd.merge(left, right, on="feature_id", how="outer"), data_frames)

    # Create the 'Sources' column. Fill it according the content of the tool_IK2D columns.
    # E.g. if sirius_IK2D is not null and matches isdb_IK2D, then the source is 'SIRIUS, ISDB'

    merged_data["source"] = merged_data.apply(determine_source, axis=1)

    merged_data["source_number"] = merged_data["source"].apply(count_sources)

    # Select columns

    selected_columns = ["feature_id", "source", "source_number"]

    # Place the selected columns at the front of the dataframe

    merged_data = merged_data[
        selected_columns + [column for column in merged_data.columns if column not in selected_columns]
    ]

    return merged_data
