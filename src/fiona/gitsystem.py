from __future__ import annotations

import subprocess  # nosec B404 blacklist
from pathlib import Path


class GitSystem:
    def __init__(self, repository_dir: Path) -> None:
        self.repository_dir = repository_dir

    def create_repository(self) -> None:
        self._run("init")
        self._run("add", ".")
        self._run(
            "-c",
            "user.name=Fiona",
            "-c",
            "user.email=fiona@example.invalid",
            "commit",
            "--allow-empty",
            "-m",
            "Initial commit",
        )

    def _run(self, *args: str) -> None:
        command = ["/usr/bin/git", *args]

        try:
            subprocess.run(  # nosec BB603 subprocess_without_shell_equals_true
                command,
                cwd=self.repository_dir,
                check=True,
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
