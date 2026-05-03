"""Read-only diagnostics for the local seCureLI / pre-commit environment."""

from __future__ import annotations

import importlib.metadata
from importlib.metadata import PackageNotFoundError
import shutil
import sys
from pathlib import Path

import yaml
from packaging.specifiers import SpecifierSet
from packaging.version import Version

from secureli.modules.shared.abstractions.echo import EchoAbstraction
from secureli.modules.shared.abstractions.pre_commit import PreCommitAbstraction
from secureli.modules.shared.models.exit_codes import ExitCode
from secureli.repositories.secureli_config import SecureliConfigRepository
import secureli.repositories.secureli_config as secureli_config_module


class DoctorAction:
    """Runs quick, non-mutating checks (Python range, pre-commit on PATH, hook config)."""

    def __init__(
        self,
        echo: EchoAbstraction,
        pre_commit: PreCommitAbstraction,
        secureli_config: SecureliConfigRepository,
    ):
        self.echo = echo
        self.pre_commit = pre_commit
        self.secureli_config = secureli_config

    @staticmethod
    def _requires_python_spec() -> str:
        try:
            meta = importlib.metadata.metadata("secureli")
            return meta.get("Requires-Python") or ">= 3.9, < 3.13"
        except PackageNotFoundError:
            return ">= 3.9, < 3.13"

    @staticmethod
    def _python_within_supported_range(spec_clause: str) -> bool:
        current = Version(
            f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )
        return SpecifierSet(spec_clause).contains(current)

    def run(self, folder_path: Path) -> None:
        messages: list[str] = []

        spec = self._requires_python_spec()
        if not self._python_within_supported_range(spec):
            messages.append(
                f"This interpreter (Python {sys.version_info.major}.{sys.version_info.minor}) "
                f"is outside secureli's supported range ({spec.strip()})."
            )

        if shutil.which("pre-commit") is None:
            messages.append(
                "`pre-commit` is not on PATH. Install pre-commit "
                "(https://pre-commit.com) or reinstall seCureLI with its dependencies."
            )

        previous_root = secureli_config_module.FOLDER_PATH
        secureli_config_module.FOLDER_PATH = folder_path
        try:
            loaded = self.secureli_config.load()
            if loaded.languages and loaded.version_installed:
                config_path = self.pre_commit.get_preferred_pre_commit_config_path(
                    folder_path
                )
                if not config_path.exists():
                    messages.append(
                        f"seCureLI metadata exists but hook config is missing at `{config_path}`. "
                        "Run `secureli init` in this repository."
                    )
                else:
                    try:
                        with open(config_path, encoding="utf-8") as handle:
                            yaml.safe_load(handle)
                    except yaml.YAMLError as exc:
                        messages.append(
                            f"Hook configuration at `{config_path}` is not valid YAML: {exc}"
                        )
        finally:
            secureli_config_module.FOLDER_PATH = previous_root

        if messages:
            for line in messages:
                self.echo.error(line)
            sys.exit(ExitCode.DOCTOR_FAILED.value)

        self.echo.print("Doctor: all checks passed.")
