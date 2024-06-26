import pytest

from backend.crud import snapshot as snapshot_crud
from backend.database_models.snapshot import Snapshot, SnapshotAccess, SnapshotLink
from backend.tests.factories import get_factory


@pytest.fixture(autouse=True)
def conversation(session):
    return get_factory("Conversation", session).create(id="1")


@pytest.fixture(autouse=True)
def message(session, conversation):
    return get_factory("Message", session).create(id="1", conversation_id="1")


@pytest.fixture(autouse=True)
def organization(session):
    return get_factory("Organization", session).create(id="1")


@pytest.fixture()
def snapshot(session, conversation, organization):
    return get_factory("Snapshot", session).create(
        id="1",
        user_id="1",
        organization_id="1",
        conversation_id="1",
        last_message_id="1",
        version=1,
        title="Hello, World!",
    )


# Snapshot
def test_create_snapshot(session):
    snapshot_data = Snapshot(
        user_id="1",
        organization_id="1",
        conversation_id="1",
        last_message_id="1",
        version=1,
        title="Hello, World!",
    )

    snapshot = snapshot_crud.create_snapshot(session, snapshot_data)
    assert snapshot.user_id == snapshot_data.user_id
    assert snapshot.organization_id == snapshot_data.organization_id
    assert snapshot.conversation_id == snapshot_data.conversation_id
    assert snapshot.last_message_id == snapshot_data.last_message_id
    assert snapshot.version == snapshot_data.version
    assert snapshot.title == snapshot_data.title

    snapshot = snapshot_crud.get_snapshot(session, snapshot.id)
    assert snapshot.user_id == snapshot_data.user_id
    assert snapshot.organization_id == snapshot_data.organization_id
    assert snapshot.conversation_id == snapshot_data.conversation_id
    assert snapshot.last_message_id == snapshot_data.last_message_id
    assert snapshot.version == snapshot_data.version
    assert snapshot.title == snapshot_data.title


def test_get_snapshot(session, snapshot):
    snapshot = snapshot_crud.get_snapshot(session, "1")
    assert snapshot.user_id == "1"
    assert snapshot.organization_id == "1"
    assert snapshot.conversation_id == "1"
    assert snapshot.last_message_id == "1"
    assert snapshot.version == 1
    assert snapshot.title == "Hello, World!"


def test_fail_get_nonexistent_snapshot(session):
    snapshot = snapshot_crud.get_snapshot(session, "123")
    assert snapshot is None


def test_delete_snapshot(session, snapshot):
    snapshot_crud.delete_snapshot(session, "1", "1")

    assert snapshot_crud.get_snapshot(session, "1") is None


# SnapshotLink
# def test_create_snapshot_link(session, snapshot):
#     snapshot_link_data = SnapshotLink(
#         snapshot_id="1",
#     )

#     snapshot_link = snapshot_crud.create_snapshot_link(session, snapshot_link_data)
#     assert snapshot_link.snapshot_id == snapshot_link_data.snapshot_id

#     snapshot_link = snapshot_crud.get_snapshot_link(session, snapshot_link.id)
#     assert snapshot_link.snapshot_id == snapshot_link_data.snapshot_id


# def test_get_snapshot_link(session, snapshot):
#     _ = get_factory("SnapshotLink", session).create(id="1", snapshot_id="1")

#     snapshot_link = snapshot_crud.get_snapshot_link(session, "1")
#     assert snapshot_link.snapshot_id == "1"


# def test_fail_get_nonexistent_snapshot_link(session, snapshot):
#     snapshot_link = snapshot_crud.get_snapshot_link(session, "123")
#     assert snapshot_link is None


# def test_delete_snapshot_link(session, snapshot):
#     snapshot_link = get_factory("SnapshotLink", session).create(id="1")
#     snapshot_crud.delete_snapshot_link(session, "1", "1")

#     assert snapshot_crud.get_snapshot_link(session, "1") is None


# # SnapshotAccess
# def test_create_snapshot_access(session):
#     snapshot_access_data = SnapshotAccess(
#         user_id="1",
#         snapshot_id="1",
#         link_id="1",
#     )

#     snapshot_access = snapshot_crud.create_snapshot_access(
#         session, snapshot_access_data
#     )
#     assert snapshot_access.user_id == snapshot_access_data.user_id
#     assert snapshot_access.snapshot_id == snapshot_access_data.snapshot_id
#     assert snapshot_access.link_id == snapshot_access_data.link_id

#     snapshot_access = snapshot_crud.get_snapshot_access(session, snapshot_access.id)
#     assert snapshot_access.user_id == snapshot_access_data.user_id
#     assert snapshot_access.snapshot_id == snapshot_access_data.snapshot_id
#     assert snapshot_access.link_id == snapshot_access_data.link_id


# def test_get_snapshot_access(session):
#     _ = get_factory("SnapshotAccess", session).create(
#         id="1", user_id="1", snapshot_id="1", link_id="1"
#     )

#     snapshot_access = snapshot_crud.get_snapshot_access(session, "1")
#     assert snapshot_access.user_id == "1"
#     assert snapshot_access.snapshot_id == "1"
#     assert snapshot_access.link_id == "1"


# def test_fail_get_nonexistent_snapshot_access(session):
#     snapshot_access = snapshot_crud.get_snapshot_access(session, "123")
#     assert snapshot_access is None


# def test_delete_snapshot_access(session):
#     snapshot_access = get_factory("SnapshotAccess", session).create(id="1")
#     snapshot_crud.delete_snapshot_access(session, "1", "1")

#     assert snapshot_crud.get_snapshot_access(session, "1") is None
