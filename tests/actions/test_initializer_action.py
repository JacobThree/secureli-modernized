from pathlib import Path
from unittest.mock import MagicMock, ANY

import pytest

from secureli.actions.action import ActionDependencies
from secureli.actions.initializer import InitializerAction
from secureli.modules.shared.models.install import VerifyOutcome
from secureli.modules.shared.models.language import (
    AnalyzeResult,
    BuildConfigResult,
    LanguageMetadata,
    LanguageNotSupportedError,
)
from secureli.modules.shared.models import config as ConfigModels
from secureli.modules.shared.models.logging import LogAction

test_folder_path = Path("does-not-matter")


@pytest.fixture()
def mock_hooks_scanner() -> MagicMock:
    mock_hooks_scanner = MagicMock()
    return mock_hooks_scanner


@pytest.fixture()
def mock_updater() -> MagicMock:
    mock_updater = MagicMock()
    return mock_updater


@pytest.fixture()
def action_deps(
    mock_echo: MagicMock,
    mock_language_analyzer: MagicMock,
    mock_language_support: MagicMock,
    mock_hooks_scanner: MagicMock,
    mock_secureli_config: MagicMock,
    mock_settings: MagicMock,
    mock_updater: MagicMock,
    mock_logging_service: MagicMock,
) -> ActionDependencies:
    return ActionDependencies(
        mock_echo,
        mock_language_analyzer,
        mock_language_support,
        mock_hooks_scanner,
        mock_secureli_config,
        mock_settings,
        mock_updater,
        mock_logging_service,
    )


@pytest.fixture()
def initializer_action(
    action_deps: ActionDependencies,
) -> InitializerAction:
    return InitializerAction(
        action_deps=action_deps,
    )


def test_that_initialize_repo_does_not_load_config_when_resetting(
    initializer_action: InitializerAction,
    mock_secureli_config: MagicMock,
):
    initializer_action.initialize_repo(test_folder_path, True, True)

    mock_secureli_config.load.assert_not_called()

    initializer_action.action_deps.logging.success.assert_called_with(LogAction.init)


def test_that_initialize_repo_logs_failure_when_failing_to_verify(
    initializer_action: InitializerAction,
    mock_language_analyzer: MagicMock,
):
    mock_language_analyzer.analyze.side_effect = LanguageNotSupportedError

    initializer_action.initialize_repo(test_folder_path, True, True)

    initializer_action.action_deps.logging.failure.assert_called_once_with(
        LogAction.init, ANY
    )


def test_that_initialize_repo_dry_run_skips_writes_and_logs(
    initializer_action: InitializerAction,
    mock_secureli_config: MagicMock,
    mock_settings: MagicMock,
    mock_language_support: MagicMock,
    mock_language_analyzer: MagicMock,
    mock_hooks_scanner: MagicMock,
):
    mock_secureli_config.verify.return_value = (
        ConfigModels.VerifyConfigOutcome.UP_TO_DATE
    )
    mock_secureli_config.load.return_value = ConfigModels.SecureliConfig()
    mock_language_analyzer.analyze.return_value = AnalyzeResult(
        language_proportions={"RadLang": 1.0},
        skipped_files=[],
    )

    mock_language_support.build_pre_commit_config.return_value = BuildConfigResult(
        successful=True,
        languages_added=["RadLang"],
        config_data={
            "repos": [
                {"repo": "https://example.com/hooks.git", "rev": "1", "hooks": []}
            ]
        },
        version="v1",
        linter_configs=[],
    )
    mock_language_support.apply_support.return_value = LanguageMetadata(
        version="mv",
        security_hook_id=None,
        linter_config_write_errors=[],
    )

    mock_hooks_scanner.pre_commit.get_pre_commit_config_path_is_correct.return_value = (
        True
    )
    mock_hooks_scanner.pre_commit.pre_commit_config_exists.return_value = False

    result = initializer_action.initialize_repo(
        test_folder_path, False, True, dry_run=True
    )

    assert result.outcome == VerifyOutcome.INSTALL_SUCCEEDED
    mock_secureli_config.save.assert_not_called()
    mock_settings.save.assert_not_called()
    initializer_action.action_deps.logging.success.assert_not_called()
    initializer_action.action_deps.logging.failure.assert_not_called()
    assert mock_language_support.apply_support.call_args.kwargs.get("dry_run") is True
    initializer_action.action_deps.updater.pre_commit.install.assert_not_called()
