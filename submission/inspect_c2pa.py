#!/usr/bin/env python3
"""Inspect explicit assets with public c2patool; emit one JSON record per file.

This reports active-manifest claims, not AI detection or signer trust. Unknown
covers missing evidence and records without recognized AI-source claims.
Readable claims remain claims even when validation reports a failure.
The retained tool report can contain sensitive metadata; govern its disclosure.
"""
import argparse
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import sys

AI_SOURCES = {
    "http://cv.iptc.org/newscodes/digitalsourcetype/trainedAlgorithmicMedia",
    "http://cv.iptc.org/newscodes/digitalsourcetype/compositeWithTrainedAlgorithmicMedia",
}
ACTION_LABEL = re.compile(r"c2pa\.actions(?:\.v\d+)?(?:__\d+)?")


def summarize(report):
    result = {"inspection_status": "unrecognized_report", "ai_claim": "unknown"}
    if not isinstance(report, dict):
        return result
    active = report.get("active_manifest")
    manifests = report.get("manifests")
    result["active_manifest"] = active
    result["reported_validation"] = {
        key: report[key] for key in ("validation_status", "validation_results", "validation_state")
        if key in report
    }
    if not isinstance(active, str) or not isinstance(manifests, dict):
        return result
    manifest = manifests.get(active)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("assertions", []), list):
        return result
    sources = set()
    for assertion in manifest.get("assertions", []):
        if not isinstance(assertion, dict) or not ACTION_LABEL.fullmatch(str(assertion.get("label", ""))):
            continue
        data = assertion.get("data")
        actions = data.get("actions", []) if isinstance(data, dict) else []
        if not isinstance(actions, list):
            continue
        for action in actions:
            value = action.get("digitalSourceType") if isinstance(action, dict) else None
            if isinstance(value, str):
                sources.add(value)
    result.update(inspection_status="readable_manifest", digital_source_types=sorted(sources),
                  explicit_ai_source_types=sorted(sources & AI_SOURCES),
                  ai_claim="present" if sources & AI_SOURCES else "unknown")
    return result


def inspect(path, tool, version, timeout, settings):
    record = {"asset": path, "c2patool_version": version,
              "inspection_status": "inspection_error", "ai_claim": "unknown"}
    try:
        asset = Path(path).expanduser().resolve()
        record["asset"] = str(asset)
        if not asset.is_file():
            record["error"] = "asset_is_not_a_file"
            return record
        command = [tool, str(asset)]
        if settings:
            command += ["--settings", settings]
            record["settings_path"] = settings
        completed = subprocess.run(command, capture_output=True, text=True,
                                   timeout=timeout, check=False)
        record.update(tool_exit_code=completed.returncode, tool_stderr=completed.stderr.strip())
        if completed.returncode != 0 and not completed.stdout.strip() and completed.stderr.strip() == "Error: No claim found":
            record["inspection_status"] = "no_manifest_reported"
            return record
        try:
            report = json.loads(completed.stdout)
        except json.JSONDecodeError:
            record.update(error="tool_did_not_return_json", tool_stdout=completed.stdout)
            return record
        record["tool_report"] = report
        record.update(summarize(report))
    except (OSError, RuntimeError, subprocess.TimeoutExpired) as error:
        record["error"] = str(error)
    return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("assets", nargs="+", help="Explicit asset file paths; no recursive scan")
    parser.add_argument("--tool", default="c2patool", help="c2patool executable name or path")
    parser.add_argument("--settings", help="Optional c2patool JSON/TOML settings file")
    parser.add_argument("--timeout", type=float, default=30, help="Seconds per asset (default 30)")
    args = parser.parse_args()
    tool = shutil.which(args.tool)
    if not tool or not math.isfinite(args.timeout) or args.timeout <= 0:
        parser.error("c2patool must be installed and timeout must be positive")
    try:
        version = subprocess.run([tool, "--version"], capture_output=True, text=True,
                                 timeout=10, check=True).stdout.strip()
    except (OSError, subprocess.SubprocessError) as error:
        parser.error(str(error))
    settings = str(Path(args.settings).expanduser().resolve()) if args.settings else None
    failed = False
    for path in args.assets:
        record = inspect(path, tool, version, args.timeout, settings)
        print(json.dumps(record, ensure_ascii=True))
        failed |= record["inspection_status"] in {"inspection_error", "unrecognized_report"} or (
            record.get("tool_exit_code", 0) != 0 and record["inspection_status"] != "no_manifest_reported")
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
