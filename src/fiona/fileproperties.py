# SPDX-FileCopyrightText: 2026, Qualcomm Technologies, Inc.
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from datetime import timezone
from pathlib import Path
from stat import filemode
from typing import Any

DEFAULT_STATS = "path,name,size,changed"
STAT_ALIASES = {
    "path": "path",
    "p": "path",
    "name": "name",
    "n": "name",
    "size": "size",
    "s": "size",
    "permissions": "permissions",
    "e": "permissions",
    "access": "access",
    "a": "access",
    "modified": "modified",
    "m": "modified",
    "changed": "changed",
    "c": "changed",
    "birth": "birth",
    "b": "birth",
}


def parse_stats(value: str) -> list[str]:
    selected_stats: list[str] = []

    for raw_stat in value.split(","):
        stat = raw_stat.strip().lower()
        if not stat:
            continue

        if stat not in STAT_ALIASES:
            valid_stats = ", ".join(sorted(STAT_ALIASES))
            raise ValueError(f"invalid stat '{raw_stat}'. Valid stats: {valid_stats}")

        canonical_stat = STAT_ALIASES[stat]
        if canonical_stat not in selected_stats:
            selected_stats.append(canonical_stat)

    if not selected_stats:
        raise ValueError("at least one stat must be selected")

    return selected_stats


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
            if path.name in {".gitattributes", ".gitignore"}:
                continue
            if path.is_file():
                files.append(cls.from_path(path, input_dir))

        return files

    def to_dict(self, selected_stats: list[str]) -> dict[str, Any]:
        values = {
            "path": self.path,
            "name": self.name,
            "size": self.size,
            "permissions": self.permissions,
            "access": self.accessed_at,
            "modified": self.modified_at,
            "changed": self.changed_at,
            "birth": self.birth_at,
        }

        return {stat: values[stat] for stat in selected_stats}

    @staticmethod
    def _timestamp(value: float | None) -> str | None:
        if value is None:
            return None

        return datetime.fromtimestamp(value, tz=timezone.utc).isoformat()
