# met-annot-unifier

[![Release](https://img.shields.io/github/v/release/mapp-metabolomics-unit/met-annot-unifier)](https://img.shields.io/github/v/release/mapp-metabolomics-unit/met-annot-unifier)
[![Build status](https://img.shields.io/github/actions/workflow/status/mapp-metabolomics-unit/met-annot-unifier/main.yml?branch=main)](https://github.com/mapp-metabolomics-unit/met-annot-unifier/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/mapp-metabolomics-unit/met-annot-unifier/branch/main/graph/badge.svg)](https://codecov.io/gh/mapp-metabolomics-unit/met-annot-unifier)
[![Commit activity](https://img.shields.io/github/commit-activity/m/mapp-metabolomics-unit/met-annot-unifier)](https://img.shields.io/github/commit-activity/m/mapp-metabolomics-unit/met-annot-unifier)
[![License](https://img.shields.io/github/license/mapp-metabolomics-unit/met-annot-unifier)](https://img.shields.io/github/license/mapp-metabolomics-unit/met-annot-unifier)

A Python project to combine tabular outputs from GNPS, Sirius and ISDB

- **Github repository**: <https://github.com/mapp-metabolomics-unit/met-annot-unifier/>
- **Documentation** <https://mapp-metabolomics-unit.github.io/met-annot-unifier/>

## Quickstart

### Installation

met-annot-unifier is available on PyPi and can be installed with pip:

```bash
pip install met-annot-unifier
```

### Usage

For now the package is only available as a command line tool. You can run it with the following command:

```bash
met-annot-unifier-cli
```

Get help on the available modes with:

```bash
met-annot-unifier-cli --help
```

#### Align tables

You can align the annotations tables from GNPS, Sirius and ISDB using two modes:

- `align-horizontally`: This will return a long table with a single row for each unique compound (according to their planar structures or IK2D). This mode can be useful to output a table to be viewed in [Datawarrior](https://openmolecules.org/datawarrior/) or similar tools for chemical structures exploration.

```bash
met-annot-unifier-cli align-horizontally --gnps-file <path-to-gnps-table> --sirius-file <path-to-sirius-table> --isdb-file <path-to-isdb-table> --output <output-path>
```

- `align-vertically`: This will return a wide table with a single row per feature (m/z and retention time) and columns for each of the three sources. This mode can be useful to output a table to be added to a molecular network to be visualized in [Cytoscape](https://cytoscape.org/) or similar tools for network visualization.

```bash
met-annot-unifier-cli align-vertically --gnps-file <path-to-gnps-table> --sirius-file <path-to-sirius-table> --isdb-file <path-to-isdb-table> --output <output-path>
```

#### Pruning tables

You can prune the aligned tables to remove rows with missing values in the columns of interest. This can be useful to remove rows with missing values in the columns used to merge the tables.

```bash
met-annot-unifier-cli prune-table --input <path-to-aligned-table> --list-columns <key-in-config-file> --output <output-path>
```

The `--list-columns` argument should be a key in the `column_config.yaml` file that contains a list of columns to be used to prune the table. You can edit this file [here](https://mapp-metabolomics-unit.github.io/met-annot-unifier/config/column_config.yaml).

### Example

You can align the GNPS, ISDB and Sirius tables found in the `examples/data/in` folder of this repository and prune them to have a Cytoscape compatible table with the following commands:

```bash
met-annot-unifier-cli align-horizontally --gnps-file examples/data/in/gnps_output_example.tsv --sirius-file examples/data/in/sirius_output_example.tsv --isdb-file examples/data/in/isdb_output_example.tsv --output examples/data/out/aligned_table_horizontally.tsv
met-annot-unifier-cli prune-table --input-file examples/data/out/aligned_table_horizontally.tsv --list-columns "minimal_cytoscape" -o examples/data/out/aligned_table_horizontally_pruned_cytoscape.tsv
```

Since the input file arguments are optional, you can also choose to treat only ISDB and Sirius tables for example.

````bash
met-annot-unifier-cli align-horizontally --sirius-file examples/data/in/sirius_output_example.tsv --isdb-file examples/data/in/isdb_output_example.tsv --output examples/data/out/aligned_table_horizontally_isdb_sirius.tsv
met-annot-unifier-cli prune-table --input-file examples/data/out/aligned_table_horizontally_isdb_sirius.tsv --list-columns "minimal_cytoscape_no_gnps" -o examples/data/out/aligned_table_horizontally_pruned_isdb_sirius_cytoscape.tsv
```

---

Repository initiated with [fpgmaas/cookiecutter-poetry](https://github.com/fpgmaas/cookiecutter-poetry).
````
