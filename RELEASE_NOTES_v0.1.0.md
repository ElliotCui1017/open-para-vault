# Open PARA Vault v0.1.0

## Purpose

Open PARA Vault is a privacy-first Obsidian starter system that separates reusable knowledge-management infrastructure from personal content. It helps users capture, organize, review, and retain notes without requiring them to publish a real vault.

## Major features

- PARA-inspired inbox, projects, areas, resources, wiki, and archive structure;
- consistent YAML metadata and Obsidian wikilinks;
- reusable templates for common note and review types;
- a fictional demo vault with generic Dataview dashboards;
- portable QuickAdd and Templater examples;
- safe Obsidian core settings without plugin binaries or workspace state;
- bootstrap, privacy preflight, structural validation, and CI;
- complete architecture, setup, workflow, privacy, and contribution documentation.

## Installation

1. Clone or download the repository.
2. Open `examples/demo-vault` as an Obsidian vault.
3. Start with `Home.md`.
4. Optionally install Dataview or QuickAdd through Obsidian.
5. To use the system privately, copy selected templates and conventions into a separate private vault; do not put real notes in the public repository.

Detailed instructions are in `docs/setup.md`.

## Known limitations

- optional plugin configuration is documented and validated as JSON but not exercised against every plugin release;
- the preflight uses conservative pattern matching and cannot prove that prose is fictional;
- bootstrap behavior has not yet been exercised by a cross-platform CI matrix;
- the demo contains no screenshots or binary attachments by design;
- updating an existing private vault is a manual, reviewed merge.

## Privacy guarantee

The release tree was created with an allowlist and a new Git history. It excludes the maintainer's real vault, private source history, journals, projects, study material, health and financial notes, attachments, credentials, plugin binaries, and machine state. The guarantee applies to this repository tree and history, not to the separate source vault.

Automated scans supplement, but do not replace, human review.

## Roadmap

Next priorities are rendered-template validation, QuickAdd compatibility testing, cross-platform bootstrap CI, and a generated starter-vault release artifact. See `ROADMAP.md` and `docs/initial-issues.md`.
