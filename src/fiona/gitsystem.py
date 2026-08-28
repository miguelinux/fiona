# SPDX-FileCopyrightText: 2026, Qualcomm Technologies, Inc.
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import subprocess  # nosec B404 blacklist
from pathlib import Path


class GitSystem:
    def __init__(self, repository_dir: Path) -> None:
        self.repository_dir = repository_dir

    def create_repository(self) -> bool:
        if not (self.repository_dir / ".git").exists():
            self._run("init")

        has_commits = self._has_commits()

        self._run("add", "--all")
        if not self._has_staged_changes():
            return False

        message = "Update file properties" if has_commits else "Initial commit"
        self._run(
            "-c",
            "user.name=Fiona",
            "-c",
            "user.email=fiona@example.invalid",
            "commit",
            "-m",
            message,
        )
        return True

    def _has_commits(self) -> bool:
        result = self._run("rev-parse", "--verify", "HEAD", check=False)
        return result.returncode == 0

    def _has_staged_changes(self) -> bool:
        result = self._run("diff", "--cached", "--quiet", check=False)
        return result.returncode == 1

    def _run(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        command = ["/usr/bin/git", *args]

        try:
            return subprocess.run(  # nosec BB603 subprocess_without_shell_equals_true
                command,
                cwd=self.repository_dir,
                check=check,
                capture_output=True,
                text=True,
            )
        except FileNotFoundError as error:
            raise RuntimeError("git command was not found") from error
        except subprocess.CalledProcessError as error:
            message = error.stderr.strip() or error.stdout.strip()
            raise RuntimeError(
                f"git command failed: {' '.join(command)}\n{message}"
            ) from error
