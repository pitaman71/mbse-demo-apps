# Guide for AI agents

Demo applications for the mbse repositories, one directory per app and language (`python/WorkTracker`). Each app's
schemas are a module-scope `install(txn)`, written out in the builders' fluent syntax (mbse-basis P-019), and its seed
data a transaction of its own.

## Invariants

- **Use mbse-schemas as it stands.** An app models what it needs with what mbse-schemas offers; a gap found is reported
  to the user, not worked around in the app.
- **Siblings are checkouts beside this repository**, pinned by commit in `siblings.json`. Other agents may be working in
  them: never edit a sibling from here.
- **Every element an app's UI browses has a reference**: owned by a singleton directory, keyed by an ID its naming
  pattern generates, or a singleton itself (VISUALIZATION.md, FEA-003).
- **Tests run with pytest** from the app's directory: `uv sync && uv run pytest`. Use uv, never pip.
