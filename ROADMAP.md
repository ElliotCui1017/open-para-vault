# Roadmap

Open PARA Vault is evolving from a single starter system into privacy-safe tooling for publishing reusable Obsidian knowledge systems. PARA remains the reference implementation, not the only long-term use case.

## Completed

- [x] privacy-first public repository and clean Git history;
- [x] metadata and maintainer-identity privacy guards;
- [x] deterministic rendered-template validation;
- [x] cross-platform bootstrap behavior and source-boundary testing;
- [x] frozen `v0.1.0` public preview.

## Current: v0.2.0

- [x] deterministic downloadable starter-vault builder;
- [x] explicit safe Obsidian configuration allowlist;
- [x] package safety, extraction, and reproducibility tests;
- [x] guarded Draft Release asset workflow;
- [ ] maintainer review and publish of the `v0.2.0` release.

## Next: generic privacy and public-release checker

The next major tooling direction is a reusable checker with an interface such as:

```bash
python scripts/check_vault.py /path/to/vault
```

This checker is planned, not implemented. Likely follow-up work includes configurable exclusions, a reusable CLI, a GitHub Action, and external integrations.

## Lower-priority reference implementation work

- compatibility feedback for optional Obsidian plugins;
- safe customization overlays for private vaults;
- additional dashboard and review recipes.

## Non-goals

- hosting or synchronizing users' private notes;
- bundling community-plugin binaries;
- requiring cloud AI or a particular sync provider;
- replacing deliberate privacy review with a scanner.
