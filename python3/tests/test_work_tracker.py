"""The work tracker's schemas and seed data, in a store of mbse-schemas."""

from __future__ import annotations

import pytest
from mbse.Schemas.Framework import Builders, Paths, References

from mbse.Demos.Apps.WorkTracker import Schemas, Seed

NAMES = [
    "work.Project", "work.Feature", "work.Capability", "work.Result", "work.Task", "work.Comment", "work.Schedule",
    "work.Goal",
]


@pytest.fixture
def store():
    store = Builders.Store()
    for install in Schemas.INSTALLS:
        store.transaction(install)
    store.transaction(Seed.seed)
    return store


def find(store, directory, adjacency, id_):
    """An element by its ID, through its schema's directory."""
    return getattr(store.singleton(directory), adjacency)({"id": id_})


def ids(directory, adjacency):
    return [str(entry.id) for entry in getattr(directory, adjacency)]


def test_schemas_are_valid(store):
    for name in NAMES:
        assert store.registered(name).validate() == [], name


def test_every_element_schema_is_described(store):
    """CAP-009 browses only schemas with a registered name and a description."""
    for name in NAMES:
        assert store.registered(name).description, name


def test_install_and_seed_write_nothing_again(store):
    before = {name: len(list(store.extent(name))) for name in NAMES}
    for install in Schemas.INSTALLS:
        store.transaction(install)
    store.transaction(Seed.seed)
    assert {name: len(list(store.extent(name))) for name in NAMES} == before


def test_each_element_is_in_its_directory_by_id(store):
    assert ids(store.singleton("work.Projects"), "projects") == ["PRJ-001"]
    assert ids(store.singleton("work.Features"), "features") == ["FEA-001", "FEA-002"]
    assert ids(store.singleton("work.Capabilities"), "capabilities") == ["CAP-001", "CAP-002", "CAP-003"]
    assert ids(store.singleton("work.Tasks"), "tasks") == ["TSK-001", "TSK-002"]


def test_an_id_is_generated_where_none_is_given(store):
    with store.transaction():
        task = store.work.Task(lambda t: t.title("Write the endpoints"))
    assert ids(store.singleton("work.Tasks"), "tasks") == ["TSK-001", "TSK-002", "TSK-003"]
    assert Paths.of(task) is not None


def test_an_id_does_not_change_when_an_element_moves(store):
    cap = find(store, "work.Capabilities", "capabilities", "CAP-003")
    reference = References.of(store, cap)
    ui = find(store, "work.Features", "features", "FEA-001")
    views = find(store, "work.Features", "features", "FEA-002")
    with store.transaction():
        store.work.Feature(views, lambda f: f.capabilities(lambda a: a.remove(lambda e: e.capability(cap))))
        store.work.Feature(ui, lambda f: f.capabilities([cap]))
    assert References.resolve(store, reference) is cap  # the reference taken before the move still designates it
    assert [str(e.feature.title) for e in cap.feature] == ["Schema-driven UI"]


def test_every_element_has_a_reference(store):
    for name in NAMES:
        for obj in store.extent(name):
            assert References.resolve(store, References.of(store, obj)) is obj


def test_a_thread_is_about_several_elements(store):
    thread = find(store, "work.Comments", "comments", "CMT-001")
    assert sorted(str(e.topic.title) for e in thread.about) == ["Logical view as chip", "Object browser"]


def test_replies_answer_one_thread_and_one_resolves_it(store):
    """CAP-016: two levels, a thread (About) and its replies (RepliesTo); a reply may resolve its thread."""
    thread = find(store, "work.Comments", "comments", "CMT-001")
    replies = [e.reply for e in thread.replies]
    assert [str(r.text) for r in replies] == ["Not by default: a chip stays small. The inspector lists them.",
                                            "Agreed, *no adjacencies* on chips."]
    assert [r.resolves_thread.get() for r in replies] == [False, True]
    assert all(list(r.about) == [] and [e.thread for e in r.thread] == [thread] for r in replies)


def test_a_goal_plans_its_capabilities(store):
    goal = find(store, "work.Goals", "goals", "GOL-001")
    assert [(str(e.capability.title), e.progress.get()) for e in goal.capabilities] == [
        ("No-code index view", 0.25),
        ("Logical view as chip", 0.0),
    ]


def test_an_adjacency_from_one_object_by_reference(store):
    """CAP-008's form: the capabilities of one feature, the feature given by reference."""
    views = find(store, "work.Features", "features", "FEA-002")
    frames = store.transaction(lambda t: t.mutations([lambda mu: mu.map(lambda m: m.symbols([lambda p: p
        .symbols({"f": References.of(store, views), "c": store.work.Capability})
        .spec([lambda _: _.f.capabilities([_.c])])]))]))
    assert [str(frame["c"].title) for frame in frames] == ["Logical view as chip", "Logical view of object as detail"]


def test_comments_have_a_history_and_other_elements_do_not(store):
    """CAP-015: the seed's comments were created by its transaction, recorded with the placeholder session and
    identity (no service stamped it); a task, whose schema has no history, has no record."""
    thread = find(store, "work.Comments", "comments", "CMT-001")
    [frame] = store.transaction(lambda t: t.mutations([lambda mu: mu.map(lambda m: m.symbols([lambda p: p
        .symbols({"c": References.of(store, thread), "t": store.Provenance.OfTransaction,
                  "s": store.Provenance.OfSession, "i": store.Provenance.OfIdentity})
        .spec([lambda _: _.t.created([_.c]), lambda _: _.t.session([_.s]), lambda _: _.s.who([_.i])])]))]))
    assert str(frame["t"].when).endswith("Z")
    assert [str(e.id) for e in frame["s"].directory] == ["unknown"]
    task = find(store, "work.Tasks", "tasks", "TSK-001")
    assert store.transaction(lambda t: t.mutations([lambda mu: mu.map(lambda m: m.symbols([lambda p: p
        .symbols({"x": References.of(store, task), "t": store.Provenance.OfTransaction})
        .spec([lambda _: _.t.created([_.x])])]))])) == []
