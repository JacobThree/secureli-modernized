import json

from secureli.modules.shared.models.scan import ScanFailure, ScanResult
from secureli.modules.shared.scan_output import (
    SARIF_SCHEMA_URI,
    SARIF_VERSION,
    build_sarif_payload,
)


def test_build_sarif_payload_success_empty_results():
    result = ScanResult(successful=True, failures=[], output=None)
    payload = build_sarif_payload(result)

    assert payload["version"] == SARIF_VERSION
    assert payload["$schema"] == SARIF_SCHEMA_URI
    assert len(payload["runs"]) == 1
    run = payload["runs"][0]
    assert run["results"] == []
    assert run["tool"]["driver"]["rules"] == []
    serialized = json.dumps(payload)
    assert json.loads(serialized) == payload


def test_build_sarif_payload_includes_rules_and_results_sorted_golden():
    """Stable ``sort_keys=True`` snapshot for one failure (different hook ids → two rules)."""
    result = ScanResult(
        successful=False,
        output="ignored for sarif builder",
        failures=[
            ScanFailure(
                repo="https://hooks.example/repo",
                id="flake8",
                file="secureli/foo.py",
                exitCode="1",
            ),
            ScanFailure(
                repo="https://hooks.example/other",
                id="detect-secrets",
                file=".env",
                exitCode="1",
            ),
        ],
    )
    payload = build_sarif_payload(result)
    dumped = json.dumps(payload, sort_keys=True)

    parsed = json.loads(dumped)
    assert parsed["version"] == SARIF_VERSION
    run = parsed["runs"][0]
    assert {r["id"] for r in run["tool"]["driver"]["rules"]} == {
        "detect-secrets",
        "flake8",
    }
    assert len(run["results"]) == 2
    assert run["results"][0]["ruleId"] == "flake8"
    assert run["results"][1]["ruleId"] == "detect-secrets"

    expected = json.dumps(
        {
            "$schema": SARIF_SCHEMA_URI,
            "runs": [
                {
                    "results": [
                        {
                            "level": "error",
                            "locations": [
                                {
                                    "physicalLocation": {
                                        "artifactLocation": {"uri": "secureli/foo.py"},
                                        "region": {
                                            "startColumn": 1,
                                            "startLine": 1,
                                        },
                                    }
                                }
                            ],
                            "message": {
                                "text": (
                                    "Rule `flake8` failed for `secureli/foo.py` "
                                    "(hook repo: https://hooks.example/repo, exitCode: 1)."
                                )
                            },
                            "partialFingerprints": {
                                "secureli/exitCode": "1",
                                "secureli/repo": "https://hooks.example/repo",
                            },
                            "ruleId": "flake8",
                        },
                        {
                            "level": "error",
                            "locations": [
                                {
                                    "physicalLocation": {
                                        "artifactLocation": {"uri": ".env"},
                                        "region": {
                                            "startColumn": 1,
                                            "startLine": 1,
                                        },
                                    }
                                }
                            ],
                            "message": {
                                "text": (
                                    "Rule `detect-secrets` failed for `.env` "
                                    "(hook repo: https://hooks.example/other, exitCode: 1)."
                                )
                            },
                            "partialFingerprints": {
                                "secureli/exitCode": "1",
                                "secureli/repo": "https://hooks.example/other",
                            },
                            "ruleId": "detect-secrets",
                        },
                    ],
                    "tool": {
                        "driver": {
                            "informationUri": "https://github.com/slalombuild/secureli",
                            "name": "secureli",
                            "rules": [
                                {
                                    "id": "flake8",
                                    "shortDescription": {
                                        "text": "Pre-commit or custom scan rule "
                                        "`flake8` reported an issue."
                                    },
                                },
                                {
                                    "id": "detect-secrets",
                                    "shortDescription": {
                                        "text": "Pre-commit or custom scan rule "
                                        "`detect-secrets` reported an issue."
                                    },
                                },
                            ],
                        }
                    },
                }
            ],
            "version": SARIF_VERSION,
        },
        sort_keys=True,
    )
    assert dumped == expected


def test_build_sarif_empty_file_uri_defaults_to_dot():
    result = ScanResult(
        successful=False,
        failures=[
            ScanFailure(
                repo="r",
                id="x",
                file="",
                exitCode="0",
            ),
        ],
    )
    uri = build_sarif_payload(result)["runs"][0]["results"][0]["locations"][0][
        "physicalLocation"
    ]["artifactLocation"]["uri"]
    assert uri == "."
