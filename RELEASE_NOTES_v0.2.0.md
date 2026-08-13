# Open PARA Vault v0.2.0

## Purpose and positioning

Open PARA Vault is now positioned as a privacy-safe toolkit and starter framework for publishing reusable Obsidian knowledge systems without exposing a private vault. The included PARA system remains the ready-to-use reference implementation.

## Major features

- downloadable `open-para-vault-v0.2.0.zip` starter vault;
- no-Git installation path for Obsidian users;
- deterministic standard-library package builder;
- SHA-256 checksum distributed beside the ZIP;
- explicit allowlisting of safe `.obsidian` configuration;
- archive safety, extraction, and reproducibility tests;
- guarded automation that creates a Draft Release or uploads only to a matching tag release;
- cross-platform bootstrap hardening completed through Issue #3;
- deterministic rendered-template validation completed through Issue #1.

## Installation

1. Open the repository's GitHub Releases page.
2. Download `open-para-vault-v0.2.0.zip`.
3. Optionally verify it against `open-para-vault-v0.2.0.zip.sha256`.
4. Extract the archive.
5. In Obsidian, choose **Open folder as vault** and select `open-para-vault-v0.2.0`.

## Deterministic build

Maintainers can reproduce the asset with:

```bash
python scripts/build_starter_vault.py --version v0.2.0 --output dist
```

The builder fixes archive ordering, timestamps, permissions, and storage settings. Identical source and version inputs produce identical ZIP bytes and SHA-256 digests.

## Privacy guarantee

The starter asset is built only from the fictional `examples/demo-vault` tree. It excludes repository Git history, remotes, workspace state, plugin binaries, caches, build output, credential-bearing files, private attachments, and machine-specific paths. Unknown `.obsidian` state fails packaging instead of being silently included.

The maintainer's real private vault remains outside this repository and outside the downloadable asset. The frozen `v0.1.0` tag and release notes are unchanged.

## Known limitations

- Dataview and QuickAdd remain optional plugins and are not bundled;
- the package builder targets the repository's reference starter vault rather than arbitrary private vaults;
- archive validation reduces disclosure risk but does not replace human review;
- release assets remain Draft until a maintainer explicitly publishes the GitHub Release.

## Roadmap

A generic privacy/public-release checker is planned but not implemented. Future work may add a reusable CLI, configurable exclusions, a GitHub Action, and external integrations.
