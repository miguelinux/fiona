from argparse import ArgumentParser
from pathlib import Path


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

    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
