#!/usr/bin/env python3
"""Validate repository structure and local Markdown links without dependencies."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")

REQUIRED = [
    "README.md",
    "DISCLAIMER.md",
    "SECURITY.md",
    "docs/01-engagement-model.md",
    "docs/02-prerequisites-and-client-intake.md",
    "docs/03-scope-and-rules-of-engagement.md",
    "docs/04-testing-methodology.md",
    "docs/05-ad-test-catalog.md",
    "docs/06-tooling.md",
    "docs/07-timeline-effort-and-noise.md",
    "docs/08-automation-architecture.md",
    "docs/09-ai-models-and-token-budget.md",
    "docs/10-nodezero-public-source-analysis.md",
    "docs/11-reporting-and-deliverables.md",
    "docs/12-safety-and-risk-register.md",
    "architecture/system-design.md",
    "templates/client-questionnaire.md",
    "templates/rules-of-engagement.md",
    "templates/test-plan.md",
    "templates/finding-template.md",
    "templates/evidence-log.csv",
    "references/sources.md",
]

PROHIBITED_SUFFIXES = {
    ".ccache",
    ".dmp",
    ".kirbi",
    ".keytab",
    ".ntds",
    ".pfx",
    ".sam",
}


def local_link_target(markdown_file: Path, raw_target: str) -> Path | None:
    target = raw_target.strip().strip("<>")
    if target.startswith(("http://", "https://", "mailto:", "#")):
        return None
    target = unquote(target.split("#", 1)[0])
    if not target:
        return None
    return (markdown_file.parent / target).resolve()


def validate() -> list[str]:
    errors: list[str] = []

    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"missing required file: {relative}")

    for path in ROOT.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.is_file() and path.suffix.lower() in PROHIBITED_SUFFIXES:
            errors.append(f"prohibited sensitive artifact suffix: {path.relative_to(ROOT)}")

    for markdown_file in ROOT.rglob("*.md"):
        text = markdown_file.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = local_link_target(markdown_file, match.group(1))
            if target is not None and not target.exists():
                errors.append(
                    f"broken local link in {markdown_file.relative_to(ROOT)}: {match.group(1)}"
                )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print(f"Repository validation passed ({len(REQUIRED)} required files).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
