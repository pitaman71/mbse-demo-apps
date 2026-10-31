# Guide for AI agents

Demo applications for the mbse repositories, one package per app under `mbse.Demos.Apps`, laid out as every mbse repository is (`python3/mbse/Demos/Apps/WorkTracker`). Each app's
schemas are a module-scope `install(txn)`, written out in the builders' fluent syntax (mbse-basis [PRI-019: fluent builder syntax](../mbse-basis/docs/PRINCIPLES.md#PRI-019)), and its seed
data a transaction of its own.

## Invariants

The conventions every mbse repository shares are stated once in mbse-basis; this file cites them and keeps
only what differs here.

- **Vocabulary**: [VOC-007: property](../mbse-basis/docs/VOCABULARY.md#VOC-007) and [VOC-026: schema](../mbse-basis/docs/VOCABULARY.md#VOC-026) for schema-governed things, qualified with whose it is where
  it meets a language's own term ([the vocabulary](../mbse-basis/docs/VOCABULARY.md), its introduction).
- **Models as data** are written in the builders' fluent syntax ([PRI-019: fluent builder syntax](../mbse-basis/docs/PRINCIPLES.md#PRI-019)); packages are laid out and
  capitalized alike ([PRI-030: one package layout](../mbse-basis/docs/PRINCIPLES.md#PRI-030)).
- **Documents**: navigation lines, the README opening with why, and what this file holds ([Rules for every document](../mbse-basis/docs/README.md#rules-for-every-document)).
- **Work**: [PRI-029: parallel work in polyrepo workspaces](../mbse-basis/docs/PRINCIPLES.md#PRI-029), so a sibling is changed only through a workspace that edits it, never from this
  checkout; [PRI-031: the version is the contract](../mbse-basis/docs/PRINCIPLES.md#PRI-031); [PRI-032: a sibling's gap is reported, not worked around](../mbse-basis/docs/PRINCIPLES.md#PRI-032): an app models what it needs with what mbse-schemas offers; and [PRI-033: work lands by branch and pull request](../mbse-basis/docs/PRINCIPLES.md#PRI-033).
- **What this repository builds is specified in mbse-basis' features and capabilities**, cited by ID; where one is
  silent, decide and record it as the basis says ([Detail files](../mbse-basis/docs/README.md#detail-files)).
- **Siblings are checkouts beside this repository**, pinned by version and commit in `siblings.json`
  (`python3 ../mbse-basis/scripts/polyrepo.py pin`).
- **Every element an app's UI browses has a reference**: owned by a singleton directory, keyed by an ID its naming
  pattern generates, or a singleton itself. Logical views designate every object by its reference, and only singletons
  and owned objects have one (mbse-basis [FEA-003: no-code logical views](../mbse-basis/docs/features/FEA-003.md)).
- **Tests run with pytest** from `python3/`: `uv sync && uv run pytest`. Use uv, never pip.
- **mbse-rest tests and builds its golden corpus over the WorkTracker** (`Schemas.install`, `Seed.seed`), pinned in
  its `siblings.json`: a change to the WorkTracker's schemas or seed changes mbse-rest's corpus, so land it with a
  new pin and a regenerated corpus there.
- Never write to `~/.claude/projects/*/memory/` or any hidden memory: what is worth keeping goes in the repository.
