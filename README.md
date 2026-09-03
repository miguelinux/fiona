# fiona

Command-line program that receives an input directory and an output directory.
It recursively reads file properties from the input directory and writes one
metadata file per input file in the output directory, preserving the same
directory structure and file names. The output directory is initialized as a Git
repository on the first run and updated on later runs. The first commit is always
`Initial commit`. Later runs commit changed metadata files using the commit
message passed with `--message`, or `Update file properties` by default.
`fiona-stats.txt` lists the processed files.

## Usage

```sh
uv run fiona --input <input_dir> --output <output_dir> --message <commit_message>
```

Example:

```sh
uv run fiona -i ./input -o ./output -m "Update file properties"
```

Show the package version:

```sh
uv run fiona --version
```

Short form:

```sh
uv run fiona -v
```
