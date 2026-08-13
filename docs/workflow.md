# Workflow

## 1. Capture without classifying

Put incomplete input in `00_Inbox/Capture Queue.md`. Capture only enough context to make the item understandable later.

Example:

```markdown
## 2026-08-14 09:00 Quick capture

type:: quick-capture
status:: inbox

Draft a one-page watering guide for the fictional community garden project.
```

## 2. Clarify

During inbox review, ask:

1. Is an action required?
2. Does it have a concrete outcome and finish line?
3. Is it an ongoing responsibility?
4. Is it source material or a durable idea?

Use the answers to route the item:

| Answer | Destination |
| --- | --- |
| Concrete outcome | `02_Projects` |
| Ongoing standard | `03_Areas` |
| Source or reference | `04_Resources` |
| Durable reusable idea | `05_Wiki` |
| No current value, retained for context | `06_Archive` |

## 3. Define the next action

A project is active only when the next physical or digital action is visible. Prefer "draft the three section headings" over "work on guide."

Tasks use standard Markdown checkboxes:

```markdown
- [ ] Draft the three section headings.
```

The `next` property is a short summary for dashboards; the checkbox is the executable record.

## 4. Connect source and synthesis

Keep source notes in `04_Resources`. Create a `05_Wiki` note when an idea is useful beyond the source or project. Link both directions with Obsidian wikilinks.

```markdown
Related: [[04_Resources/Knowledge Management]]
```

## 5. Review

- Daily: choose a focus and record transient context.
- Weekly: review active projects, areas, inbox, and blocked work.
- Monthly: reconsider outcomes, standards, and inactive material.

Reviews generate changes in system notes. They should not become isolated journals that dashboards cannot act on.

## 6. Archive deliberately

Archive when a project is completed, cancelled, or no longer active. Preserve enough context to explain the outcome and maintain links. Moving or deleting notes in a real vault should be a deliberate user action.

## Complete fictional path

1. A watering-guide idea enters `00_Inbox/Capture Queue.md`.
2. It becomes `02_Projects/Community Garden Guide.md` because it has a deliverable.
3. Research is summarized in `04_Resources/Knowledge Management.md` as a demonstration source.
4. A reusable method is written as `05_Wiki/Progressive Summarization.md`.
5. The project dashboard displays its active task.
6. When the guide is finished, its status changes to `done`; the user may later move it to `06_Archive`.

All names and events in the demo are fictional.
