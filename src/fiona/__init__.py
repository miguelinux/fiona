import json
from argparse import ArgumentParser
from pathlib import Path

from fiona.fileproperties import FileProperties
from fiona.gitsystem import GitSystem


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
    for file in files:
        output_file = output_dir / file.path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(
            json.dumps(file.to_dict(), indent=2),
            encoding="utf-8",
        )

    stats_file = output_dir / "fiona-stats.txt"
    stats_file.write_text(
        "Files processed: "
        f"{len(files)}\n"
        "\n"
        "Processed files:\n" + "".join(f"{file.path}\n" for file in files),
        encoding="utf-8",
    )

    try:
        GitSystem(output_dir).create_repository()
    except RuntimeError as error:
        parser.exit(1, f"error: {error}\n")

    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Files processed: {len(files)}")
