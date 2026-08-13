#!/usr/bin/env python3
"""Validate the public repository structure using only the Python standard library."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

from validate_templates import validate_templates


REQUIRED_FILES = {
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/pull_request_template.md",
    ".github/workflows/public-preflight.yml",
    ".gitignore",
    "AGENTS.md",
    "CHANGELOG.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "MIGRATION_AUDIT.md",
    "README.md",
    "RELEASE_NOTES_v0.1.0.md",
    "ROADMAP.md",
    "SECURITY.md",
    "config/quickadd.example.json",
    "config/templater.example.json",
    "docs/architecture.md",
    "docs/automation.md",
    "docs/initial-issues.md",
    "docs/metadata-conventions.md",
    "docs/privacy-model.md",
    "docs/release-checklist.md",
    "docs/setup.md",
    "docs/workflow.md",
    "scripts/preflight_public.py",
    "scripts/validate_templates.py",
    "scripts/validate_repo.py",
    "tests/test_validate_templates.py",
}

DEMO_FOLDERS = {
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

MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
WIKILINK = re.compile(r"!?(?:\[\[)([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def frontmatter_keys(path: Path) -> set[str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0] != "---":
        return set()
    try:
        end = lines.index("---", 1)
    except ValueError:
        return set()
    keys = set()
    for line in lines[1:end]:
        match = re.match(r"^([A-Za-z][A-Za-z0-9_-]*):", line)
        if match:
            keys.add(match.group(1))
    return keys


def walk_json(value, path: str = ""):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = f"{path}.{key}" if path else key
            yield child_path, key, child
            yield from walk_json(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from walk_json(child, f"{path}[{index}]")


def validate_standard_links(root: Path, errors: list[str]) -> None:
    for markdown in root.rglob("*.md"):
        if ".git" in markdown.parts:
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in MARKDOWN_LINK.findall(text):
            target = raw_target.strip().split("#", 1)[0]
            if not target or "://" in target or target.startswith(("#", "mailto:")):
                continue
            resolved = (markdown.parent / target).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                errors.append(f"Markdown link escapes repository: {markdown.relative_to(root)} -> {target}")
                continue
            if not resolved.exists():
                errors.append(f"Broken Markdown link: {markdown.relative_to(root)} -> {target}")


def validate_demo_wikilinks(demo: Path, errors: list[str]) -> None:
    for markdown in demo.rglob("*.md"):
        if "99_Templates" in markdown.parts:
            continue
        text = markdown.read_text(encoding="utf-8")
        for raw_target in WIKILINK.findall(text):
            target = raw_target.strip()
            candidate = demo / target
            if candidate.suffix.lower() != ".md":
                candidate = candidate.with_suffix(".md")
            if not candidate.exists():
                errors.append(f"Broken demo wikilink: {markdown.relative_to(demo)} -> {target}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate repository structure and examples.")
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    errors: list[str] = []

    for relative in sorted(REQUIRED_FILES):
        if not (root / relative).is_file():
            errors.append(f"Missing required file: {relative}")

    demo = root / "examples" / "demo-vault"
    for folder in sorted(DEMO_FOLDERS):
        if not (demo / folder).is_dir():
            errors.append(f"Missing demo folder: examples/demo-vault/{folder}")

    for json_file in root.rglob("*.json"):
        if ".git" in json_file.parts:
            continue
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"Invalid JSON: {json_file.relative_to(root)} ({exc.__class__.__name__})")
            continue
        for key_path, key, value in walk_json(data):
            if key.lower() in {"apikey", "accesstoken", "authorization", "clientsecret", "cookie", "password"}:
                errors.append(f"Credential-bearing key is not allowed: {json_file.relative_to(root)}:{key_path}")
            if isinstance(value, str) and re.search(r"(?i)(?:[A-Z]:\\Users\\|/Users/|/home/)", value):  # PUBLIC_PREFLIGHT_PATTERN_DEFINITION
                errors.append(f"Absolute user path in JSON: {json_file.relative_to(root)}:{key_path}")

    template_root = root / "templates"
    demo_templates = demo / "99_Templates"
    templates = sorted(template_root.glob("*.md"))
    if not templates:
        errors.append("No reusable templates found")
    template_errors, rendered_template_count = validate_templates(root)
    errors.extend(template_errors)
    if rendered_template_count != len(templates):
        errors.append("Rendered template validator did not cover every reusable template")
    for template in templates:
        mirror = demo_templates / template.name
        if not mirror.is_file():
            errors.append(f"Demo template mirror missing: {mirror.relative_to(root)}")
        elif mirror.read_bytes() != template.read_bytes():
            errors.append(f"Demo template mirror differs: {mirror.relative_to(root)}")

    for note in demo.rglob("*.md"):
        if "99_Templates" in note.parts and note.name != "README.md":
            continue
        keys = frontmatter_keys(note)
        if not {"type", "status", "created", "updated"}.issubset(keys):
            errors.append(f"Demo note has incomplete frontmatter: {note.relative_to(root)}")

    quickadd_path = root / "config" / "quickadd.example.json"
    if quickadd_path.is_file():
        quickadd = json.loads(quickadd_path.read_text(encoding="utf-8"))
        choices = quickadd.get("choices", [])
        if len(choices) < 2:
            errors.append("QuickAdd example must contain at least two capture choices")
        for choice in choices:
            capture_to = choice.get("captureTo", "")
            if not capture_to.startswith("00_Inbox/") or re.search(r"(?i)^[A-Z]:|^/", capture_to):
                errors.append(f"QuickAdd capture path is not portable: {choice.get('name', '<unnamed>')}")
        if quickadd.get("disableOnlineFeatures") is not True:
            errors.append("QuickAdd online features must be disabled in the example")

    templater_path = root / "config" / "templater.example.json"
    if templater_path.is_file():
        templater = json.loads(templater_path.read_text(encoding="utf-8"))
        if templater.get("enable_system_commands") is not False:
            errors.append("Templater system commands must be disabled")
        if templater.get("shell_path"):
            errors.append("Templater shell path must be empty")

    plugin_root = demo / ".obsidian" / "plugins"
    if plugin_root.exists():
        errors.append("Demo vault must not vendor community-plugin files")

    home = demo / "Home.md"
    if home.is_file() and home.read_text(encoding="utf-8").count("```dataview") < 4:
        errors.append("Demo Home must contain at least four Dataview examples")

    validate_standard_links(root, errors)
    validate_demo_wikilinks(demo, errors)

    if errors:
        print("REPOSITORY VALIDATION FAILED\n")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1

    print(
        f"Repository validation passed: {len(templates)} rendered templates, "
        f"{len(list(demo.rglob('*.md')))} demo Markdown files, and all required files are valid."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
