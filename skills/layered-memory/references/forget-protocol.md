# Forgetting and privacy withdrawal

Use for an explicit request to remove retained information, including derived
content. Ordinary correction or archive is a different operation. The owner's
request determines the target and scope; existing authorization need not be
asked for again. Clarify only an ambiguity that materially changes what would be
irreversibly erased.

1. **Resolve the target.** Identify the source, matter, passage, or claim from
   stable IDs and source references. Inspect accessible derivation links,
   backlinks, source aliases, and relevant content matches. Filename similarity
   alone is insufficient. Bound the search to authorized stores.
2. **Stop reuse and recreation where supported.** Use real read/write barriers,
   pending-operation holds, or ingestion suppression if the system provides
   them. A prompt instruction alone cannot guarantee concurrent writers stop.
   When no such mechanism exists, state the limitation and coordinate only
   within the tools actually available. Do not claim a store is sealed.
3. **Clear affected derivatives.** Remove the withdrawn material from summaries,
   observations, working state, retained timelines, archived copies, prompts,
   and generated artifacts under control. Recompile mixed records from remaining
   permitted evidence. Delete a derived skill or make it a candidate when its
   only support was withdrawn; keep an abstract rule only when independent
   allowed support remains. Do not preserve a revealing "audit" copy of the
   deleted content.
4. **Remove targeted originals last.** Once their dependent records are cleared,
   remove or redact the originals and duplicate input copies in scope. A source
   can be needed to locate its derivatives, which is why deleting it first is
   unsafe. If a step fails, keep pending state minimal and nonrevealing, prevent
   available reuse, and report the incomplete scope; do not declare success.
5. **Refresh and verify.** Rebuild or invalidate affected search indexes, graph
   entries, metadata catalogs, embeddings, and quick-context caches. Search by
   identifiers and relevant aliases; inspect results for actual remnants and
   unrelated matches. Verify that normal recall no longer returns the withdrawn
   material. When supported, suppress reingestion by a minimal nonrevealing
   source key; reallow it only on the owner's instruction. Do not retain the
   private text inside a suppression entry.
6. **Report the real boundary.** List stores and projections checked, failures,
   and unhandled copies without repeating the private content. Version-control
   history, remote backups, exported files, company stores, provider logs, and
   external conversations may require separate access or a different removal
   procedure. Never claim universal or permanent erasure from a scoped cleanup.

Do not rewrite shared Git history, delete remote backups, contact third parties,
or change retention in other systems merely because a local memory deletion was
requested. If those actions are necessary, make the concrete affected scope and
consequences reviewable and follow the owner's authorization for that action.

## Distinctions to preserve

| Action | Current answer | Ordinary history | Original source |
| --- | --- | --- | --- |
| Correct / supersede | Recompile from better evidence | Keep relevant previous version | Retain if permitted |
| Archive | No longer active by default | Retained, potentially retrievable | Usually retained |
| Expire temporary state | Stop treating it as current | Follow retention policy | Follow retention policy |
| Forget / withdraw | Remove affected claims and derivatives | Remove withdrawn content in scope | Remove/redact targeted source in scope |

Append-only history is an ordinary update convention, not an exemption from
the owner's privacy withdrawal. Conversely, a request to update a plan is not
permission to destroy its history.
