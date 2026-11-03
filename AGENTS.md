# Guide for AI agents

Demo applications for the mbse repositories, one package per app under `mbse.Demos.Apps` (`python3/mbse/Demos/Apps/WorkTracker`, mbse-basis [PRI-030: one package layout](https://github.com/pitaman71/mbse-basis/blob/main/docs/PRINCIPLES.md#PRI-030)). Each app's
schemas are a module-scope `install(txn)` ([PRI-019: fluent builder syntax](https://github.com/pitaman71/mbse-basis/blob/main/docs/PRINCIPLES.md#PRI-019)), and its seed data a transaction of its own.

## Read before any work

Agents must read these mbse-basis documents before doing any work:

- [The mbse basis](https://github.com/pitaman71/mbse-basis/blob/main/docs/README.md)
- [Principles](https://github.com/pitaman71/mbse-basis/blob/main/docs/PRINCIPLES.md)
- [Features](https://github.com/pitaman71/mbse-basis/blob/main/docs/features/README.md)
- [Capabilities](https://github.com/pitaman71/mbse-basis/blob/main/docs/capabilities/README.md)

These may be read selectively, on demand: [Vocabulary](https://github.com/pitaman71/mbse-basis/blob/main/docs/VOCABULARY.md) and
[Qualities](https://github.com/pitaman71/mbse-basis/blob/main/docs/QUALITIES.md).

Never write to `~/.claude/projects/*/memory/` or any hidden memory: what is worth keeping goes in the repository.

Resolve a link written `mbse:<repo>/<path>`, as skills and source comments write a link into another mbse
repository, to the first of these that exists: in a polyrepo checkout, `<repo root>/../<repo>/<path>`, where `<repo
root>` is this repository's root; for a link into the installed package's own repository, `<path>` without its
language directory (`python3/` or `typescript5/`), under the installed package's root (Python: the `site-packages`
directory that holds `mbse/`; npm: the package's directory), where the package ships that file; otherwise
`https://github.com/pitaman71/<repo>/blob/main/<path>`.

## This repository

- Every element an app's UI browses has a reference: it is owned by a singleton directory and keyed by an ID its
  naming pattern generates, as [the work tracker](docs/WORK_TRACKER.md)'s elements are, or it is a singleton itself.
- mbse-rest tests and builds its golden corpus over the WorkTracker (`Schemas.install`, `Seed.seed`), pinned in its
  `siblings.json`: a change to the WorkTracker's schemas or seed changes mbse-rest's corpus, so land it with a new pin
  and a regenerated corpus there.

## Commands

```sh
python3 ../mbse-basis/scripts/polyrepo.py pin   # the siblings beside this repository, pinned in siblings.json
cd python3 && uv sync && uv run pytest          # Python: use uv, never pip
```
