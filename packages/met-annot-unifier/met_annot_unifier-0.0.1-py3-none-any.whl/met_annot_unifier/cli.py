from typing import Optional

import click

from met_annot_unifier.aligner.aligner import align_data_horizontally, align_data_vertically


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
        aligned_data.to_csv(output, index=False)
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
        aligned_data.to_csv(output, index=False)
        click.echo(f"Aligned data saved to {output}")
    else:
        click.echo(aligned_data)


if __name__ == "__main__":
    cli()
