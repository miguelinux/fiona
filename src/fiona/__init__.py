# SPDX-FileCopyrightText: 2026, Qualcomm Technologies, Inc.
#
# SPDX-License-Identifier: BSD-3-Clause

import json
from argparse import ArgumentParser
from pathlib import Path
from time import perf_counter

from fiona.fileproperties import FileProperties
from fiona.gitsystem import GitSystem

STATS_FILE_NAME = "fiona-stats.txt"


def remove_stale_files(output_dir: Path, expected_files: set[Path]) -> None:
    for path in output_dir.rglob("*"):
        relative_path = path.relative_to(output_dir)
        if ".git" in relative_path.parts:
            continue
        if path.is_file() and relative_path not in expected_files:
            path.unlink()

    for path in sorted(output_dir.rglob("*"), reverse=True):
        relative_path = path.relative_to(output_dir)
        if ".git" in relative_path.parts:
            continue
        if path.is_dir():
            try:
                path.rmdir()
            except OSError:
                pass


def format_duration(seconds: float) -> str:
    if seconds < 60:
        return f"{seconds:.2f} seconds"

    minutes = seconds // 60
    sec = int(seconds) % 60
    return f"{minutes} minutes and {sec} seconds"


def main() -> None:
    start_time = perf_counter()

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
    parser.add_argument(
        "-m",
        "--message",
        dest="commit_message",
        default="Update file properties",
        help="Commit message to use when changes are committed",
    )
    args = parser.parse_args()

    input_dir = args.input_dir.expanduser().resolve()
    output_dir = args.output_dir.expanduser().resolve()

    if not input_dir.is_dir():
        parser.error(f"input_dir must be an existing directory: {input_dir}")

    output_dir.mkdir(parents=True, exist_ok=True)

    files = FileProperties.collect_from_tree(input_dir)
    expected_files = {Path(file.path) for file in files}
    expected_files.add(Path(STATS_FILE_NAME))

    remove_stale_files(output_dir, expected_files)

    for file in files:
        output_file = output_dir / file.path
        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(
            json.dumps(file.to_dict(), indent=2),
            encoding="utf-8",
        )

    stats_file = output_dir / STATS_FILE_NAME
    stats_file.write_text(
        "Files processed: "
        f"{len(files)}\n"
        "\n"
        "Processed files:\n" + "".join(f"{file.path}\n" for file in files),
        encoding="utf-8",
    )

    try:
        commit_created = GitSystem(output_dir).create_repository(args.commit_message)
    except RuntimeError as error:
        parser.exit(1, f"error: {error}\n")

    elapsed_time = perf_counter() - start_time

    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Files processed: {len(files)}")
    print(f"Git commit created: {commit_created}")
    print(f"Total time: {format_duration(elapsed_time)}")
