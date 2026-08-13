# Setup

## Requirements

- Obsidian for using the vault;
- Git for cloning and versioning the public system;
- Python 3 for publication validation;
- PowerShell only if you use the optional bootstrap helper.

Dataview, QuickAdd, Templater, and Obsidian Git are optional community plugins.

## Option 1: open the fictional demo vault

1. Clone or download the repository.
2. Open Obsidian.
3. Select **Open folder as vault**.
4. Choose `examples/demo-vault`.
5. Start at `Home.md`.

The included `.obsidian` files enable only safe, reproducible core settings. Workspace state and plugin binaries are intentionally absent.

## Option 2: install into a private vault

Set a local variable to the private vault root. Do not write its real path into committed files.

macOS or Linux:

```bash
export VAULT_ROOT="/path/to/private-vault"
cp templates/*.md "$VAULT_ROOT/99_Templates/"
```

PowerShell:

```powershell
$VaultRoot = "C:\path\to\private-vault"
Copy-Item templates\*.md "$VaultRoot\99_Templates\"
```

Then configure Obsidian:

1. Set the core Templates folder to `99_Templates`.
2. Set the Daily Notes folder to `01_Daily`.
3. Set the Daily Notes template to `99_Templates/daily-note`.
4. If using Dataview, enable JavaScript queries only when a trusted query requires them; the examples here do not.
5. If using QuickAdd or Templater, follow [automation setup](automation.md) and merge only the settings you need.

## Option 3: create a clean public derivative

Run the allowlisted bootstrap from PowerShell with an empty destination outside this repository:

```powershell
.\scripts\bootstrap_public_repo.ps1 -Destination "C:\path\to\new-public-repo"
```

The script initializes a new `main` branch and runs preflight. It does not configure a remote or publish anything.

## Recommended private-vault layout

```text
00_Inbox/
01_Daily/
02_Projects/
03_Areas/
04_Resources/
05_Wiki/
06_Archive/
99_Templates/
```

Create only the folders your workflow needs. Folder names are conventions, not a database schema.

## Updating

Treat updates as a reviewed merge:

1. inspect changes in this repository;
2. compare templates and configuration with your private copies;
3. apply deliberate changes;
4. preserve private customizations;
5. test links, template insertion, and queries in a disposable vault first.

Do not automate bidirectional synchronization between the public system and private content.

## Troubleshooting

- Raw `dataview` blocks are visible: install and enable Dataview, or use the notes without dashboards.
- A QuickAdd command is missing: recreate the choices from `config/quickadd.example.json` or merge that file carefully.
- Dates remain as placeholders: confirm the file was inserted through Obsidian Templates, not copied as a finished note.
- Preflight reports a path or string: remove or fictionalize it; do not add broad exceptions for real private data.
