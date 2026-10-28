<!-- nav -->
[← mbse-demo-apps](../README.md)

# The work tracker

The demo application of mbse-basis' schema-driven visualization (FEA-001), from the workspace's `VISUALIZATION.md`.

The single-user demo's MBSE app tracks work. Its schemas and seed data are in
`mbse-demo-apps/python3/mbse/Demos/Apps/WorkTracker`.

Organization:

```
project -> feature -> capability -> result -> task
```

- Every organization element is auto-assigned a permanent ID via regex.
- Every organization element has a title, a description, and allows
  comments, which may be resolved.

Planning:

```
schedule -> goal -> capabilities -> original/forecast/completed date, progress
```

Proposed model, for review, using mbse-schemas as it stands. Every element
is owned and addressed through its schema, never its parent: each schema
has a singleton directory that owns its objects, keyed by `id`, generated
from the schema's naming pattern when the object is created. An ID is
therefore unique across its schema and does not change when an element
moves.

| Schema | Directory (singleton) | ID pattern | Properties |
|---|---|---|---|
| `work.Project` | `work.Projects` | `PRJ-\d+\d\d` | `title`, `description` |
| `work.Feature` | `work.Features` | `FEA-\d+\d\d` | `title`, `description` |
| `work.Capability` | `work.Capabilities` | `CAP-\d+\d\d` | `title`, `description` |
| `work.Result` | `work.Results` | `RES-\d+\d\d` | `title`, `description` |
| `work.Task` | `work.Tasks` | `TSK-\d+\d\d` | `title`, `description` |
| `work.Comment` | `work.Comments` | `CMT-\d+\d\d` | `text`, `resolved` |
| `work.Schedule` | `work.Schedules` | `SCH-\d+\d\d` | `title`, `description` |
| `work.Goal` | `work.Goals` | `GOL-\d+\d\d` | `title`, `description` |

- The hierarchy is ordinary relations, not ownership: `work.HasFeature`
  (project, feature), `work.HasCapability` (feature, capability),
  `work.HasResult` (capability, result), `work.HasTask` (result, task) and
  `work.HasGoal` (schedule, goal), each `unique` on its child, so a child
  has at most one parent.
- `work.About` links a comment to each topic element it is about; every
  organization schema declares an adjacency to it.
- `work.Plans` links a goal to each of its capabilities. Its entry
  properties are `original`, `forecast` and `completed` (dates as ISO 8601
  text) and `progress` (a fraction from 0 to 1).
- `title` and `description` give each element's label and summary by
  mbse-basis CAP-005's convention.

---

<!-- nav -->
[← mbse-demo-apps](../README.md)
