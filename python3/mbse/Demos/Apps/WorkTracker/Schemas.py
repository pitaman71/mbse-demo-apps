"""The work tracker's schemas, defined by `install(txn)`: `store.transaction(Schemas.install)`.

Organization: project -> feature -> capability -> result -> task. Planning: schedule -> goal -> capabilities, each
with its original, forecast and completed date and its progress. Comments are about organization elements.

Every element is owned and addressed through its schema, never its parent: each schema has a singleton directory
that owns its objects, keyed by `id`, which the key's naming pattern generates where none is given. An ID is
therefore unique across its schema, and does not change when an element moves. The hierarchy is ordinary relations.
"""

from __future__ import annotations

from typing import Any

__all__ = ["install"]


def install(txn: Any) -> Any:
    """The work tracker's schemas, each found by its name, else made: run again, it writes nothing."""
    S = txn.Schemas  # the store's meta-schemas and basic scalars
    return txn.uid("work/1").mutations([lambda mu: mu.upsert(lambda u: u.exists([lambda p: p
        .symbols({
            "Project": S.OfObject, "Feature": S.OfObject, "Capability": S.OfObject, "Result": S.OfObject,
            "Task": S.OfObject, "Comment": S.OfObject, "Schedule": S.OfObject, "Goal": S.OfObject,
            "ProjectDirectory": S.OfObject, "FeatureDirectory": S.OfObject, "CapabilityDirectory": S.OfObject,
            "ResultDirectory": S.OfObject, "TaskDirectory": S.OfObject, "CommentDirectory": S.OfObject,
            "ScheduleDirectory": S.OfObject, "GoalDirectory": S.OfObject,
            "InProjects": S.OfRelation, "InFeatures": S.OfRelation, "InCapabilities": S.OfRelation,
            "InResults": S.OfRelation, "InTasks": S.OfRelation, "InComments": S.OfRelation,
            "InSchedules": S.OfRelation, "InGoals": S.OfRelation,
            "HasFeature": S.OfRelation, "HasCapability": S.OfRelation, "HasResult": S.OfRelation,
            "HasTask": S.OfRelation, "HasGoal": S.OfRelation, "About": S.OfRelation, "Plans": S.OfRelation,
        })
        .spec([
            # --- Directories: a singleton per schema, owning its objects by `id` ---
            lambda _: _.InProjects.name("work.InProjects").links([
                lambda t: t.name("directory"),
                lambda t: t.name("project"),
            ]).properties([
                lambda t: t.name("id").schema([S.OfStr]).pattern(r"PRJ-(\d+\d\d)"),
            ]).uniques([["directory", "id"], ["project"]]),
            lambda _: _.InFeatures.name("work.InFeatures").links([
                lambda t: t.name("directory"),
                lambda t: t.name("feature"),
            ]).properties([
                lambda t: t.name("id").schema([S.OfStr]).pattern(r"FEA-(\d+\d\d)"),
            ]).uniques([["directory", "id"], ["feature"]]),
            lambda _: _.InCapabilities.name("work.InCapabilities").links([
                lambda t: t.name("directory"),
                lambda t: t.name("capability"),
            ]).properties([
                lambda t: t.name("id").schema([S.OfStr]).pattern(r"CAP-(\d+\d\d)"),
            ]).uniques([["directory", "id"], ["capability"]]),
            lambda _: _.InResults.name("work.InResults").links([
                lambda t: t.name("directory"),
                lambda t: t.name("result"),
            ]).properties([
                lambda t: t.name("id").schema([S.OfStr]).pattern(r"RES-(\d+\d\d)"),
            ]).uniques([["directory", "id"], ["result"]]),
            lambda _: _.InTasks.name("work.InTasks").links([
                lambda t: t.name("directory"),
                lambda t: t.name("task"),
            ]).properties([
                lambda t: t.name("id").schema([S.OfStr]).pattern(r"TSK-(\d+\d\d)"),
            ]).uniques([["directory", "id"], ["task"]]),
            lambda _: _.InComments.name("work.InComments").links([
                lambda t: t.name("directory"),
                lambda t: t.name("comment"),
            ]).properties([
                lambda t: t.name("id").schema([S.OfStr]).pattern(r"CMT-(\d+\d\d)"),
            ]).uniques([["directory", "id"], ["comment"]]),
            lambda _: _.InSchedules.name("work.InSchedules").links([
                lambda t: t.name("directory"),
                lambda t: t.name("schedule"),
            ]).properties([
                lambda t: t.name("id").schema([S.OfStr]).pattern(r"SCH-(\d+\d\d)"),
            ]).uniques([["directory", "id"], ["schedule"]]),
            lambda _: _.InGoals.name("work.InGoals").links([
                lambda t: t.name("directory"),
                lambda t: t.name("goal"),
            ]).properties([
                lambda t: t.name("id").schema([S.OfStr]).pattern(r"GOL-(\d+\d\d)"),
            ]).uniques([["directory", "id"], ["goal"]]),
            lambda _: _.ProjectDirectory.name("work.ProjectDirectory").ref(True).singleton("work.Projects").adjacencies({
                "projects": lambda a: a.relation([_.InProjects]).me("directory"),
            }),
            lambda _: _.FeatureDirectory.name("work.FeatureDirectory").ref(True).singleton("work.Features").adjacencies({
                "features": lambda a: a.relation([_.InFeatures]).me("directory"),
            }),
            lambda _: _.CapabilityDirectory.name("work.CapabilityDirectory").ref(True).singleton("work.Capabilities")
            .adjacencies({
                "capabilities": lambda a: a.relation([_.InCapabilities]).me("directory"),
            }),
            lambda _: _.ResultDirectory.name("work.ResultDirectory").ref(True).singleton("work.Results").adjacencies({
                "results": lambda a: a.relation([_.InResults]).me("directory"),
            }),
            lambda _: _.TaskDirectory.name("work.TaskDirectory").ref(True).singleton("work.Tasks").adjacencies({
                "tasks": lambda a: a.relation([_.InTasks]).me("directory"),
            }),
            lambda _: _.CommentDirectory.name("work.CommentDirectory").ref(True).singleton("work.Comments").adjacencies({
                "comments": lambda a: a.relation([_.InComments]).me("directory"),
            }),
            lambda _: _.ScheduleDirectory.name("work.ScheduleDirectory").ref(True).singleton("work.Schedules")
            .adjacencies({
                "schedules": lambda a: a.relation([_.InSchedules]).me("directory"),
            }),
            lambda _: _.GoalDirectory.name("work.GoalDirectory").ref(True).singleton("work.Goals").adjacencies({
                "goals": lambda a: a.relation([_.InGoals]).me("directory"),
            }),

            # --- The hierarchy: each child has at most one parent ---
            lambda _: _.HasFeature.name("work.HasFeature").links([
                lambda t: t.name("project"),
                lambda t: t.name("feature"),
            ]).uniques("project"),
            lambda _: _.HasCapability.name("work.HasCapability").links([
                lambda t: t.name("feature"),
                lambda t: t.name("capability"),
            ]).uniques("feature"),
            lambda _: _.HasResult.name("work.HasResult").links([
                lambda t: t.name("capability"),
                lambda t: t.name("result"),
            ]).uniques("capability"),
            lambda _: _.HasTask.name("work.HasTask").links([
                lambda t: t.name("result"),
                lambda t: t.name("task"),
            ]).uniques("result"),
            lambda _: _.HasGoal.name("work.HasGoal").links([
                lambda t: t.name("schedule"),
                lambda t: t.name("goal"),
            ]).uniques("schedule"),

            # --- Comments, about one or more organization elements ---
            lambda _: _.About.name("work.About").links([
                lambda t: t.name("comment"),
                lambda t: t.name("topic"),
            ]).uniques([]),  # a set: a comment is about a topic once

            # --- Planning: a goal's capabilities, each with its dates and progress ---
            lambda _: _.Plans.name("work.Plans").links([
                lambda t: t.name("goal"),
                lambda t: t.name("capability"),
            ]).properties({
                "original": S.OfStr,  # ISO 8601 dates, e.g. '2026-11-30'
                "forecast": S.OfStr,
                "completed": S.OfStr,
                "progress": S.OfFloat,  # a fraction from 0 to 1
            }).uniques(["original", "forecast", "completed", "progress"]),  # (goal, capability) determine the rest

            # --- The elements ---
            lambda _: _.Project.name("work.Project").description("A body of work with a purpose, broken down into features.").ref(True).properties({
                "title": S.OfStr,
                "description": S.OfStr,
            }).adjacencies([
                lambda t: t.name("directory").relation([_.InProjects]).me("project").owner(True),
                lambda t: t.name("features").relation([_.HasFeature]).me("project"),
                lambda t: t.name("comments").relation([_.About]).me("topic"),
            ]),
            lambda _: _.Feature.name("work.Feature").description("A capability area of a project, broken down into capabilities.").ref(True).properties({
                "title": S.OfStr,
                "description": S.OfStr,
            }).adjacencies([
                lambda t: t.name("directory").relation([_.InFeatures]).me("feature").owner(True),
                lambda t: t.name("project").relation([_.HasFeature]).me("feature"),
                lambda t: t.name("capabilities").relation([_.HasCapability]).me("feature"),
                lambda t: t.name("comments").relation([_.About]).me("topic"),
            ]),
            lambda _: _.Capability.name("work.Capability").description("Something the system must be able to do, delivered through results.").ref(True).properties({
                "title": S.OfStr,
                "description": S.OfStr,
            }).adjacencies([
                lambda t: t.name("directory").relation([_.InCapabilities]).me("capability").owner(True),
                lambda t: t.name("feature").relation([_.HasCapability]).me("capability"),
                lambda t: t.name("results").relation([_.HasResult]).me("capability"),
                lambda t: t.name("goals").relation([_.Plans]).me("capability"),
                lambda t: t.name("comments").relation([_.About]).me("topic"),
            ]),
            lambda _: _.Result.name("work.Result").description("A verifiable outcome that shows a capability works, reached through tasks.").ref(True).properties({
                "title": S.OfStr,
                "description": S.OfStr,
            }).adjacencies([
                lambda t: t.name("directory").relation([_.InResults]).me("result").owner(True),
                lambda t: t.name("capability").relation([_.HasResult]).me("result"),
                lambda t: t.name("tasks").relation([_.HasTask]).me("result"),
                lambda t: t.name("comments").relation([_.About]).me("topic"),
            ]),
            lambda _: _.Task.name("work.Task").description("A unit of work toward a result.").ref(True).properties({
                "title": S.OfStr,
                "description": S.OfStr,
            }).adjacencies([
                lambda t: t.name("directory").relation([_.InTasks]).me("task").owner(True),
                lambda t: t.name("result").relation([_.HasTask]).me("task"),
                lambda t: t.name("comments").relation([_.About]).me("topic"),
            ]),
            lambda _: _.Comment.name("work.Comment").description("A remark about one or more organization elements, which may be resolved.").ref(True).properties({
                "text": S.OfStr,
                "resolved": S.OfBool,
            }).adjacencies([
                lambda t: t.name("directory").relation([_.InComments]).me("comment").owner(True),
                lambda t: t.name("about").relation([_.About]).me("comment"),
            ]),
            lambda _: _.Schedule.name("work.Schedule").description("A plan of goals over time.").ref(True).properties({
                "title": S.OfStr,
                "description": S.OfStr,
            }).adjacencies([
                lambda t: t.name("directory").relation([_.InSchedules]).me("schedule").owner(True),
                lambda t: t.name("goals").relation([_.HasGoal]).me("schedule"),
            ]),
            lambda _: _.Goal.name("work.Goal").description("A milestone of a schedule: the capabilities due by it, each with its dates and progress.").ref(True).properties({
                "title": S.OfStr,
                "description": S.OfStr,
            }).adjacencies([
                lambda t: t.name("directory").relation([_.InGoals]).me("goal").owner(True),
                lambda t: t.name("schedule").relation([_.HasGoal]).me("goal"),
                lambda t: t.name("capabilities").relation([_.Plans]).me("goal"),
            ]),
        ])]))])
