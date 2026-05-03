from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from secureli.modules.shared.consts.pii import IGNORED_EXTENSIONS
from secureli.modules.shared.consts.repository import default_ignored_extensions
from secureli.modules.shared.models.echo import Level
from secureli.modules.shared.models.language import LanguageSupportSettings


class PiiScannerSettings(BaseSettings):
    """Settings that adjust how seCureLI evaluates the PII of the consuming repository."""

    model_config = SettingsConfigDict(extra="ignore")

    ignored_extensions: list[str] = Field(default=IGNORED_EXTENSIONS)


class RepoFilesSettings(BaseSettings):
    """Settings that adjust how seCureLI evaluates the consuming repository."""

    model_config = SettingsConfigDict(extra="ignore")

    max_file_size: int = Field(default=100000)
    ignored_file_extensions: list[str] = Field(default=default_ignored_extensions)
    exclude_file_patterns: list[str] = Field(default_factory=list)


class CustomScanSettings(BaseSettings):
    """Settings that maintain user defined custom scan patterns"""

    model_config = SettingsConfigDict(extra="ignore")

    custom_scan_patterns: list[str] = Field(default_factory=list)


class EchoSettings(BaseSettings):
    """Settings that affect how seCureLI provides information to the user."""

    model_config = SettingsConfigDict(extra="ignore")

    level: Level = Field(default=Level.warn)


class TelemetrySettings(BaseSettings):
    """Settings for telemetry/logging i.e. New Relic logs"""

    model_config = SettingsConfigDict(extra="ignore")

    api_url: Optional[str] = None


class PreCommitHook(BaseModel):
    """Hook settings for pre-commit."""

    model_config = ConfigDict(extra="ignore")

    id: str
    arguments: Optional[list[str]] = Field(default_factory=list)
    additional_args: Optional[list[str]] = Field(default_factory=list)
    exclude_file_patterns: Optional[list[str]] = Field(default_factory=list)


class PreCommitRepo(BaseModel):
    """Repo settings for pre-commit."""

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    url: str = Field(alias="repo")
    rev: Optional[str] = None
    hooks: list[PreCommitHook] = Field(default_factory=list)
    suppressed_hook_ids: list[str] = Field(default_factory=list)


class PreCommitSettings(BaseModel):
    """
    Various adjustments that affect how seCureLI configures the pre-commit system.

    Extends schema for .pre-commit-config.yaml file.
    See for details: https://pre-commit.com/#pre-commit-configyaml---top-level

    """

    model_config = ConfigDict(extra="ignore")

    repos: list[PreCommitRepo] = Field(default_factory=list)
    suppressed_repos: list[str] = Field(default_factory=list)


class SecureliFile(BaseModel):
    """Represents the contents of the .secureli.yaml file"""

    model_config = ConfigDict(extra="ignore")

    repo_files: Optional[RepoFilesSettings] = None
    echo: Optional[EchoSettings] = None
    language_support: Optional[LanguageSupportSettings] = Field(default=None)
    telemetry: Optional[TelemetrySettings] = None
    scan_patterns: Optional[CustomScanSettings] = None
    pii_scanner: Optional[PiiScannerSettings] = None
