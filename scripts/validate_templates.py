#!/usr/bin/env python3
"""Render repository templates deterministically and validate their frontmatter."""

from __future__ import annotations

import argparse
import ast
import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path


FIXTURE_VALUES = {
    "title": "Rendered Template",
    "date:YYYY-MM-DD": "2030-01-02",
    "date:YYYY-MM": "2030-01",
    "time:HH:mm": "03:04",
}

PLACEHOLDER = re.compile(r"\{\{([^{}]+)\}\}")
PROPERTY = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(.*)$")
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

COMMON_REQUIRED = frozenset({"type", "status", "created", "updated", "aliases", "tags"})


@dataclass(frozen=True)
class TemplateSchema:
    note_type: str
    statuses: frozenset[str]
    required: frozenset[str] = COMMON_REQUIRED


TEMPLATE_SCHEMAS = {
    "area.md": TemplateSchema("area", frozenset({"active", "inactive", "archived"})),
    "daily-note.md": TemplateSchema("daily", frozenset({"active"})),
    "meeting.md": TemplateSchema("meeting", frozenset({"active", "done"})),
    "monthly-review.md": TemplateSchema("monthly-review", frozenset({"active", "done"})),
    "project.md": TemplateSchema(
        "project",
        frozenset({"idea", "active", "waiting", "paused", "blocked", "done", "archived"}),
    ),
    "quick-capture.md": TemplateSchema("capture", frozenset({"inbox", "processed"})),
    "resource.md": TemplateSchema(
        "resource", frozenset({"unread", "reading", "processed", "archived"})
    ),
    "weekly-review.md": TemplateSchema("weekly-review", frozenset({"active", "done"})),
    "wiki.md": TemplateSchema("wiki", frozenset({"draft", "evergreen", "archived"})),
}


class FrontmatterError(ValueError):
    """Raised when the supported frontmatter subset is invalid."""


def render_template(text: str) -> str:
    """Replace only the placeholders currently supported by this repository."""

    def replace(match: re.Match[str]) -> str:
        expression = match.group(1)
        return FIXTURE_VALUES.get(expression, match.group(0))

    return PLACEHOLDER.sub(replace, text)


def extract_frontmatter(text: str) -> str:
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        raise FrontmatterError("generated note must start with frontmatter delimiter '---'")
    try:
        closing = lines.index("---", 1)
    except ValueError as exc:
        raise FrontmatterError("generated frontmatter is missing closing delimiter '---'") from exc
    if closing == 1:
        raise FrontmatterError("generated frontmatter is empty")
    return "\n".join(lines[1:closing])


def parse_scalar(raw: str, line_number: int):
    value = raw.strip()
    if not value:
        return None
    if value == "[]":
        return []
    if value.startswith(("\"", "'")):
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise FrontmatterError(f"invalid quoted value on frontmatter line {line_number}") from exc
        if not isinstance(parsed, str):
            raise FrontmatterError(f"unsupported scalar on frontmatter line {line_number}")
        return parsed
    if value.startswith("[") or value.endswith("]"):
        raise FrontmatterError(f"invalid inline list on frontmatter line {line_number}")
    return value


def parse_frontmatter(frontmatter: str) -> dict[str, object]:
    """Parse the small YAML subset used by the repository templates."""
    properties: dict[str, object] = {}
    active_list: str | None = None

    for line_number, line in enumerate(frontmatter.splitlines(), start=2):
        if "\t" in line:
            raise FrontmatterError(f"tab indentation on frontmatter line {line_number}")
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        if line.startswith("  - "):
            if active_list is None:
                raise FrontmatterError(f"list item without a property on frontmatter line {line_number}")
            item = line[4:].strip()
            if not item:
                raise FrontmatterError(f"empty list item on frontmatter line {line_number}")
            current = properties[active_list]
            if current is None:
                current = []
                properties[active_list] = current
            elif not isinstance(current, list):
                raise FrontmatterError(f"property '{active_list}' mixes scalar and list values")
            current.append(item)
            continue

        if line.startswith(" "):
            raise FrontmatterError(f"unsupported indentation on frontmatter line {line_number}")

        match = PROPERTY.fullmatch(line)
        if match is None:
            raise FrontmatterError(f"invalid property syntax on frontmatter line {line_number}")
        key, raw_value = match.groups()
        if key in properties:
            raise FrontmatterError(f"duplicate property '{key}'")
        value = parse_scalar(raw_value, line_number)
        properties[key] = value
        active_list = key if value is None else None

    return properties


def validate_template(template: Path, display_path: str, schema: TemplateSchema) -> list[str]:
    errors: list[str] = []
    try:
        source = template.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return [f"{display_path}: template is not readable UTF-8"]

    rendered = render_template(source)
    unresolved = sorted(set(PLACEHOLDER.findall(rendered)))
    if unresolved:
        expressions = ", ".join(f"'{{{{{value}}}}}'" for value in unresolved)
        errors.append(f"{display_path}: generated note contains unresolved placeholder {expressions}")

    try:
        frontmatter = extract_frontmatter(rendered)
        properties = parse_frontmatter(frontmatter)
    except FrontmatterError as exc:
        errors.append(f"{display_path}: {exc}")
        return errors

    for key in sorted(schema.required - properties.keys()):
        errors.append(f"{display_path}: missing required property '{key}'")

    note_type = properties.get("type")
    if note_type is not None and note_type != schema.note_type:
        errors.append(
            f"{display_path}: property 'type' must be '{schema.note_type}', got '{note_type}'"
        )

    status = properties.get("status")
    if status is not None and status not in schema.statuses:
        allowed = ", ".join(sorted(schema.statuses))
        errors.append(f"{display_path}: property 'status' must be one of [{allowed}], got '{status}'")

    for key in ("created", "updated"):
        value = properties.get(key)
        if value is None:
            continue
        if not isinstance(value, str) or ISO_DATE.fullmatch(value) is None:
            errors.append(f"{display_path}: property '{key}' must use YYYY-MM-DD")
            continue
        try:
            date.fromisoformat(value)
        except ValueError:
            errors.append(f"{display_path}: property '{key}' is not a valid calendar date")

    for key in ("aliases", "tags"):
        value = properties.get(key)
        if value is not None and not isinstance(value, list):
            errors.append(f"{display_path}: property '{key}' must be a YAML list")
        elif isinstance(value, list) and any(not isinstance(item, str) or not item for item in value):
            errors.append(f"{display_path}: property '{key}' must contain non-empty strings")

    tags = properties.get("tags")
    if isinstance(tags, list) and not tags:
        errors.append(f"{display_path}: property 'tags' must contain at least one tag")

    # Ensure the fixed fixture itself remains deterministic and locale independent.
    if FIXTURE_VALUES["date:YYYY-MM-DD"] not in rendered:
        errors.append(f"{display_path}: rendered note does not contain the deterministic date fixture")

    return errors


def validate_templates(root: Path) -> tuple[list[str], int]:
    template_root = root / "templates"
    templates = sorted(template_root.glob("*.md")) if template_root.is_dir() else []
    errors: list[str] = []

    discovered = {template.name for template in templates}
    for name in sorted(TEMPLATE_SCHEMAS.keys() - discovered):
        errors.append(f"templates/{name}: expected template is missing")
    for name in sorted(discovered - TEMPLATE_SCHEMAS.keys()):
        errors.append(f"templates/{name}: no validation schema is registered")

    for template in templates:
        schema = TEMPLATE_SCHEMAS.get(template.name)
        if schema is None:
            continue
        errors.extend(validate_template(template, template.relative_to(root).as_posix(), schema))

    return errors, len(templates)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render reusable templates with deterministic values and validate generated frontmatter."
    )
    parser.add_argument("root", nargs="?", default=".")
    args = parser.parse_args()
    root = Path(args.root).resolve()

    errors, count = validate_templates(root)
    if errors:
        print("RENDERED TEMPLATE VALIDATION FAILED\n")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1

    print(f"Rendered template validation passed: {count} templates rendered and validated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
