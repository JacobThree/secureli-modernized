"""JSON-serializable scan payloads (pure data; no I/O)."""

from __future__ import annotations

from typing import Any

from secureli.modules.shared.models.scan import ScanResult

SCAN_OUTPUT_SCHEMA_VERSION = "1"


def build_scan_payload(
    scan_result: ScanResult,
    *,
    schema_version: str = SCAN_OUTPUT_SCHEMA_VERSION,
) -> dict[str, Any]:
    """
    Build a stable JSON-compatible dict for ScanResult outputs (hooks + custom scanners).

    Each failure exposes repo, id, file, and exitCode per the ScanFailure contract.
    """
    return {
        "schema_version": schema_version,
        **scan_result.model_dump(mode="json"),
    }
