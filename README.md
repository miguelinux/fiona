# fiona

Command-line program that receives an input directory and an output directory.
It recursively reads file properties from the input directory and writes them to
`fileproperties.json` in the output directory.

## Usage

```sh
uv run fiona --input <input_dir> --output <output_dir>
```

Example:

```sh
uv run fiona -i ./input -o ./output
```
