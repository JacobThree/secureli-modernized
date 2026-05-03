from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from secureli.actions.doctor import DoctorAction
from secureli.modules.shared.models.config import SecureliConfig
from secureli.modules.shared.models.exit_codes import ExitCode


@pytest.fixture()
def mock_pre_commit_dr() -> MagicMock:
    m = MagicMock()
    m.get_preferred_pre_commit_config_path.return_value = Path(
        "/nonexistent/mock/.pre-commit-config.yaml"
    )
    return m


@pytest.fixture()
def doctor_action(
    mock_echo: MagicMock,
    mock_pre_commit_dr: MagicMock,
    mock_secureli_config: MagicMock,
) -> DoctorAction:
    return DoctorAction(mock_echo, mock_pre_commit_dr, mock_secureli_config)


def test_doctor_passes_when_repo_not_initialized(
    doctor_action: DoctorAction,
    mock_secureli_config: MagicMock,
    mock_echo: MagicMock,
):
    mock_secureli_config.load.return_value = SecureliConfig()
    with patch(
        "secureli.actions.doctor.shutil.which", return_value="/usr/bin/pre-commit"
    ):
        doctor_action.run(Path("."))
    mock_echo.print.assert_called()
    mock_echo.error.assert_not_called()


def test_doctor_passes_when_initialized_and_hook_config_readable(
    doctor_action: DoctorAction,
    mock_secureli_config: MagicMock,
    mock_pre_commit_dr: MagicMock,
    mock_echo: MagicMock,
    tmp_path: Path,
):
    cfg_path = tmp_path / ".secureli" / ".pre-commit-config.yaml"
    cfg_path.parent.mkdir(parents=True)
    cfg_path.write_text(yaml.safe_dump({"repos": []}), encoding="utf-8")
    mock_pre_commit_dr.get_preferred_pre_commit_config_path.return_value = cfg_path
    mock_secureli_config.load.return_value = SecureliConfig(
        languages=["Python"], version_installed="1"
    )
    with patch(
        "secureli.actions.doctor.shutil.which", return_value="/usr/bin/pre-commit"
    ):
        doctor_action.run(tmp_path)
    mock_echo.error.assert_not_called()
    mock_echo.print.assert_called()


def test_doctor_fails_when_pre_commit_missing_from_path(
    doctor_action: DoctorAction,
    mock_secureli_config: MagicMock,
):
    mock_secureli_config.load.return_value = SecureliConfig()
    with patch("secureli.actions.doctor.shutil.which", return_value=None):
        with pytest.raises(SystemExit) as exc:
            doctor_action.run(Path("."))
        assert exc.value.code == ExitCode.DOCTOR_FAILED.value


def test_doctor_fails_when_initialized_but_hook_file_missing(
    doctor_action: DoctorAction,
    mock_secureli_config: MagicMock,
    mock_pre_commit_dr: MagicMock,
    tmp_path: Path,
):
    missing = tmp_path / ".secureli" / ".pre-commit-config.yaml"
    mock_pre_commit_dr.get_preferred_pre_commit_config_path.return_value = missing
    mock_secureli_config.load.return_value = SecureliConfig(
        languages=["Python"], version_installed="1"
    )
    with patch(
        "secureli.actions.doctor.shutil.which", return_value="/usr/bin/pre-commit"
    ):
        with pytest.raises(SystemExit) as exc:
            doctor_action.run(tmp_path)
        assert exc.value.code == ExitCode.DOCTOR_FAILED.value


def test_doctor_fails_on_invalid_yaml(
    doctor_action: DoctorAction,
    mock_secureli_config: MagicMock,
    mock_pre_commit_dr: MagicMock,
    tmp_path: Path,
):
    cfg_path = tmp_path / ".secureli" / ".pre-commit-config.yaml"
    cfg_path.parent.mkdir(parents=True)
    cfg_path.write_text("{ not: valid yaml <<<", encoding="utf-8")
    mock_pre_commit_dr.get_preferred_pre_commit_config_path.return_value = cfg_path
    mock_secureli_config.load.return_value = SecureliConfig(
        languages=["Python"], version_installed="1"
    )
    with patch(
        "secureli.actions.doctor.shutil.which", return_value="/usr/bin/pre-commit"
    ):
        with pytest.raises(SystemExit) as exc:
            doctor_action.run(tmp_path)
        assert exc.value.code == ExitCode.DOCTOR_FAILED.value


def test_doctor_fails_when_python_out_of_range(
    doctor_action: DoctorAction,
    mock_secureli_config: MagicMock,
):
    mock_secureli_config.load.return_value = SecureliConfig()
    with patch(
        "secureli.actions.doctor.shutil.which", return_value="/usr/bin/pre-commit"
    ):
        with patch.object(
            DoctorAction, "_python_within_supported_range", return_value=False
        ):
            with pytest.raises(SystemExit) as exc:
                doctor_action.run(Path("."))
        assert exc.value.code == ExitCode.DOCTOR_FAILED.value
