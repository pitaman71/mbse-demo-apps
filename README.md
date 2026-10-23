# mbse-demo-apps

Demo applications for the mbse repositories: small, complete models that show a schema-driven app working end to end,
from its schemas to the index site that presents them (`../VISUALIZATION.md` in the workspace).

| App | Language | What it shows |
|---|---|---|
| [WorkTracker](python/WorkTracker) | Python | Projects, features, capabilities, results and tasks, with comments and schedules; every element owned by its schema's directory under a permanent ID |

Each app depends on its mbse siblings as checkouts beside this repository (`../mbse-schemas`), pinned in
[siblings.json](siblings.json).

```sh
cd python/WorkTracker && uv sync && uv run pytest
```
