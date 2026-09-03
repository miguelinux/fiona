# SPDX-FileCopyrightText: 2026, Qualcomm Technologies, Inc.
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import subprocess  # nosec B404 blacklist
from importlib.metadata import PackageNotFoundError
from importlib.metadata import version
from pathlib import Path


def get_version() -> str:
    base_version = _base_version()
    git_revision = _git_revision()

    if git_revision is None:
        return base_version

    return f"{git_revision[1:]}"


def _base_version() -> str:
    try:
        return version("fiona")
    except PackageNotFoundError:
        return "unknown"


def _git_revision() -> str | None:
    project_dir = Path(__file__).resolve().parents[2]
    git_dir = project_dir / ".git"
    if not git_dir.exists():
        return None

    try:
        result = subprocess.run(  # nosec B603 subprocess_without_shell_equals_true
            ["/usr/bin/git", "describe", "--tags", "--dirty"],
            cwd=project_dir,
            check=True,
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None

    return result.stdout.strip() or None
