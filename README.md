<!-- nav -->
[The work tracker →](docs/WORK_TRACKER.md)

# mbse-demo-apps

Demo applications for the mbse repositories: small, complete models that show a schema-driven app working end to end,
from its schemas to the index site that presents them (mbse-basis [FEA-001: schema-driven UI](../mbse-basis/docs/features/FEA-001.md); the work tracker's model is
[docs/WORK_TRACKER.md](docs/WORK_TRACKER.md)).

| App | Language | What it shows |
|---|---|---|
| [WorkTracker](python3/mbse/Demos/Apps/WorkTracker) | Python | Projects, features, capabilities, results and tasks, with comments and schedules; every element owned by its schema's directory under a permanent ID |

Each app depends on its mbse siblings as checkouts beside this repository (`../mbse-schemas`), pinned in
[siblings.json](siblings.json).

```sh
cd python3 && uv sync && uv run pytest
```

## Running the demo

The single-user demo ([mbse-basis/proposals/PRIORITIES.md, single-user demo](../mbse-basis/proposals/PRIORITIES.md#single-user-demo-with-schema-driven-index-site-for-any-mbse-app)): the WorkTracker served by mbse-rest and browsed with mbse-react,
its store kept in memory or in DynamoDB Local ([FEA-006: persistence](../mbse-basis/docs/features/FEA-006.md), [CAP-013: an in-memory store journaled to DynamoDB](../mbse-basis/docs/capabilities/CAP-013.md)).

```sh
scripts/demo.sh              # in memory: a fresh store each run
scripts/demo.sh dynamodb     # in DynamoDB Local, in Docker: writes survive a restart of the service
scripts/demo.sh dynamodb --check   # start everything, check each part answers, stop it all
```

Then open http://localhost:5173/. It needs the sibling checkouts beside this repository (mbse-schemas, mbse-rest,
mbse-react, and mbse-dynamodb for `dynamodb`), uv, npm, curl, and Docker for `dynamodb`. The service listens on
8000, DynamoDB Local on 8001, the UI on 5173.

*Decided by the agent, for review:* the script runs mbse-rest, mbse-dynamodb and mbse-react as they are checked out,
without pinning them in `siblings.json`: mbse-rest pins this repository (its tests and corpus run the WorkTracker), and
pinning it back would make the siblings a cycle, which `polyrepo.py land` cannot order.

---

<!-- nav -->
[The work tracker →](docs/WORK_TRACKER.md)
