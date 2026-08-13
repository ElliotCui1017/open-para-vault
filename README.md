# Open PARA Vault

A privacy-first, local-first starter system for Obsidian. It combines a PARA-inspired folder structure, reusable templates, consistent metadata, optional Dataview and QuickAdd workflows, publication checks, and Git-friendly defaults.

The repository is the reusable **system layer**. Your real notes remain in a separate private vault.

## What is included

- an eight-folder vault convention from inbox to archive;
- project, area, resource, wiki, meeting, daily, and review templates;
- fictional notes demonstrating a complete capture-to-archive workflow;
- generic Dataview dashboards;
- portable QuickAdd and Templater configuration examples;
- a minimal safe Obsidian configuration;
- privacy preflight, structural validation, and CI;
- migration and contributor guidance.

## Quick start

### Explore the demo

1. Install Obsidian.
2. Clone or download this repository.
3. In Obsidian, choose **Open folder as vault**.
4. Select `examples/demo-vault`.
5. Open `Home.md`.

The demo works with Obsidian core features. Dataview and QuickAdd sections are optional enhancements.

### Add the system to an existing private vault

1. Back up the vault.
2. Read [the privacy model](docs/privacy-model.md).
3. Copy selected files from `templates/` into your vault's template folder.
4. Merge, rather than overwrite, the safe settings described in [setup](docs/setup.md).
5. Keep the private vault outside this public repository.

Never copy your private vault into this repository to "try the system."

## Repository map

```text
.
|-- .github/                 contribution templates and CI
|-- codex/                   reusable migration prompt
|-- config/                  optional plugin configuration examples
|-- docs/                    architecture, setup, privacy, conventions
|-- examples/demo-vault/     fictional self-contained Obsidian vault
|-- scripts/                 bootstrap and validation
|-- tests/                   standard-library validation tests
|-- templates/               portable note templates
|-- MIGRATION_AUDIT.md       source migration risk record
`-- RELEASE_NOTES_v0.1.0.md  first-release notes
```

## Core workflow

```text
capture -> inbox -> clarify -> project/area/resource -> wiki -> review -> archive
```

See [workflow](docs/workflow.md) for the decision rules and a complete fictional example.

## Optional plugins

- **Dataview** renders the dashboard query blocks.
- **QuickAdd** provides keyboard-driven capture into the inbox.
- **Templater** can extend templates, but the included templates use portable core placeholders.
- **Obsidian Git** can back up a private vault; its plugin state and credentials do not belong here.

Install community plugins from Obsidian's own interface. This repository does not vendor plugin code.

## Validate before publication

From the repository root:

```bash
python scripts/preflight_public.py .
python scripts/validate_repo.py .
python scripts/validate_templates.py .
python -m unittest discover -s tests -v
```

The checks reduce risk; they do not replace human review of the full Git history.

## Privacy promise

The public tree is built from an allowlist and has a new Git history. The maintainer's source vault, history, journals, academic material, health or financial notes, attachments, credentials, and machine state are excluded. See [MIGRATION_AUDIT.md](MIGRATION_AUDIT.md) for the migration decision.

## Project status

The public repository and CI are established, and the tree is prepared for the `v0.1.0` preview. The release tag and GitHub Release remain pending explicit maintainer approval. See [release notes](RELEASE_NOTES_v0.1.0.md) and [roadmap](ROADMAP.md).

## Contributing and security

Read [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Never attach real vault content to an issue or pull request.

## License

MIT. See [LICENSE](LICENSE).
