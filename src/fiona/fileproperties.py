# SPDX-FileCopyrightText: 2026, Qualcomm Technologies, Inc.
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from dataclasses import asdict
from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from pathlib import Path
from stat import filemode
from typing import Any


@dataclass(frozen=True)
class FileProperties:
    path: str
    name: str
    size: int
    permissions: str
    accessed_at: str | None
    modified_at: str | None
    changed_at: str | None
    birth_at: str | None

    @classmethod
    def from_path(cls, path: Path, root: Path) -> FileProperties:
        stat_result = path.stat()

        return cls(
            path=str(path.relative_to(root)),
            name=path.name,
            size=stat_result.st_size,
            permissions=filemode(stat_result.st_mode),
            accessed_at=cls._timestamp(stat_result.st_atime),
            modified_at=cls._timestamp(stat_result.st_mtime),
            changed_at=cls._timestamp(stat_result.st_ctime),
            birth_at=cls._timestamp(getattr(stat_result, "st_birthtime", None)),
        )

    @classmethod
    def collect_from_tree(cls, input_dir: Path) -> list[FileProperties]:
        files: list[FileProperties] = []

        for path in input_dir.rglob("*"):
            if {".git", ".repo"}.intersection(path.relative_to(input_dir).parts):
                continue
            if path.is_file():
                files.append(cls.from_path(path, input_dir))

        return files

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @staticmethod
    def _timestamp(value: float | None) -> str | None:
        if value is None:
            return None

        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
