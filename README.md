# fiona

Command-line program that receives an input directory and an output directory.
It recursively reads file properties from the input directory and writes one
metadata file per input file in the output directory, preserving the same
directory structure and file names. The output directory is initialized as a Git
repository on the first run and updated on later runs. Each run commits changed
metadata files, and `fiona-stats.txt` lists the processed files.

## Usage

```sh
uv run fiona --input <input_dir> --output <output_dir>
```

Example:

```sh
uv run fiona -i ./input -o ./output
```
