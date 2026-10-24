# Guide for AI agents

Demo applications for the mbse repositories, one package per app under `mbse.Demos.Apps`, laid out as every mbse repository is (`python3/mbse/Demos/Apps/WorkTracker`). Each app's
schemas are a module-scope `install(txn)`, written out in the builders' fluent syntax (mbse-basis P-019), and its seed
data a transaction of its own.

## Invariants

- **Use mbse-schemas as it stands.** An app models what it needs with what mbse-schemas offers; a gap found is reported
  to the user, not worked around in the app.
- **Siblings are checkouts beside this repository**, pinned by commit in `siblings.json`. Other agents may be working in
  them: never edit a sibling from here.
- **Every element an app's UI browses has a reference**: owned by a singleton directory, keyed by an ID its naming
  pattern generates, or a singleton itself (VISUALIZATION.md, FEA-003).
- **Tests run with pytest** from `python3/`: `uv sync && uv run pytest`. Use uv, never pip.
- **mbse-rest tests and builds its golden corpus over the WorkTracker** (`Schemas.install`, `Seed.seed`), pinned in
  its `siblings.json`: a change to the WorkTracker's schemas or seed changes mbse-rest's corpus, so land it with a
  new pin and a regenerated corpus there.

## Working agreement (M0, for every agent on mbse-rest, mbse-dynamodb, mbse-react and mbse-demo-apps)

- Work on a branch in each repository you change (M0's is `m0-contract`). Commit and push after every step whose
  tests pass (`git push -u origin <branch>`, or `python3 ../mbse-basis/scripts/polyrepo.py push` where it supports
  every sibling). Never commit to `main`. When done, open one pull request per repository with `gh pr create`,
  listing the decisions for review.
- Where VISUALIZATION.md is silent, take the simplest default consistent with it and with mbse-schemas, record it
  under "Decided by the agent, for review" (for the REST contract, in mbse-rest's `docs/CONTRACT.md`, from mbse-rest's
  own work; otherwise in this repository's docs), and keep going.
- Stop and report (do not work around) for: a gap or bug in mbse-schemas; an outward-facing action beyond pushing
  branches and opening pull requests in these repositories; anything destructive (force-push, deleting branches or
  files outside your work, rewriting history); a contradiction in VISUALIZATION.md that changes what gets built.
- Never edit a sibling from another repository's work; never edit mbse-schemas, mbse-basis or VISUALIZATION.md.
- Never write to `~/.claude/projects/*/memory/` or any hidden memory: what is worth keeping goes in the repository.
- Conventions: Python with uv (`uv sync`, `uv run pytest`), never pip; package capitalization as mbse-schemas has it
  (`mbse.Services.Rest`); "property", never "field", and "schema", never "type", for schema-governed things. Models
  as data are written in the builders' fluent syntax, never wire format, never helpers that wrap builder syntax.
- End every commit message with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`, and every pull request's
  description with `🤖 Generated with [Claude Code](https://claude.com/claude-code)`.
