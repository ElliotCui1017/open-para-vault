# Contributing

Thank you for improving Open PARA Vault.

## Suitable contributions

- clearer setup and workflow documentation;
- portable templates and metadata improvements;
- safer privacy defaults and validation rules;
- generic Dataview queries;
- QuickAdd workflows without personal paths or credentials;
- accessibility, compatibility, and cross-platform fixes;
- fictional demo content that tests a real workflow.

Do not submit real notes, attachments, credentials, contact details, academic or employment records, or copyrighted material you cannot redistribute.

## Development workflow

1. Fork the repository and create a focused branch.
2. Make one coherent change.
3. Use fictional reproduction data.
4. Run:

```bash
python scripts/preflight_public.py .
python scripts/validate_repo.py .
python scripts/validate_templates.py .
python -m unittest discover -s tests -v
```

5. Review the entire diff and new Git history for private data.
6. Open a pull request using the template.

## Style

- Public documentation and examples use English.
- Paths are relative and use `/` in documentation.
- Markdown follows CommonMark where possible; Obsidian extensions are documented.
- YAML uses stable fields from `docs/metadata-conventions.md`.
- Scripts use only the Python standard library unless a dependency is justified.

## Commits

Use conventional prefixes such as `docs:`, `feat:`, `fix:`, `refactor:`, `test:`, and `chore:`. Keep commits small enough to review for privacy and behavior.

## Pull request expectations

Explain the problem, the change, validation performed, compatibility implications, and why the content is safe to publish. A maintainer may request fictionalization or removal even when automated checks pass.
