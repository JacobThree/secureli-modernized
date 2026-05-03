"""SARIF 2.1.0 log dict builders for scan results (pure data; no I/O).

`ruleId` is always ``ScanFailure.id`` (covers pre-commit hooks and custom scanners).
Repositories and exit codes appear in ``message.text`` and ``partialFingerprints`` for context.

This output is intentionally minimal: it omits fingerprints, snippets, fixes, taxonomies, and run
artifacts that GitHub Advanced Security and other SARIF consumers may optionally use.
"""

from __future__ import annotations

from typing import Any

from secureli.modules.shared.models.scan import ScanFailure, ScanResult

SARIF_VERSION = "2.1.0"
SARIF_SCHEMA_URI = "https://json.schemastore.org/sarif-2.1.0.json"

TOOL_NAME = "secureli"
TOOL_INFORMATION_URI = "https://github.com/slalombuild/secureli"


def _artifact_uri(file_path: str) -> str:
    return file_path if file_path else "."


def _rules_for_failures(failures: list[ScanFailure]) -> list[dict[str, Any]]:
    seen: dict[str, ScanFailure] = {}
    for f in failures:
        if f.id not in seen:
            seen[f.id] = f
    rules: list[dict[str, Any]] = []
    for failure in seen.values():
        rules.append(
            {
                "id": failure.id,
                "shortDescription": {
                    "text": f"Pre-commit or custom scan rule `{failure.id}` reported an issue."
                },
            }
        )
    return rules


def _results_for_failures(failures: list[ScanFailure]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for failure in failures:
        msg = (
            f"Rule `{failure.id}` failed for `{failure.file}` "
            f"(hook repo: {failure.repo}, exitCode: {failure.exitCode})."
        )
        results.append(
            {
                "ruleId": failure.id,
                "level": "error",
                "message": {"text": msg},
                "locations": [
                    {
                        "physicalLocation": {
                            "artifactLocation": {"uri": _artifact_uri(failure.file)},
                            "region": {
                                "startLine": 1,
                                "startColumn": 1,
                            },
                        }
                    }
                ],
                "partialFingerprints": {
                    "secureli/repo": failure.repo,
                    "secureli/exitCode": failure.exitCode,
                },
            }
        )
    return results


def build_sarif_payload(scan_result: ScanResult) -> dict[str, Any]:
    """
    Build a SARIF 2.1.0 log object (JSON-serializable dict) for a merged ``ScanResult``.

    When there are no failures, ``runs[0].results`` and ``tool.driver.rules`` are empty arrays.
    """
    failures = scan_result.failures
    rules = _rules_for_failures(failures)
    results = _results_for_failures(failures)

    run: dict[str, Any] = {
        "tool": {
            "driver": {
                "name": TOOL_NAME,
                "informationUri": TOOL_INFORMATION_URI,
                "rules": rules,
            }
        },
        "results": results,
    }

    return {
        "$schema": SARIF_SCHEMA_URI,
        "version": SARIF_VERSION,
        "runs": [run],
    }
