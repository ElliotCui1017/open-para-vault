# Codex Migration Task

Use this prompt from the root of the existing private knowledge-system project.

## Goal

Transform the existing personal knowledge management project into a clean, public, reusable open-source repository suitable for external users and long-term maintenance.

The system currently may contain Obsidian configuration, PARA-style folders, templates, Dataview/QuickAdd automation, Git configuration, scripts, personal notes, machine-specific paths, and private data.

The public repository must expose the reusable system while keeping the maintainer's real private knowledge content out of Git history.

## Required approach

### 1. Audit before editing

Inventory the current tree and classify files into:

- reusable system;
- generic documentation;
- reusable template;
- reusable automation;
- fictional/example content;
- private content;
- credentials/secrets/auth;
- generated/cache;
- machine-specific configuration;
- uncertain.

Write the classification summary to `MIGRATION_AUDIT.md`.

Do not print secret values into the audit. Refer to secret-bearing files by path only.

### 2. Prefer a clean public tree

If the current repository history contains personal notes, credentials, identifying information, or other sensitive content, do not make that history public.

Create a sanitized public tree using an allowlist of reusable components.

The intended public shape is described by the OSS kit and `AGENTS.md`.

### 3. Preserve useful functionality

Where safe, migrate:

- PARA folder conventions;
- reusable Obsidian templates;
- generic Dataview queries;
- generic QuickAdd workflows;
- reusable scripts;
- documentation;
- metadata conventions;
- Git-friendly workflows;
- safe Obsidian settings that improve reproducibility.

Replace personal paths with configuration variables or placeholders.

Replace real examples with fictional examples.

### 4. Improve project quality

Add or improve:

- README;
- architecture documentation;
- setup instructions;
- privacy model;
- metadata documentation;
- CONTRIBUTING;
- SECURITY;
- CODE_OF_CONDUCT;
- CHANGELOG;
- issue templates;
- pull request template;
- roadmap;
- preflight validation;
- appropriate CI.

Use English as the primary public documentation language.

### 5. Validate

Run:

```bash
python scripts/preflight_public.py .
```

Also run any project-specific tests or validators you discover.

Search for:

- tokens;
- passwords;
- API keys;
- private keys;
- `.env`;
- email addresses;
- phone numbers;
- student IDs;
- real addresses;
- Windows user paths;
- macOS user paths;
- Linux home paths;
- personal journal directories;
- private attachments.

Do not assume `.gitignore` is sufficient if sensitive files were previously committed.

### 6. Git hygiene

Create focused commits using conventional prefixes.

Suggested sequence:

1. `chore: establish public repository safety baseline`
2. `refactor: separate reusable knowledge system from private content`
3. `docs: document architecture and setup`
4. `feat: add fictional demo vault and reusable templates`
5. `ci: add public preflight validation`

Do not fabricate a long historical commit trail. Preserve real development history only when it is safe to publish.

### 7. First release readiness

Prepare the project for `v0.1.0`.

Create `RELEASE_NOTES_v0.1.0.md` with:

- project purpose;
- major features;
- installation steps;
- known limitations;
- privacy guarantee;
- roadmap.

Create a small set of genuine GitHub-ready issue descriptions in `docs/initial-issues.md` based on real remaining work.

## Stop conditions

Stop before any public push if:

- the preflight fails;
- secrets are found;
- private content may exist in Git history;
- the target GitHub repository is ambiguous;
- authentication would require exposing credentials.

Report the exact blocker and the safest next command or action.

## Final report

At the end, provide:

- files added/changed/removed;
- private content excluded;
- tests/preflight run and results;
- Git history risk assessment;
- suggested repository name and description;
- suggested GitHub topics;
- whether the tree is ready for a public push;
- remaining blockers for `v0.1.0`.
