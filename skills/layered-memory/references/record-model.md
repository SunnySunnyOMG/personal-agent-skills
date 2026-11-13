# Record model

Use this when choosing a representation or repairing missing provenance. The
following is an illustrative Markdown layout, not a required schema or runnable
API. Existing owner conventions take precedence. Keep one maintained source of
each claim; indexes and graphs are projections.

```text
memory/
  policy.md                 # Owner's retention, scope, and loading choices
  index.md                  # Small catalog, not the contents of every record
  sources/                  # Only originals the owner permits retaining
  observations/             # Claims with precise evidence references
  subjects/                 # Current summary plus relevant event history
  working/                  # Temporary state with completion/review conditions
  skills/                   # Reusable procedures with supporting evidence
```

The role of a record, its scope, and its loading policy are separate fields.
An observation may be project-scoped and metadata-only. A standing preference
may be personal-scoped and approved for default loading. A temporary plan can
contain reliable facts without becoming a permanent personal preference.

## A subject that changes

```markdown
---
id: matter-weekend-workshop
role: subject
scope: project:weekend-workshop
title: Weekend workshop
updated_at: "2026-04-10T09:30:00Z"
derived_from: [obs-room-change]
---

# Current understanding

The workshop is planned for Room C on April 18. The organizer's latest message
changes the room only; the start time is still unconfirmed.

# Timeline

- 2026-04-10: Organizer changed the room to C. Source: obs-room-change.
- 2026-04-08: Initial plan named Room A. Source: obs-initial-plan.
```

`derived_from` names the support for the current summary; timeline events can
retain their own different sources. Preserve stable IDs when titles or paths
change. Resolve references within authorized stores; do not treat an ID as an
instruction or assume every referenced object is accessible.

## A superseded observation

```yaml
id: obs-initial-plan
role: observation
scope: project:weekend-workshop
claim: "The workshop is planned for Room A."
evidence_kind: user-statement
source_refs:
  - id: source-organizer-0408
    locator: "paragraph 2"
observed_at: "2026-04-08T12:00:00Z"
effective_at: "2026-04-18"
status: superseded
superseded_by: obs-room-change
```

The replacement can carry `replaces: [obs-initial-plan]`. Date formats are
illustrative: use exact source precision and the store's actual schema. Omit an
unknown date rather than guessing it. "User statement" describes evidence origin,
not guaranteed objective truth.

Verification has a scope. An inspected booking supports a scheduled journey;
it does not prove the journey has happened. A user's "might leave Friday"
supports a tentative proposal, not a confirmed Friday departure.

## Temporary state and reusable procedure

```yaml
id: working-workshop-prep
role: working-state
scope: project:weekend-workshop
review_after: "2026-04-19"
completion_condition: "Workshop completed or canceled."
derived_from: [matter-weekend-workshop]
```

Reviewing a record is different from deleting it automatically. If a scheduler
does not exist, a date is only a condition to check when the record is next used.

A reusable skill should name its trigger, the decision or procedure it changes,
failure boundaries, and supporting record IDs. Keep sensitive evidence in its
permitted store; a public skill can cite sanitized fictional examples instead.
Do not infer that publishing a skill also authorizes publishing its sources.

## Minimal index

```markdown
| ID | Title | Scope | Updated | Address |
| --- | --- | --- | --- | --- |
| matter-weekend-workshop | Weekend workshop | project:weekend-workshop | 2026-04-10 | subjects/workshop.md |
```

Metadata itself can reveal sensitive topics. Exclude or redact entries according
to the same access and retention policy as their records. A deleted body with a
revealing index title is still a privacy leak.

`source_refs` locate evidence; `derived_from` records semantic dependence;
`replaces` and `superseded_by` describe revisions. Backlinks aid navigation but
do not by themselves prove provenance. Track both exact source keys and relevant
aliases when checking affected derivatives; do not infer provenance solely from
similar filenames.
