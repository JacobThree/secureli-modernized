import json

from secureli.modules.shared.models.scan import ScanFailure, ScanResult
from secureli.modules.shared.scan_output import (
    SCAN_OUTPUT_SCHEMA_VERSION,
    build_scan_payload,
)


def _assert_json_serializable(payload: dict) -> None:
    serialized = json.dumps(payload)
    assert json.loads(serialized) == payload


def test_build_scan_payload_success_empty_failures():
    result = ScanResult(successful=True, failures=[], output=None)
    payload = build_scan_payload(result)

    assert payload["schema_version"] == SCAN_OUTPUT_SCHEMA_VERSION
    assert payload["successful"] is True
    assert payload["failures"] == []
    _assert_json_serializable(payload)


def test_build_scan_payload_failure_with_multiple_failures():
    result = ScanResult(
        successful=False,
        output="hook stderr\nexit 1\n",
        failures=[
            ScanFailure(
                repo="https://example.com/hooks",
                id="markdownlint",
                file="README.md",
                exitCode="1",
            ),
            ScanFailure(
                repo="https://example.com/hooks",
                id="flake8",
                file="secureli/foo.py",
                exitCode="flake8",
            ),
        ],
    )
    payload = build_scan_payload(result)

    assert payload["successful"] is False
    assert payload["output"] == "hook stderr\nexit 1\n"
    assert payload["failures"] == [
        {
            "repo": "https://example.com/hooks",
            "id": "markdownlint",
            "file": "README.md",
            "exitCode": "1",
        },
        {
            "repo": "https://example.com/hooks",
            "id": "flake8",
            "file": "secureli/foo.py",
            "exitCode": "flake8",
        },
    ]
    _assert_json_serializable(payload)


def test_build_scan_payload_uses_explicit_schema_version():
    result = ScanResult(successful=True, failures=[])
    payload = build_scan_payload(result, schema_version="2-preview")

    assert payload["schema_version"] == "2-preview"
