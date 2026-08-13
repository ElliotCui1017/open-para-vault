# Optional Automation

The system is useful without community plugins. Add automation only after the manual workflow makes sense.

## Dataview

The demo Home note contains generic queries for active projects, actionable tasks, recent resources, and weekly reviews. Queries depend on the folders and properties documented in [metadata conventions](metadata-conventions.md).

Example:

````markdown
```dataview
TABLE status, next, updated
FROM "02_Projects"
WHERE type = "project" AND status = "active"
SORT updated DESC
```
````

The examples use read-only Dataview query language. Dataview JavaScript is not required.

## QuickAdd

`config/quickadd.example.json` defines portable captures that append to `00_Inbox/Capture Queue.md` using relative paths.

Safe installation:

1. back up the private vault;
2. install QuickAdd through Obsidian;
3. close Obsidian before editing plugin data;
4. compare the example with the vault's existing QuickAdd configuration;
5. recreate or merge individual choices instead of overwriting the whole file;
6. leave AI provider credentials unset;
7. reopen Obsidian and test with fictional text.

QuickAdd's internal schema may change. Prefer recreating the documented choices through its UI if the example does not match the installed plugin.

## Templater

`config/templater.example.json` points to `99_Templates` and keeps system commands disabled. The supplied templates use core Obsidian placeholders, so Templater is optional.

Do not enable arbitrary shell commands merely to use this repository.

## Obsidian Git

Obsidian Git can version a private vault, but that private history must remain private. Do not copy its plugin data, authentication helpers, remote URL, or bundled plugin code into a public repository.

## Automation design rules

- use relative paths;
- fail safely when a folder or setting is missing;
- append rather than overwrite captures;
- keep credentials in the application's secret store, never configuration examples;
- make every automated result discoverable and reversible;
- test with fictional content before using a real vault.
