# AGENTS.md

## Mission

This repository is a public, reusable personal knowledge management framework.

When modifying it, optimize for:

1. privacy and secret safety;
2. reproducibility for a new user;
3. clear separation between reusable system components and private user content;
4. small, reviewable changes;
5. understandable documentation;
6. cross-platform paths where possible.

## Hard safety rules

- Never commit `.env` files, API keys, access tokens, cookies, passwords, SSH keys, private certificates, or auth caches.
- Never commit the user's real private vault, journals, personal contacts, academic records, employment records, medical information, financial information, or private attachments.
- Never copy absolute user-specific paths into public examples. Convert them to placeholders such as `${VAULT_ROOT}` or `<USER_HOME>`.
- Never preserve real names, phone numbers, email addresses, student IDs, addresses, account IDs, or other identifying content in example notes.
- If uncertain whether a file is safe to publish, exclude it and report it for human review.
- Before any push, run the public preflight checks.

## Migration strategy

When migrating an existing private vault:

1. inventory the repository and classify each file as:
   - reusable system;
   - generic documentation;
   - fictional/example content;
   - private content;
   - secret/config credential;
   - generated/cache;
   - uncertain.
2. copy only reusable system, generic documentation, and sanitized fictional/example content into the public tree;
3. rewrite machine-specific paths into variables or documented placeholders;
4. add missing documentation around non-obvious automation;
5. run the preflight scripts;
6. run any project tests;
7. review `git diff --cached` before commit;
8. create focused commits with conventional messages.

## Preferred public architecture

- `templates/`: reusable note templates.
- `scripts/`: automation and validation.
- `docs/`: architecture, setup, conventions, privacy.
- `examples/demo-vault/`: fictional safe demonstration content.
- `.github/`: contribution and CI configuration.
- private content should live outside this repository.

## Commit style

Prefer:

- `docs: ...`
- `feat: ...`
- `fix: ...`
- `refactor: ...`
- `chore: ...`
- `test: ...`

Avoid bundling unrelated changes in a single commit.

## Release expectations

A public release should have:

- working README;
- installation instructions;
- license;
- contribution guidance;
- privacy/security guidance;
- changelog;
- at least one reproducible example workflow;
- no secret-scan/preflight failures;
- a tagged version following semantic versioning.
