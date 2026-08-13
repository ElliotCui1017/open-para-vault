# Migration Audit

Audit date: 2026-08-14

Source: existing private Obsidian vault at the parent repository root

Public destination: this clean allowlisted repository

## Executive decision

The source repository and its Git history are **not safe to publish**. The history contains personal weekly reviews, academic project notes, dashboards linked to private material, and long-lived vault backup commits. The source working tree also contains private content and unrelated uncommitted changes.

This migration therefore uses a clean public tree and a new Git history. No source commit, branch, remote, private note, attachment, plugin bundle, or workspace state is inherited.

## Inventory scope

The source contains 406 files after excluding `.git/`, the supplied OSS kit, and its archive. The high-level inventory is:

- 350 files under the private PARA content directories (`00_Inbox/` through `06_Archive/`);
- 24 note templates under `99_Templates/`;
- 26 Obsidian settings or community-plugin files under `.obsidian/`;
- 49 generated, cache, or temporary extraction files (overlapping the content count above);
- 6 root-level documents or repository files.

The Git history contains 123 currently tracked paths and multiple vault-backup commits. Historical paths include daily/weekly reviews, academic project material, and personal project notes.

## Classification

| Classification | Source paths or file groups | Decision |
| --- | --- | --- |
| Reusable system | PARA folder responsibilities, capture-to-inbox lifecycle, project/area/resource/wiki separation, review cadence, task conventions | Recreate from documented conventions; do not copy the private vault tree wholesale |
| Generic documentation | Safe portions of root `README.md`, `AGENTS.md`, folder usage guides, metadata guidance, and workflow explanations | Rewrite in English without private links or context |
| Reusable template | Generic daily, project, area, resource, meeting, wiki, weekly review, monthly review, and quick-capture patterns in `99_Templates/` | Rebuild with portable placeholders and consistent metadata |
| Reusable automation | Generic Dataview query shapes in dashboards; relative-path QuickAdd captures; Templater template-folder convention | Recreate as documented examples and sanitized configuration; never copy plugin state wholesale |
| Fictional/example content | Supplied OSS kit demo notes | Keep only after validation; expand with clearly fictional content |
| Private content | `00_Inbox/`, `01_Daily/`, real content in `02_Projects/`, `03_Areas/`, `04_Resources/`, `05_Wiki/`, and `06_Archive/`; root `Home.md` links to private context | Exclude completely |
| Credentials/secrets/auth | Auth-capable community-plugin state such as `.obsidian/plugins/quickadd/data.json` and `.obsidian/plugins/obsidian-git/data.json`; any future `.env`, key, token, cookie, or credential file | Exclude; reconstruct only credential-free examples. No secret values are recorded in this audit |
| Generated/cache | `.git/`, `_tutorial_extract_tmp/`, `.DS_Store`, notebook checkpoints, plugin `main.js`/`styles.css`, extracted datasets, compiled or downloaded artifacts, and the OSS kit archive | Exclude |
| Machine-specific configuration | `.obsidian/workspace.json`, `.obsidian/graph.json`, hotkeys and local UI state, Obsidian Git state, shell paths, plugin install artifacts | Exclude; publish a minimal safe `.obsidian/` example only |
| Uncertain | `SYSTEMPROMPT.md`, `LLMMEMORIES.md`, course-specific templates, source/plugin data not explicitly allowlisted, and any file whose ownership or privacy cannot be proven | Exclude pending human review |

## Sensitive-data scan summary

The current-tree scan checked secret/token/private-key patterns, `.env`-style filenames, email-like strings, phone-like strings, student-identifier language, absolute user paths, journal/private directory names, and attachment indicators.

- No credential value is reproduced here.
- Several source files produced privacy/PII-like matches and remain excluded.
- Minified third-party plugin bundles produced secret-pattern false positives and remain excluded as vendored/generated code.
- The supplied OSS kit passed its configured public preflight before migration.
- No Windows, macOS, or Linux user-home path match was found in the scanned Git history, but private knowledge content is present in that history.

## Allowlist for the public tree

Only these classes may enter this repository:

- public project governance and documentation;
- portable validation scripts and CI;
- generic templates;
- sanitized Dataview and QuickAdd examples;
- a minimal, safe Obsidian configuration example;
- fictional demo-vault notes and empty folder keepers;
- release and contribution materials.

Everything else is denied by default.

## Git history risk assessment

Risk: **high / confirmed unsuitable for publication**.

The parent repository history contains private note paths and content categories. `.gitignore` cannot mitigate that historical exposure. The safe publication path is to publish only this directory as a new repository with its own initial commits. Do not attach the parent repository's remote or copy its `.git/` directory.

## Stop conditions

A public push must not occur unless all of the following are true:

1. `python scripts/preflight_public.py .` passes in this repository.
2. Project-specific validators pass.
3. A human reviews the complete new Git history and staged diff.
4. The intended GitHub repository and owner are explicitly confirmed.
5. No credential or authentication material is required for review.
