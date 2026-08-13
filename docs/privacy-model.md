# Privacy Model

## Guarantee

This repository contains a reusable knowledge-management system and fictional demonstrations. It does not contain, require, or derive its usefulness from the maintainer's real vault.

The guarantee is scoped to the public tree and its new Git history. It does not make the separate source vault safe to publish.

## Publish by allowlist

When adapting a private vault:

1. create a new empty repository;
2. define the permitted system files;
3. recreate or copy only those files;
4. replace real examples with fictional ones;
5. run preflight and structural validation;
6. inspect the complete new history before adding a public remote.

Starting with the private vault and relying on `.gitignore` is unsafe because ignored files may already exist in history.

## Data classification

| Class | Examples | Public policy |
| --- | --- | --- |
| System | folder conventions, metadata, generic queries | Allowed after review |
| Documentation | setup and architecture | Allowed after review |
| Fictional demo | invented projects and notes | Allowed |
| Private knowledge | journals, real projects, contacts, study or work records | Denied |
| Authentication | tokens, cookies, keys, OAuth state | Denied |
| Local state | workspaces, caches, plugin data, absolute paths | Denied unless rebuilt as a minimal example |
| Uncertain | files whose ownership or sensitivity is unclear | Denied pending human review |

## High-risk content

Never publish real:

- names, contact details, addresses, account identifiers, or location history;
- health, financial, legal, employment, or academic records;
- calendars, messages, browser profiles, chat exports, or private attachments;
- API credentials, authentication caches, private certificates, or environment files;
- screenshots that expose accounts, notifications, file paths, or private note titles.

## Configuration policy

The repository publishes example configuration outside live plugin state wherever practical. Example files:

- contain only relative paths;
- keep credential fields absent or empty;
- disable shell/system-command execution;
- do not include plugin binaries;
- document that users should merge settings instead of overwriting an existing vault blindly.

## Git history response

If private data or a credential is committed:

1. stop publication;
2. rotate any exposed credential immediately;
3. remove the data from the current tree;
4. rewrite affected public history or create another clean repository;
5. rerun all validators;
6. review before pushing again.

Deleting a file in a later commit is not remediation for data retained in earlier commits.
