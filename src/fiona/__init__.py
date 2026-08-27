import json
from argparse import ArgumentParser
from pathlib import Path

from fiona.fileproperties import FileProperties


def main() -> None:
    parser = ArgumentParser(
        prog="fiona",
        description="Receive an input directory and an output directory.",
    )
    parser.add_argument(
        "-i",
        "--input",
        dest="input_dir",
        required=True,
        type=Path,
        help="Directory to read from",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_dir",
        required=True,
        type=Path,
        help="Directory to write to",
    )
    args = parser.parse_args()

    input_dir = args.input_dir.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    if not input_dir.is_dir():
        parser.error(f"input_dir must be an existing directory: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    files = FileProperties.collect_from_tree(input_dir)
    output_file = output_dir / "fileproperties.json"
    output_file.write_text(
        json.dumps([file.to_dict() for file in files], indent=2),
        encoding="utf-8",
    )

    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Files processed: {len(files)}")
    print(f"Properties file: {output_file}")
