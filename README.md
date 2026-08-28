# fiona

Command-line program that receives an input directory and an output directory.
It recursively reads file properties from the input directory and writes one
metadata file per input file in the output directory, preserving the same
directory structure and file names. The output directory is initialized as a Git
repository and committed with `Initial commit`.

## Usage

```sh
uv run fiona --input <input_dir> --output <output_dir>
```

Example:

```sh
uv run fiona -i ./input -o ./output
```
