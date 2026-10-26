"""Seed data for the demo, written by `seed(txn)`: `store.transaction(Seed.seed)`, after `Schemas.install`.

Each element is placed in its directory under its ID, so that seeding again finds what it wrote and writes nothing.
"""

from __future__ import annotations

from typing import Any

__all__ = ["seed"]


def seed(txn: Any) -> Any:
    """A project tracking this demo's own plan, with a schedule and a goal."""
    W = txn.work  # the store's work tracker schemas, by name
    return txn.uid("work.seed/1").mutations([lambda mu: mu.upsert(lambda u: u.exists([lambda p: p
        .symbols({
            "projects": W.ProjectDirectory, "features": W.FeatureDirectory, "capabilities": W.CapabilityDirectory,
            "results": W.ResultDirectory, "tasks": W.TaskDirectory, "comments": W.CommentDirectory,
            "schedules": W.ScheduleDirectory, "goals": W.GoalDirectory,
            "demo": W.Project,
            "ui": W.Feature, "views": W.Feature,
            "index": W.Capability, "chip": W.Capability, "detail": W.Capability,
            "browser": W.Result,
            "install": W.Task, "seeded": W.Task,
            "question": W.Comment, "answer": W.Comment, "agreed": W.Comment,
            "mvp": W.Schedule,
            "demoable": W.Goal,
        })
        .spec([
            # --- Each element in its directory, under its ID ---
            lambda _: _.projects.projects({"PRJ-001": lambda e: e.project(_.demo)}),
            lambda _: _.features.features({
                "FEA-001": lambda e: e.feature(_.ui),
                "FEA-002": lambda e: e.feature(_.views),
            }),
            lambda _: _.capabilities.capabilities({
                "CAP-001": lambda e: e.capability(_.index),
                "CAP-002": lambda e: e.capability(_.chip),
                "CAP-003": lambda e: e.capability(_.detail),
            }),
            lambda _: _.results.results({"RES-001": lambda e: e.result(_.browser)}),
            lambda _: _.tasks.tasks({
                "TSK-001": lambda e: e.task(_.install),
                "TSK-002": lambda e: e.task(_.seeded),
            }),
            lambda _: _.comments.comments({
                "CMT-001": lambda e: e.comment(_.question),
                "CMT-002": lambda e: e.comment(_.answer),
                "CMT-003": lambda e: e.comment(_.agreed),
            }),
            lambda _: _.schedules.schedules({"SCH-001": lambda e: e.schedule(_.mvp)}),
            lambda _: _.goals.goals({"GOL-001": lambda e: e.goal(_.demoable)}),

            # --- Organization ---
            lambda _: _.demo
            .title("Schema-driven visualization")
            .description("An index site for any MBSE app, driven by its schemas.")
            .features([_.ui, _.views]),
            lambda _: _.ui
            .title("Schema-driven UI")
            .description("Present a useful index site driven exclusively by the schema.")
            .capabilities([_.index]),
            lambda _: _.views
            .title("No-code logical views")
            .description("Query formats the backend serves as mutation expressions.")
            .capabilities([_.chip, _.detail]),
            lambda _: _.index
            .title("No-code index view")
            .description("The index site, from the schema alone.")
            .results([_.browser]),
            lambda _: _.chip
            .title("Logical view as chip")
            .description("A medium-sized view of an object or relation entry."),
            lambda _: _.detail
            .title("Logical view of object as detail")
            .description("A full-sized view of an object."),
            lambda _: _.browser
            .title("Object browser")
            .description("Browse extant objects as chips.")
            .tasks([_.install, _.seeded]),
            lambda _: _.install
            .title("Install the schemas")
            .description("Define the work tracker's schemas in a module-scope install."),
            lambda _: _.seeded
            .title("Seed the demo")
            .description("Write a small project for the browsers to show."),
            lambda _: _.question
            .text("Should chips show adjacencies?")
            .about([_.chip, _.browser]),
            lambda _: _.answer
            .text("Not by default: a chip stays small. The inspector lists them.")
            .resolves_thread(False)
            .thread([_.question]),
            lambda _: _.agreed
            .text("Agreed, *no adjacencies* on chips.")
            .resolves_thread(True)
            .thread([_.question]),

            # --- Planning ---
            lambda _: _.mvp
            .title("MVP")
            .description("The single-user demo.")
            .goals([_.demoable]),
            lambda _: _.demoable
            .title("Demoable index site")
            .description("Browse and inspect the seeded project.")
            .capabilities([
                lambda e: e.capability(_.index).original("2026-11-30").forecast("2026-12-07").progress(0.25),
                lambda e: e.capability(_.chip).original("2026-11-30").forecast("2026-11-30").progress(0.0),
            ]),
        ])]))])
