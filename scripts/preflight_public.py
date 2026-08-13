#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".ini",
    ".py", ".js", ".ts", ".tsx", ".jsx", ".ps1", ".sh", ".css", ".html"
}

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}

SUSPICIOUS_PATH_PARTS = {
    "private", "_private", "personal", "journal", "journals", "diary",
    "backup", "backups", "exports-private", "attachments-private"
}

PATTERNS = [
    ("OpenAI-style API key", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("Private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("Bearer token", re.compile(r"(?i)\bAuthorization\s*:\s*Bearer\s+\S+")),
    ("Generic secret assignment", re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|secret|password)\b\s*[:=]\s*[\"']?[^\"'\s]{8,}"
    )),
    ("Windows absolute user path", re.compile(r"(?i)\b[A-Z]:\\Users\\[^\\\s]+")),
    ("macOS user path", re.compile(r"/Users/[^/\s]+")),
    ("Linux home path", re.compile(r"/home/[^/\s]+")),
]

ALLOWLIST_MARKERS = {
    "YOUR_API_KEY",
    "example-token",
    "example-secret",
    "<TOKEN>",
    "<API_KEY>",
    "${VAULT_ROOT}",
}

def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.name == "preflight_public.py":
            continue
        yield path

def main() -> int:
    parser = argparse.ArgumentParser(description="Preflight a repository before public publication.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings = []

    for path in iter_files(root):
        rel = path.relative_to(root)

        lower_parts = {part.lower() for part in rel.parts}
        risky = lower_parts & SUSPICIOUS_PATH_PARTS
        if risky:
            findings.append((str(rel), 0, f"suspicious private path component: {', '.join(sorted(risky))}"))

        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in {".gitignore", "LICENSE"}:
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        except OSError as exc:
            findings.append((str(rel), 0, f"could not read file: {exc}"))
            continue

        for line_no, line in enumerate(text.splitlines(), start=1):
            if any(marker in line for marker in ALLOWLIST_MARKERS):
                continue
            for label, pattern in PATTERNS:
                if pattern.search(line):
                    findings.append((str(rel), line_no, label))

    if findings:
        print("PUBLIC PREFLIGHT FAILED\n")
        for path, line_no, message in findings:
            location = f"{path}:{line_no}" if line_no else path
            print(f"- {location}: {message}")
        print("\nReview every finding before publishing.")
        return 1

    print("Public preflight passed: no configured secret/privacy patterns were detected.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
