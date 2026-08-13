# Changelog

All notable changes are documented here. The format follows Keep a Changelog, and versions follow semantic versioning.

## [Unreleased]

### Added

- deterministic rendering and generated-frontmatter validation for every reusable template;
- Windows, macOS, and Linux CI coverage for rendered-template validation;
- Windows and Linux CI coverage for bootstrap success and safety boundaries;
- a stable required CI gate for branch protection;
- complete bootstrap allowlisting for repository validation and tests, with generated caches excluded;
- deterministic downloadable starter-vault ZIP and SHA-256 checksum generation;
- strict package allowlisting for safe Obsidian configuration;
- package extraction, safety, and reproducibility validation;
- tag-triggered Draft Release asset automation with minimal write permissions.

### Changed

- positioned PARA as the reference implementation within broader privacy-safe Obsidian publishing tooling;
- added a no-Git onboarding path for release downloads.

### Planned

- generic privacy/public-release checker and reusable CLI;
- configurable exclusions and a future GitHub Action.

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
