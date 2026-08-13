# Architecture

Open PARA Vault is a reusable system layer, not a user's live knowledge base.

## Two-repository model

```text
public system repository              private user vault
------------------------              ------------------
templates/                     --->   99_Templates/
config/*.example.json          --->   selected .obsidian settings
examples/demo-vault/           --->   learning and experimentation
docs/                                 real notes and attachments
scripts/                              private Git history
```

The arrow means "copy deliberately," never "synchronize every file." A private vault may consume templates and conventions from this repository, but private notes never flow back automatically.

## Public repository layout

| Path | Responsibility |
| --- | --- |
| `templates/` | Portable Obsidian note templates |
| `config/` | Credential-free configuration examples for optional plugins |
| `examples/demo-vault/` | A self-contained vault with fictional content |
| `docs/` | Architecture, setup, metadata, privacy, and workflows |
| `scripts/` | Bootstrap and publication validators |
| `.github/` | Issue forms, pull request guidance, and CI |

## Vault information architecture

The demo vault uses numbered, underscore-separated folders so they sort consistently across platforms:

| Folder | Purpose |
| --- | --- |
| `00_Inbox` | Unclarified captures |
| `01_Daily` | Daily notes and periodic reviews |
| `02_Projects` | Work with a concrete outcome and end condition |
| `03_Areas` | Ongoing responsibilities without an end date |
| `04_Resources` | Source material and references |
| `05_Wiki` | Durable, reusable knowledge |
| `06_Archive` | Inactive material retained for context |
| `99_Templates` | Templates installed into the vault |

## Information flow

```text
Capture
  -> 00_Inbox
  -> clarify ownership and next action
  -> 02_Projects / 03_Areas / 04_Resources
  -> synthesize durable ideas into 05_Wiki
  -> review from dashboards
  -> 06_Archive when inactive
```

Daily notes are a working surface, not a required permanent source of truth. Useful decisions and knowledge should be promoted to the appropriate project, area, resource, or wiki note.

## Automation boundary

Automations operate on metadata and relative vault paths. They must not depend on a username, drive letter, home directory, private project name, or credential.

Portable:

```text
${VAULT_ROOT}/02_Projects
```

Not portable:

```text
<USER_HOME>/Documents/My Real Vault/02_Projects
```

Dataview is read-only in the provided examples. QuickAdd examples append to a relative inbox file. Templater system commands are disabled in the example configuration.

## Failure model

- Core templates continue to work without community plugins.
- Dataview code blocks remain visible as source when Dataview is unavailable.
- QuickAdd is optional; users can type into the capture queue manually.
- Validation fails closed when it finds a high-risk path, credential pattern, or unsupported private artifact.
