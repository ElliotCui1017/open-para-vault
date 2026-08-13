#!/usr/bin/env python3
"""Fail closed on common privacy hazards in the public tree and Git history."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath


TEXT_EXTENSIONS = {
    ".css",
    ".html",
    ".ini",
    ".js",
    ".json",
    ".jsx",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}

TEXT_FILENAMES = {".gitattributes", ".gitignore", "LICENSE"}
SKIP_DIRS = {".git", ".venv", "build", "coverage", "dist", "node_modules", "venv"}
SKIP_CONTENT_PATHS = {"scripts/preflight_public.py"}

PRIVATE_PATH_PARTS = {
    "_private",
    "attachment",
    "attachments",
    "attachments-private",
    "auth-cache",
    "backup",
    "backups",
    "diary",
    "exports-private",
    "inbox-private",
    "journal",
    "journals",
    "personal",
    "private",
}

GENERATED_PATH_PARTS = {"__pycache__", ".ipynb_checkpoints", ".trash"}

HIGH_RISK_EXTENSIONS = {
    ".cer",
    ".crt",
    ".env",
    ".kdbx",
    ".key",
    ".mobileprovision",
    ".ovpn",
    ".p12",
    ".pem",
    ".pfx",
    ".sqlite",
    ".sqlite3",
}

ATTACHMENT_EXTENSIONS = {
    ".7z",
    ".avi",
    ".doc",
    ".docx",
    ".gif",
    ".heic",
    ".jpeg",
    ".jpg",
    ".mov",
    ".mp3",
    ".mp4",
    ".pdf",
    ".png",
    ".ppt",
    ".pptx",
    ".rar",
    ".wav",
    ".xls",
    ".xlsx",
    ".zip",
}

PATTERNS = [
    ("OpenAI-style API key", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("private key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("bearer token", re.compile(r"(?i)\bAuthorization\s*:\s*Bearer\s+\S+")),
    (
        "secret-like assignment",
        re.compile(
            r"(?i)\b(?:api[_-]?key|access[_-]?token|client[_-]?secret|password)\b"
            r"\s*[:=]\s*[\"']?[^\"'\s,}]{8,}"
        ),
    ),
    ("Windows user-home path", re.compile(r"(?i)\b[A-Z]:\\Users\\[^\\\s]+")),
    ("macOS user-home path", re.compile(r"/Users/[^/\s]+")),
    ("Linux user-home path", re.compile(r"/home/[^/\s]+")),
    (
        "email address",
        re.compile(r"(?i)\b[A-Z0-9._%+-]+@([A-Z0-9.-]+\.[A-Z]{2,})\b"),
    ),
    (
        "phone number",
        re.compile(
            r"(?x)(?:\+\d{1,3}[ .()-]*)?(?:\(\d{2,4}\)[ .-]*)"
            r"\d{3,4}[ .-]*\d{3,4}\b|\+\d{1,3}[ -]\d{2,4}[ -]\d{3,4}[ -]\d{3,4}\b"
        ),
    ),
    (
        "student identifier",
        re.compile(r"(?i)\b(?:student|university)\s*(?:id|number)\D{0,12}\d{6,12}\b"),
    ),
    (
        "street address",
        re.compile(
            r"(?i)\b\d{1,5}\s+[A-Z][A-Z .'-]{2,40}\s"
            r"(?:street|st|road|rd|avenue|ave|boulevard|blvd|lane|ln|drive|dr|court|ct)\b"
        ),
    ),
]

ALLOWED_EMAIL_DOMAINS = {"example.com", "example.invalid", "users.noreply.github.com"}
MAINTAINER_EMAILS = {
    "ElliotCui1017": "221169086+ElliotCui1017@users.noreply.github.com",
}
MAX_TEXT_BYTES = 2 * 1024 * 1024
IGNORED_LINE_MARKER = "PUBLIC_PREFLIGHT_PATTERN_DEFINITION"


def posix_path(path: Path) -> str:
    return path.as_posix()


def path_findings(relative: str) -> list[str]:
    path = PurePosixPath(relative)
    parts = {part.lower() for part in path.parts}
    name = path.name.lower()
    suffix = path.suffix.lower()
    findings: list[str] = []

    risky_parts = sorted(parts & PRIVATE_PATH_PARTS)
    if risky_parts:
        findings.append(f"private path component: {', '.join(risky_parts)}")

    generated_parts = sorted(parts & GENERATED_PATH_PARTS)
    if generated_parts:
        findings.append(f"generated/cache path component: {', '.join(generated_parts)}")

    if name == ".env" or name.startswith(".env."):
        findings.append("environment file")
    if suffix in HIGH_RISK_EXTENSIONS:
        findings.append(f"high-risk file extension: {suffix}")
    if suffix in ATTACHMENT_EXTENSIONS:
        findings.append(f"attachment or archive requires explicit review: {suffix}")
    if name.startswith(("credential", "secrets.", "token.", "cookies.")):
        findings.append("credential-like filename")

    return findings


def text_findings(text: str) -> list[tuple[int, str]]:
    findings: list[tuple[int, str]] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if IGNORED_LINE_MARKER in line:
            continue
        for label, pattern in PATTERNS:
            for match in pattern.finditer(line):
                if label == "email address" and match.group(1).lower() in ALLOWED_EMAIL_DOMAINS:
                    continue
                findings.append((line_number, label))
    return findings


def scan_worktree(root: Path) -> list[tuple[str, int, str]]:
    findings: list[tuple[str, int, str]] = []
    for path in root.rglob("*"):
        relative_path = path.relative_to(root)
        relative = posix_path(relative_path)

        if any(part in SKIP_DIRS for part in relative_path.parts):
            continue
        if path.is_symlink():
            findings.append((relative, 0, "symbolic link requires explicit review"))
            continue
        if not path.is_file():
            continue

        for message in path_findings(relative):
            findings.append((relative, 0, message))

        if relative in SKIP_CONTENT_PATHS:
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS and path.name not in TEXT_FILENAMES:
            continue

        try:
            if path.stat().st_size > MAX_TEXT_BYTES:
                findings.append((relative, 0, "text file exceeds public review size limit"))
                continue
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            findings.append((relative, 0, "declared text file is not valid UTF-8"))
            continue
        except OSError:
            findings.append((relative, 0, "could not read file"))
            continue

        for line_number, message in text_findings(text):
            findings.append((relative, line_number, message))

    return findings


def run_git(root: Path, *args: str) -> bytes:
    return subprocess.check_output(
        ["git", "-C", str(root), *args], stderr=subprocess.STDOUT
    )


def scan_history(root: Path) -> list[tuple[str, int, str]]:
    if not (root / ".git").exists():
        return []

    findings: list[tuple[str, int, str]] = []
    seen_paths: set[str] = set()
    seen_blobs: set[tuple[str, str]] = set()

    try:
        commits = run_git(root, "rev-list", "--all").decode("ascii").splitlines()
        for commit in commits:
            records = run_git(root, "ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0")
            for record in records:
                if not record:
                    continue
                metadata, path_bytes = record.split(b"\t", 1)
                _mode, object_type, object_id = metadata.decode("ascii").split()
                if object_type != "blob":
                    continue
                relative = path_bytes.decode("utf-8", errors="strict")

                if relative not in seen_paths:
                    for message in path_findings(relative):
                        findings.append((f"history:{relative}", 0, message))
                    seen_paths.add(relative)

                if relative in SKIP_CONTENT_PATHS:
                    continue
                suffix = PurePosixPath(relative).suffix.lower()
                name = PurePosixPath(relative).name
                if suffix not in TEXT_EXTENSIONS and name not in TEXT_FILENAMES:
                    continue

                blob_key = (object_id, relative)
                if blob_key in seen_blobs:
                    continue
                seen_blobs.add(blob_key)

                size = int(run_git(root, "cat-file", "-s", object_id).decode("ascii"))
                if size > MAX_TEXT_BYTES:
                    findings.append((f"history:{relative}", 0, "historical text blob exceeds review size limit"))
                    continue
                data = run_git(root, "cat-file", "blob", object_id)
                try:
                    text = data.decode("utf-8")
                except UnicodeDecodeError:
                    findings.append((f"history:{relative}", 0, "historical text blob is not valid UTF-8"))
                    continue
                for line_number, message in text_findings(text):
                    findings.append((f"history:{relative}", line_number, message))
    except (OSError, subprocess.CalledProcessError, UnicodeError, ValueError):
        findings.append((".git", 0, "could not complete Git history scan"))

    return findings


def scan_commit_metadata(root: Path) -> list[tuple[str, int, str]]:
    """Require known maintainer identities to use their configured public email."""
    if not (root / ".git").exists():
        return []

    findings: list[tuple[str, int, str]] = []
    try:
        output = run_git(
            root,
            "log",
            "--all",
            "--format=%H%x00%an%x00%ae%x00%cn%x00%ce",
        ).decode("utf-8")
        for record in output.splitlines():
            fields = record.split("\0")
            if len(fields) != 5:
                findings.append((".git", 0, "could not parse commit identity metadata"))
                continue
            commit, author_name, author_email, committer_name, committer_email = fields
            identities = (
                ("author", author_name, author_email),
                ("committer", committer_name, committer_email),
            )
            for role, name, email in identities:
                expected = MAINTAINER_EMAILS.get(name)
                if expected is not None and email.casefold() != expected.casefold():
                    findings.append(
                        (
                            f"history:{commit}",
                            0,
                            f"maintainer {role} email does not match the public identity",
                        )
                    )
    except (OSError, subprocess.CalledProcessError, UnicodeError):
        findings.append((".git", 0, "could not complete commit metadata scan"))

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Preflight a repository tree and its Git history before publication."
    )
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"Public preflight failed: not a directory: {root}", file=sys.stderr)
        return 2

    findings = scan_worktree(root) + scan_history(root) + scan_commit_metadata(root)
    unique_findings = sorted(set(findings))

    if unique_findings:
        print("PUBLIC PREFLIGHT FAILED\n")
        for path, line_number, message in unique_findings:
            location = f"{path}:{line_number}" if line_number else path
            print(f"- {location}: {message}")
        print("\nNo matched values were printed. Review every path before publishing.")
        return 1

    history_note = " and Git history" if (root / ".git").exists() else ""
    print(f"Public preflight passed: working tree{history_note} contain no configured findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
