# Safety gates

Every action that changes the live profile passes through one of these gates. Gates are not skippable.

---

## Gate types

### Gate A — Per-section push gate

Fires before any single-section push (vanity URL, headline, About, banner, an Experience entry, the skills overhaul, a Featured tile).

Format:
> Section: **{section name}**
> Current: `{current value, truncated to 60 chars}`
> Proposed: `{proposed value, truncated to 60 chars}`
>
> This will [overwrite the current value | replace the current entry | add a new entry | delete the current entry].
>
> Push it? Type `push it`, `show me again`, `skip`, or `abort`.

Wait for user input. Accept only those four words (and minor variants).

### Gate B — Destructive action gate

Fires before any delete (a skill, an Experience entry, a Featured tile).

Format:
> ⚠️  About to delete: **{name of thing}**.
>
> This can be re-added later, but the deletion itself is immediate.
>
> Confirm by typing `delete it`, or type `keep` to skip.

Wait for explicit confirmation.

### Gate C — Bulk action gate

Fires before bulk operations (skills overhaul — multiple deletes and adds).

Format:
> This is the skills overhaul. About to:
> - Delete {N} skills: {comma-separated list, truncated to first 5 + "... and N more"}
> - Add {M} skills: {comma-separated list, truncated to first 5 + "... and M more"}
> - Re-order top 5 to: {comma-separated list}
>
> Total operations: {N+M+1}. Estimated time: {2 minutes per delete + 1 minute per add + 1 minute for reorder}.
>
> Run the bulk overhaul? Type `run it`, `let me see the full list`, `do deletes only`, `do adds only`, or `skip`.

Wait for input. Don't accept anything else.

### Gate D — Network-wide notify gate

Fires once, before Phase 6 starts, if the "Share profile updates with network" setting is On.

Format:
> Your "Share profile updates with your network" setting is currently **On**.
>
> If I touch your profile now, every change will buzz your connections. That's noisy and looks scripted.
>
> I recommend turning it Off for the duration of this session. I'll restore it at the end if you want.
>
> Choose:
> - `turn off` — I disable it now, you decide later if you want it back on
> - `keep on` — you take the noise tradeoff knowingly
> - `abort` — stop the whole flow

If the user picks `turn off`, the skill flips "Share profile updates" Off for the session and **remembers the original value** (read from the Phase 2 snapshot under `privacy_settings`). The original value is restored automatically when the session ends or is aborted — see "Restore notify-network on abort/end" below. Log the toggle:

```
{"action":"set_privacy_setting","target":"share_profile_updates","status":"ok","details":"forced Off for session; original was '<On|Off>'"}
```

---

## Pre-execution preamble checks

These run as a sequence before any Phase 6 gate. If any fails, abort with the relevant message.

### Check P1 — Snapshot exists

```
Glob: snapshots/*-*.json (most recent matching {handle})
If empty: "Phase 2 snapshot is missing. I won't push live changes without a backup. Re-run Phase 2 by typing `restart from phase 2`."
```

### Check P2 — Rewrite pack exists with at least one accepted section

```
Read snapshots/{handle}-{timestamp}-rewrite-pack.md
Count sections marked "accepted"
If 0: "The rewrite pack has nothing approved. Run Phase 5 again."
```

### Check P3 — Notify-network setting is Off

```
Chrome MCP: navigate to settings/visibility
Read the "Share profile updates" value
If On: trigger Gate D
If Off: proceed silently
```

### Check P4 — User has typed `proceed`

After P1-P3, output the pre-execution summary and wait for the user to type `proceed`. Accept only that word (or close equivalents: `go`, `let's go`, `start`, `execute`).

### Check P5 — Audit log file ready

```
Touch snapshots/{handle}-{timestamp}-audit-log.jsonl
If write fails: "Can't write the audit log. Check disk space and permissions. I won't continue without it."
```

---

## Per-action safety gates by section

### Vanity URL
- Gate A before set
- No Gate B (no delete)
- No Gate C

### Headline
- Gate A before set
- No destructive

### About
- Gate A before set
- No destructive

### Banner
- Gate A before upload
- File upload requires user to have attached the rendered banner to chat (per Pattern 8 in `chrome-driver.md`)

### Experience entries
- Gate A per entry
- Gate B if rewrite pack marked an entry as "delete this entry" (rare)

### Skills section
- Gate C before the bulk overhaul
- After Gate C, run drops → adds → pin in sequence
- No per-skill gate during the bulk operation (would be 30+ confirmations)
- Final summary after the overhaul: "Done. {N} skills are now on your profile. Top 5 pinned to: ..."

### Featured tiles
- Gate A per tile

---

## Abort, undo, resume behavior

### `abort` at any gate
- Stop immediately
- Do not push the current action
- **Restore the notify-network setting.** If "Share profile updates" was forced Off earlier this session, read the original value from the Phase 2 snapshot (`privacy_settings.share_profile_updates`) and set it back to that value via the Chrome MCP before you stop. If it was originally On, turn it back On; if it was already Off, leave it Off. Then write an audit line for the restore:
  ```
  {"action":"restore_privacy_setting","target":"share_profile_updates","status":"ok","details":"restored to original '<On|Off>' on abort"}
  ```
  If the restore push itself fails, log `"status":"fail"` and tell the user the one setting they should flip back by hand.
- Append `{"action":"abort","at_step":"<step name>","by":"user"}` to the audit log
- Leave the session lock in place so the user can resume later
- Tell the user: "Stopped at {step}. Your 'Share profile updates' setting has been put back the way it was. Type `resume` next time to pick up."

### Restore notify-network on abort/end
- The notify-network toggle is **always** returned to its original value when the session stops — whether that's a clean finish, an `abort`, or the user walking away after the last section.
- The "original value" is whatever Phase 2 captured in the snapshot under `privacy_settings.share_profile_updates`. That snapshot is the single source of truth; never guess.
- The restore runs exactly once. Before restoring, check the audit log for an existing `restore_privacy_setting` line so a resume-then-abort sequence doesn't double-toggle.
- Every restore (success or failure) gets its own audit line, as shown above. This guarantees the user never ends a session with their network-notify setting silently left in the state the skill forced.

### `undo` after a single push
- Only valid for the most recent change (one undo, not a full history walk)
- Implementation: take the previous value from the snapshot, push it back via Chrome MCP using the same Gate A approval pattern, with the "current" and "proposed" reversed
- Surface: "Undoing the {section} change. Reverting to: '{previous value}'. Confirm with `revert`."

### `resume` at session start
- Detect via the presence of `snapshots/.session-lock`
- Read the audit log to find the last successful action
- Skip phases that completed
- Resume from the first unfinished section

---

## Audit log schema

Every action appends a single-line JSON object to `snapshots/{handle}-{timestamp}-audit-log.jsonl`.

```json
{"timestamp":"2026-05-28T15:23:00Z","action":"set_headline","target":"headline_field","status":"ok","details":"set to 130 chars","value_hash":"sha256:abcd..."}
```

Fields:
- `timestamp` — ISO 8601, UTC
- `action` — verb_noun, snake_case (e.g. `delete_skill`, `set_vanity_url`)
- `target` — what was changed (e.g. `skill:Microsoft Excel`, `experience:Acme Corp`)
- `status` — `ok` | `fail` | `skipped` | `abort`
- `details` — free text, optional
- `value_hash` — sha256 of the new value (for sensitive fields; lets the user verify integrity without re-reading from disk)

The audit log is never deleted. Even after the session lock is removed, the log stays for future audit.

---

## What never bypasses a gate

The following can never happen without an explicit user confirmation, no matter what:

1. Deleting any item from the live profile
2. Uploading any file
3. Changing the vanity URL
4. Turning any privacy setting On
5. Sending any message
6. Following any account
7. Liking, sharing, or commenting on any post
8. Sending a connection request
9. Updating any setting outside the profile-editing scope

If a sub-skill or future feature requests one of these without a user gate, refuse and surface the request to the user as a separate confirmation.
