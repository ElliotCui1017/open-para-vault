# Changelog

All notable changes are documented here. The format follows Keep a Changelog, and versions follow semantic versioning.

## [Unreleased]

### Added

- deterministic rendering and generated-frontmatter validation for every reusable template;
- Windows, macOS, and Linux CI coverage for rendered-template validation;
- Windows and Linux CI coverage for bootstrap success and safety boundaries;
- a stable required CI gate for branch protection;
- complete bootstrap allowlisting for repository validation and tests, with generated caches excluded.

### Planned

- compatibility feedback from the first public preview;
- maintainer-selected improvements tracked in GitHub Issues.

## [0.1.0] - 2026-08-14

### Added

- privacy-first public repository with a clean Git history;
- migration audit and explicit system/content separation;
- PARA-inspired folder and metadata conventions;
- reusable Obsidian templates;
- fictional demo vault with Dataview dashboards;
- portable QuickAdd and Templater examples;
- setup, architecture, workflow, privacy, and release documentation;
- public preflight, structural validation, and GitHub Actions CI;
- contribution, security, conduct, issue, and pull request guidance.

### Security

- excluded the maintainer's private vault, source history, plugin bundles, credentials, local state, and machine-specific paths;
- added deny-by-default validation for common credential, identifier, user-path, and private-artifact patterns;
- required the maintainer's Git author and committer metadata to use a public noreply identity.
