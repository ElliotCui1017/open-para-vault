# Metadata Conventions

Metadata exists to support retrieval, dashboards, and automation. Do not add a property unless a workflow uses it.

## Common properties

```yaml
---
type: resource
status: reading
created: 2026-08-14
updated: 2026-08-14
aliases: []
tags:
  - knowledge-management
area: "[[03_Areas/Learning Practice]]"
project: "[[02_Projects/Community Garden Guide]]"
source: https://example.invalid/source
next: Write a three-sentence summary
---
```

| Property | Purpose | Guidance |
| --- | --- | --- |
| `type` | Note role | Required for system notes |
| `status` | Lifecycle state | Required when lifecycle matters |
| `created` | Creation date | `YYYY-MM-DD` |
| `updated` | Meaningful update date | Change when content or state changes |
| `aliases` | Alternate Obsidian names | YAML list |
| `tags` | Stable topics | Small YAML list; avoid status tags |
| `area` | Ongoing responsibility | Quoted wikilink or empty |
| `project` | Outcome-oriented work | Quoted wikilink or empty |
| `source` | Origin of a resource | URL, citation, or empty |
| `next` | Concrete next action | Short text for dashboards |

Quote wikilinks in YAML so parsers treat them as strings:

```yaml
project: "[[02_Projects/Community Garden Guide]]"
```

## Types

- `capture`
- `daily`
- `weekly-review`
- `monthly-review`
- `project`
- `area`
- `resource`
- `wiki`
- `meeting`
- `dashboard`
- `guide`

## Status vocabularies

Use the smallest vocabulary that supports a query.

| Note type | Recommended statuses |
| --- | --- |
| Capture | `inbox`, `processed` |
| Project | `idea`, `active`, `waiting`, `paused`, `blocked`, `done`, `archived` |
| Area | `active`, `inactive`, `archived` |
| Resource | `unread`, `reading`, `processed`, `archived` |
| Wiki | `draft`, `evergreen`, `archived` |
| Meeting/review | `active`, `done` |

## Date and placeholder rules

Finished notes use ISO dates. Templates use Obsidian core placeholders:

```yaml
created: "{{date:YYYY-MM-DD}}"
updated: "{{date:YYYY-MM-DD}}"
```

QuickAdd captures use QuickAdd placeholders such as `{{DATE:YYYY-MM-DD HH:mm}}` and `{{VALUE}}`.

## Template validation

The deterministic validator supports only the core placeholders currently used in `templates/`:

- `{{title}}`;
- `{{date:YYYY-MM-DD}}`;
- `{{date:YYYY-MM}}`;
- `{{time:HH:mm}}`.

It renders fixed fixture values, validates the generated frontmatter, and rejects unresolved placeholders. It is deliberately not a complete Templater engine.

Run it with:

```bash
python scripts/validate_templates.py .
python -m unittest discover -s tests -v
```

## Compatibility rules

- Keep frontmatter at the start of the file.
- Use spaces, not tabs, in YAML.
- Use YAML lists for `tags` and `aliases`.
- Do not store credentials, personal identifiers, or machine paths in properties.
- Do not mass-rewrite a private vault merely to match this schema.
