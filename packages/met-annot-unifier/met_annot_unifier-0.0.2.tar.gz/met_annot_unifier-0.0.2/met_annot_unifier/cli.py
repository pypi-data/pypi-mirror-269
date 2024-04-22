from typing import Optional

import click
import pandas as pd

from met_annot_unifier.aligner.aligner import align_data_horizontally, align_data_vertically
from met_annot_unifier.aligner.utils import load_configuration, table_pruner


@click.group()
def cli() -> None:
    """Description for your CLI tool."""
    print("CLI is running")
    pass


@cli.command()
@click.option("--gnps-file", type=click.Path(exists=True), help="Path to GNPS output file.")
@click.option("--sirius-file", type=click.Path(exists=True), help="Path to Sirius output file.")
@click.option("--isdb-file", type=click.Path(exists=True), help="Path to ISDB output file.")
@click.option("--output", "-o", type=click.Path(), help="Output file to save the merged data.")
def align_vertically(gnps_file: str, sirius_file: str, isdb_file: str, output: Optional[str] = None) -> None:
    """CLI tool to align and merge data from GNPS, Sirius, and ISDB.

    Args:
        gnps_file (str): Path to GNPS output file.
        sirius_file (str): Path to Sirius output file.
        isdb_file (str): Path to ISDB output file.
        output (str, optional): Output file to save the merged data. Defaults to None.

    Returns:
        A dataframe with the aligned data (if the output option is used, the dataframe is saved to a file)
    """
    aligned_data = align_data_vertically(gnps_file, sirius_file, isdb_file)

    if output:
        aligned_data.to_csv(output, index=False, sep="\t")
        click.echo(f"Aligned data saved to {output}")
    else:
        click.echo(aligned_data)


@cli.command()
@click.option("--gnps-file", type=click.Path(exists=True), help="Path to GNPS output file.")
@click.option("--sirius-file", type=click.Path(exists=True), help="Path to Sirius output file.")
@click.option("--isdb-file", type=click.Path(exists=True), help="Path to ISDB output file.")
@click.option("--output", "-o", type=click.Path(), help="Output file to save the merged data.")
def align_horizontally(gnps_file: str, sirius_file: str, isdb_file: str, output: Optional[str] = None) -> None:
    """CLI tool to align and merge data from GNPS, Sirius, and ISDB horizontally.

    Args:
        gnps_file (str): Path to GNPS output file.
        sirius_file (str): Path to Sirius output file.
        isdb_file (str): Path to ISDB output file.
        output (str, optional): Output file to save the merged data. Defaults to None.

    Returns:
        A dataframe with the aligned data (if the output option is used, the dataframe is saved to a file)
    """
    aligned_data = align_data_horizontally(gnps_file, sirius_file, isdb_file)

    if output:
        aligned_data.to_csv(output, index=False, sep="\t")
        click.echo(f"Aligned data saved to {output}")
    else:
        click.echo(aligned_data)


# Here we call utils.table_pruner which take a df and a list of columns to remove.
# Predefined lists of columns are proposed to the user and should be available in the CLI options.
@cli.command()
@click.option("--input-file", type=click.Path(exists=True), help="Path to the input file.")
@click.option("--remove", is_flag=True, help="Removes the specified columns instead of keeping them.")
@click.option(
    "--list-columns",
    type=click.Choice(["gnps", "sirius", "isdb", "test", "minimal_datawarrior", "minimal_cytoscape"]),
    multiple=True,
    help="List of columns to remove, can select multiple separated by spaces.",
)
@click.option("--output", "-o", type=click.Path(), help="Output file to save the pruned data.")
def prune_table(input_file: str, list_columns: str, remove: bool, output: Optional[str] = None) -> None:
    """CLI tool to remove columns from a DataFrame.

    Args:
        input_file (str): Path to the input file.
        list_columns (str): List of columns to remove.
        remove (bool): If True, removes only the specified columns; otherwise, keeps them.
        output (str, optional): Output file to save the pruned data. Defaults to None.

    Returns:
        A dataframe with the pruned data (if the output option is used, the dataframe is saved to a file)
    """
    # Define the columns to remove
    columns_to_remove = load_configuration("column_config.json")
    # Load the input file
    df = pd.read_csv(input_file, sep="\t")

    # Aggregate all columns to remove from selected lists
    all_columns_to_remove = []
    for list_name in list_columns:  # list_columns is a tuple of selections
        all_columns_to_remove.extend(columns_to_remove[list_name])

    # # Remove duplicates in the list
    # all_columns_to_remove = list(set(all_columns_to_remove))

    # Prune the table
    pruned_data = table_pruner(df, all_columns_to_remove, remove=remove)

    if output:
        pruned_data.to_csv(output, index=False, sep="\t")
        click.echo(f"Pruned data saved to {output}")
    else:
        click.echo(pruned_data)


if __name__ == "__main__":
    cli()
