from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validate_templates import (  # noqa: E402
    FIXTURE_VALUES,
    TEMPLATE_SCHEMAS,
    render_template,
    validate_template,
    validate_templates,
)


class RenderedTemplateValidationTests(unittest.TestCase):
    def test_all_repository_templates_render_and_validate(self) -> None:
        errors, count = validate_templates(ROOT)
        self.assertEqual(errors, [])
        self.assertEqual(count, len(TEMPLATE_SCHEMAS))
        self.assertEqual(
            {path.name for path in (ROOT / "templates").glob("*.md")},
            set(TEMPLATE_SCHEMAS),
        )

    def test_rendering_is_deterministic_and_resolves_supported_placeholders(self) -> None:
        source = "# {{title}} on {{date:YYYY-MM-DD}} at {{time:HH:mm}} ({{date:YYYY-MM}})"
        rendered = render_template(source)
        self.assertEqual(
            rendered,
            "# Rendered Template on 2030-01-02 at 03:04 (2030-01)",
        )
        self.assertEqual(FIXTURE_VALUES["title"], "Rendered Template")

    def test_missing_property_error_names_template_and_property(self) -> None:
        source = (ROOT / "templates" / "project.md").read_text(encoding="utf-8")
        damaged = source.replace("type: project\n", "", 1)
        errors = self._validate_temporary("project.md", damaged)
        self.assertIn("templates/project.md: missing required property 'type'", errors)

    def test_unresolved_placeholder_error_names_template(self) -> None:
        source = (ROOT / "templates" / "daily-note.md").read_text(encoding="utf-8")
        damaged = source.replace("# {{date:YYYY-MM-DD}}", "# {{unsupported:value}}", 1)
        errors = self._validate_temporary("daily-note.md", damaged)
        self.assertIn(
            "templates/daily-note.md: generated note contains unresolved placeholder "
            "'{{unsupported:value}}'",
            errors,
        )

    def test_invalid_tags_error_names_property(self) -> None:
        source = (ROOT / "templates" / "wiki.md").read_text(encoding="utf-8")
        damaged = source.replace("tags:\n  - wiki", "tags: wiki", 1)
        errors = self._validate_temporary("wiki.md", damaged)
        self.assertIn("templates/wiki.md: property 'tags' must be a YAML list", errors)

    def test_missing_frontmatter_delimiter_names_template(self) -> None:
        source = (ROOT / "templates" / "meeting.md").read_text(encoding="utf-8")
        damaged = source.replace("\n---\n\n#", "\n\n#", 1)
        errors = self._validate_temporary("meeting.md", damaged)
        self.assertIn(
            "templates/meeting.md: generated frontmatter is missing closing delimiter '---'",
            errors,
        )

    def test_invalid_type_and_status_name_properties(self) -> None:
        source = (ROOT / "templates" / "resource.md").read_text(encoding="utf-8")
        damaged = source.replace("type: resource", "type: project", 1).replace(
            "status: unread", "status: unknown", 1
        )
        errors = self._validate_temporary("resource.md", damaged)
        self.assertIn(
            "templates/resource.md: property 'type' must be 'resource', got 'project'",
            errors,
        )
        self.assertTrue(
            any(error.startswith("templates/resource.md: property 'status' must be one of") for error in errors)
        )

    def test_invalid_calendar_date_is_rejected(self) -> None:
        source = (ROOT / "templates" / "area.md").read_text(encoding="utf-8")
        damaged = source.replace('created: "{{date:YYYY-MM-DD}}"', 'created: "2030-02-30"', 1)
        errors = self._validate_temporary("area.md", damaged)
        self.assertIn("templates/area.md: property 'created' is not a valid calendar date", errors)

    def _validate_temporary(self, name: str, content: str) -> list[str]:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / name
            path.write_text(content, encoding="utf-8")
            return validate_template(path, f"templates/{name}", TEMPLATE_SCHEMAS[name])


if __name__ == "__main__":
    unittest.main()
