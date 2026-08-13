#!/usr/bin/env python3
"""Build a deterministic, privacy-safe Obsidian starter-vault archive."""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from preflight_public import path_findings, text_findings


OBSIDIAN_ALLOWLIST = frozenset(
    {
        "app.json",
        "community-plugins.json",
        "core-plugins.json",
        "daily-notes.json",
        "templates.json",
    }
)
EXPECTED_VAULT_FOLDERS = frozenset(
    {
        ".obsidian",
        "00_Inbox",
        "01_Daily",
        "02_Projects",
        "03_Areas",
        "04_Resources",
        "05_Wiki",
        "06_Archive",
        "99_Templates",
    }
)
ALLOWED_SUFFIXES = frozenset({".json", ".md"})
FORBIDDEN_PARTS = frozenset(
    {
        ".git",
        ".ipynb_checkpoints",
        ".trash",
        ".venv",
        "__pycache__",
        "build",
        "cache",
        "coverage",
        "dist",
        "local storage",
        "node_modules",
        "plugins",
        "temp",
        "tmp",
        "venv",
    }
)
FORBIDDEN_NAMES = frozenset(
    {
        "workspace.json",
        "workspace-mobile.json",
    }
)
HIGH_RISK_SUFFIXES = frozenset(
    {
        ".env",
        ".key",
        ".p12",
        ".pem",
        ".pfx",
        ".sqlite",
        ".sqlite3",
    }
)
CREDENTIAL_NAME_PREFIXES = ("auth.", "cookies.", "credential", "secrets.", "token.")
VERSION_PATTERN = re.compile(r"v\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?\Z")
FIXED_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


class PackageError(ValueError):
    """Raised when starter-vault input or output violates the safety contract."""


@dataclass(frozen=True)
class BuildResult:
    zip_path: Path
    checksum_path: Path
    sha256: str
    members: tuple[str, ...]


def validate_version(version: str) -> None:
    if VERSION_PATTERN.fullmatch(version) is None:
        raise PackageError(
            "Version must look like v1.2.3 or v1.2.3-suffix and contain only portable characters."
        )


def validate_relative_path(relative: PurePosixPath) -> None:
    parts = tuple(part.casefold() for part in relative.parts)
    name = relative.name.casefold()
    if relative.is_absolute() or not relative.parts or any(part in {"", ".", ".."} for part in relative.parts):
        raise PackageError(f"Unsafe archive path: {relative.as_posix()}")
    forbidden = sorted(set(parts) & FORBIDDEN_PARTS)
    if forbidden:
        raise PackageError(
            f"Forbidden archive path component in {relative.as_posix()}: {', '.join(forbidden)}"
        )
    if name in FORBIDDEN_NAMES:
        raise PackageError(f"Forbidden workspace state: {relative.as_posix()}")
    if name == ".env" or name.startswith(".env.") or relative.suffix.casefold() in HIGH_RISK_SUFFIXES:
        raise PackageError(f"Credential-bearing or high-risk file is forbidden: {relative.as_posix()}")
    if name.startswith(CREDENTIAL_NAME_PREFIXES):
        raise PackageError(f"Credential-like filename is forbidden: {relative.as_posix()}")
    generic_findings = path_findings(relative.as_posix())
    if generic_findings:
        raise PackageError(f"Unsafe archive path {relative.as_posix()}: {generic_findings[0]}")


def validate_obsidian_state(source: Path) -> None:
    obsidian = source / ".obsidian"
    if not obsidian.is_dir():
        raise PackageError("Starter vault is missing the required .obsidian directory.")
    entries = {entry.name for entry in obsidian.iterdir()}
    unexpected = sorted(entries - OBSIDIAN_ALLOWLIST)
    missing = sorted(OBSIDIAN_ALLOWLIST - entries)
    if unexpected:
        raise PackageError(f"Unexpected .obsidian state: {', '.join(unexpected)}")
    if missing:
        raise PackageError(f"Missing allowlisted .obsidian configuration: {', '.join(missing)}")
    for name in sorted(OBSIDIAN_ALLOWLIST):
        if not (obsidian / name).is_file():
            raise PackageError(f"Allowlisted .obsidian entry is not a regular file: {name}")


def collect_source_files(source: Path) -> tuple[tuple[PurePosixPath, bytes], ...]:
    if not source.is_dir():
        raise PackageError(f"Starter-vault source is not a directory: {source}")
    missing_folders = sorted(name for name in EXPECTED_VAULT_FOLDERS if not (source / name).is_dir())
    if missing_folders:
        raise PackageError(f"Starter vault is missing expected folders: {', '.join(missing_folders)}")
    if not (source / "Home.md").is_file():
        raise PackageError("Starter vault is missing Home.md.")

    validate_obsidian_state(source)
    files: list[tuple[PurePosixPath, bytes]] = []
    for path in sorted(source.rglob("*"), key=lambda item: item.relative_to(source).as_posix()):
        relative = PurePosixPath(path.relative_to(source).as_posix())
        validate_relative_path(relative)
        if path.is_symlink():
            raise PackageError(f"Symbolic links are forbidden in the starter vault: {relative.as_posix()}")
        if path.is_dir():
            continue
        if not path.is_file():
            raise PackageError(f"Unsupported filesystem entry: {relative.as_posix()}")
        if relative.parts[0] == ".obsidian" and relative.name not in OBSIDIAN_ALLOWLIST:
            raise PackageError(f"Unexpected .obsidian state: {relative.as_posix()}")
        if relative.suffix.casefold() not in ALLOWED_SUFFIXES:
            raise PackageError(f"Unsupported binary or file type: {relative.as_posix()}")
        data = path.read_bytes()
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise PackageError(f"Starter-vault file is not valid UTF-8: {relative.as_posix()}") from exc
        findings = text_findings(text)
        if findings:
            _line, label = findings[0]
            raise PackageError(f"Unsafe content in {relative.as_posix()}: {label}")
        files.append((relative, data))
    return tuple(files)


def zip_info(name: str, *, directory: bool) -> zipfile.ZipInfo:
    info = zipfile.ZipInfo(name, FIXED_ZIP_TIMESTAMP)
    info.create_system = 3
    info.compress_type = zipfile.ZIP_STORED
    info.external_attr = ((0o40755 if directory else 0o100644) << 16) | (0x10 if directory else 0)
    return info


def validate_archive(zip_path: Path, expected_root: str) -> tuple[str, ...]:
    with zipfile.ZipFile(zip_path, "r") as archive:
        members = tuple(info.filename for info in archive.infolist())
        if len(members) != len(set(members)):
            raise PackageError("Generated archive contains duplicate paths.")
        roots = {PurePosixPath(name).parts[0] for name in members if PurePosixPath(name).parts}
        if roots != {expected_root}:
            raise PackageError("Generated archive must contain exactly one expected top-level directory.")
        for info in archive.infolist():
            path = PurePosixPath(info.filename)
            if path.parts[0] != expected_root:
                raise PackageError(f"Archive member escaped the expected root: {info.filename}")
            relative_parts = path.parts[1:]
            if relative_parts:
                validate_relative_path(PurePosixPath(*relative_parts))
    return members


def build_starter_vault(source: Path, output: Path, version: str) -> BuildResult:
    validate_version(version)
    source = source.resolve()
    output = output.resolve()
    files = collect_source_files(source)
    archive_root = f"open-para-vault-{version}"
    output.mkdir(parents=True, exist_ok=True)
    zip_path = output / f"{archive_root}.zip"
    checksum_path = output / f"{archive_root}.zip.sha256"

    directories = {PurePosixPath()}
    for relative, _data in files:
        directories.update(relative.parents)
    ordered_directories = sorted(
        (path for path in directories if path.parts), key=lambda path: path.as_posix()
    )

    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_STORED) as archive:
        archive.writestr(zip_info(f"{archive_root}/", directory=True), b"")
        for directory in ordered_directories:
            archive.writestr(
                zip_info(f"{archive_root}/{directory.as_posix()}/", directory=True), b""
            )
        for relative, data in files:
            archive.writestr(
                zip_info(f"{archive_root}/{relative.as_posix()}", directory=False), data
            )

    members = validate_archive(zip_path, archive_root)
    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    checksum_path.write_text(f"{digest}  {zip_path.name}\n", encoding="ascii", newline="\n")
    return BuildResult(zip_path, checksum_path, digest, members)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--source",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "examples" / "demo-vault",
        help="Starter-vault source; defaults to the repository's fictional demo vault.",
    )
    args = parser.parse_args()
    try:
        result = build_starter_vault(args.source, args.output, args.version)
    except (OSError, PackageError, zipfile.BadZipFile) as exc:
        print(f"Starter-vault build failed: {exc}", file=sys.stderr)
        return 1
    print(f"Built {result.zip_path}")
    print(f"SHA-256 {result.sha256}")
    print(f"Checksum {result.checksum_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
