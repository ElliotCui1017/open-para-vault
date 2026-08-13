---
type: dashboard
status: active
created: 2026-08-14
updated: 2026-08-14
aliases:
  - Demo Home
tags:
  - demo
---

# Open PARA Vault Demo

> [!info]
> Every note and scenario in this vault is fictional. Copy conventions, not demo facts, into a private vault.

## Start here

1. Read [[00_Inbox/Capture Queue]].
2. Follow the example project in [[02_Projects/Community Garden Guide]].
3. Compare the source note [[04_Resources/Knowledge Management]] with the durable note [[05_Wiki/Progressive Summarization]].
4. Read [[06_Archive/README|the archive rule]].

## Active projects

```dataview
TABLE status AS "Status", next AS "Next action", updated AS "Updated"
FROM "02_Projects"
WHERE type = "project" AND status = "active"
SORT updated DESC
```

## Actionable tasks

```dataview
TASK
FROM "01_Daily" OR "02_Projects" OR "03_Areas"
WHERE !completed AND type != "guide" AND type != "dashboard"
SORT file.name ASC
LIMIT 20
```

## Resources in progress

```dataview
TABLE status AS "Status", source AS "Source", updated AS "Updated"
FROM "04_Resources"
WHERE type = "resource" AND status != "archived"
SORT updated DESC
```

## Durable knowledge

```dataview
TABLE status AS "Status", area AS "Area", updated AS "Updated"
FROM "05_Wiki"
WHERE type = "wiki"
SORT updated DESC
```

## Recent reviews

```dataview
LIST
FROM "01_Daily"
WHERE type = "weekly-review" OR type = "monthly-review"
SORT created DESC
LIMIT 5
```
