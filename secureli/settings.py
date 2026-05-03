from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)
from pydantic_settings.sources.providers.yaml import YamlConfigSettingsSource

from secureli.modules.shared.models.language import LanguageSupportSettings
import secureli.modules.shared.models.repository as repo_settings
import secureli.repositories.secureli_config as SecureliConfig


class SecureliYamlSettingsSource(YamlConfigSettingsSource):
    """
    Load `.secureli.yaml` beside `SecureliConfig.FOLDER_PATH` (ordering matches
    legacy `customise_sources`: init → yaml → env → secrets; dotenv omitted like v1).
    """

    def __init__(self, settings_cls: type[BaseSettings]):
        yaml_path = Path(SecureliConfig.FOLDER_PATH) / ".secureli.yaml"
        super().__init__(settings_cls, yaml_file=yaml_path, yaml_file_encoding="utf-8")


class Settings(BaseSettings):
    """
    Settings from env, `.secureli.yaml`, and defaults (`pydantic-settings` v2).
    """

    model_config = SettingsConfigDict(env_file_encoding="utf-8")

    repo_files: repo_settings.RepoFilesSettings = Field(
        default_factory=repo_settings.RepoFilesSettings
    )
    echo: repo_settings.EchoSettings = Field(default_factory=repo_settings.EchoSettings)
    language_support: LanguageSupportSettings = Field(
        default_factory=LanguageSupportSettings
    )
    telemetry: repo_settings.TelemetrySettings = Field(
        default_factory=repo_settings.TelemetrySettings
    )
    scan_patterns: repo_settings.CustomScanSettings = Field(
        default_factory=repo_settings.CustomScanSettings
    )
    pii_scanner: repo_settings.PiiScannerSettings = Field(
        default_factory=repo_settings.PiiScannerSettings
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        del dotenv_settings  # v1 customise_sources did not include dotenv
        return (
            init_settings,
            SecureliYamlSettingsSource(settings_cls),
            env_settings,
            file_secret_settings,
        )


def secureli_yaml_settings(_: Any = None) -> dict[str, Any]:
    """Load `.secureli.yaml` as a plain dict (used by helpers/tests)."""
    path_to_settings = Path(SecureliConfig.FOLDER_PATH) / ".secureli.yaml"
    if not path_to_settings.exists():
        return {}
    import yaml

    with open(path_to_settings, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}
