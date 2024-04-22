from backend.tests.factories import get_factory
from backend.models.conversation import Conversation
from backend.crud import conversation as conversation_crud
from backend.crud import message as message_crud
from backend.crud import citation as citation_crud
from backend.crud import document as document_crud
from backend.schemas.conversation import UpdateConversation


def test_create_conversation(session, user):
    conversation_data = Conversation(
        user_id=user.id,
        title="Hello, World!",
        description="This is a test",
    )

    conversation = conversation_crud.create_conversation(session, conversation_data)
    assert conversation.user_id == conversation_data.user_id
    assert conversation.title == conversation_data.title
    assert conversation.description == conversation_data.description

    conversation = conversation_crud.get_conversation(session, conversation.id, user.id)
    assert conversation.user_id == conversation_data.user_id
    assert conversation.title == conversation_data.title
    assert conversation.description == conversation_data.description


def test_get_conversation(session, user):
    _ = get_factory("Conversation", session).create(
        id="1", title="Hello, World!", user_id=user.id
    )

    conversation = conversation_crud.get_conversation(session, "1", user.id)
    assert conversation.title == "Hello, World!"
    assert conversation.id == "1"


def test_fail_get_nonexistent_conversation(session, user):
    conversation = conversation_crud.get_conversation(session, "123", user_id=user.id)
    assert conversation is None


def test_list_conversations(session, user):
    _ = get_factory("Conversation", session).create(
        title="Hello, World!", user_id=user.id
    )

    conversations = conversation_crud.get_conversations(session, user.id)
    assert len(conversations) == 1
    assert conversations[0].title == "Hello, World!"


def test_list_conversations_empty(session, user):
    conversations = conversation_crud.get_conversations(session, user.id)
    assert len(conversations) == 0


def test_list_conversations_with_pagination(session, user):
    for i in range(10):
        get_factory("Conversation", session).create(
            title=f"Conversation {i}", user_id=user.id
        )

    conversations = conversation_crud.get_conversations(
        session, user_id=user.id, offset=5, limit=5
    )
    assert len(conversations) == 5

    for i, conversation in enumerate(conversations):
        assert conversation.title == f"Conversation {i + 5}"


def test_update_conversation(session, user):
    conversation = get_factory("Conversation", session).create(
        title="Hello, World!",
        description="This is a test",
        user_id=user.id,
    )

    new_conversation_data = UpdateConversation(
        title="Hello, Universe!",
        description="This is a new test",
        user_id="1",
    )

    conversation = conversation_crud.update_conversation(
        session, conversation, new_conversation_data
    )
    assert conversation.title == new_conversation_data.title
    assert conversation.description == new_conversation_data.description


def test_delete_conversation(session, user):
    conversation = get_factory("Conversation", session).create(user_id=user.id)

    conversation_crud.delete_conversation(session, conversation.id, user.id)

    conversation = conversation_crud.get_conversation(session, conversation.id, user.id)
    assert conversation is None


def test_fail_delete_nonexistent_conversation(session, user):
    conversation = conversation_crud.delete_conversation(session, "123", user.id)
    assert conversation is None


def test_delete_conversation_cascade(session, user):
    conversation = get_factory("Conversation", session).create(user_id=user.id)
    message = get_factory("Message", session).create(
        conversation_id=conversation.id, user_id=user.id
    )
    message_id = message.id
    citation = get_factory("Citation", session).create(
        message_id=message.id, user_id=user.id
    )
    citation_id = citation.id
    document = get_factory("Document", session).create(
        conversation_id=conversation.id, message_id=message.id, user_id=user.id
    )
    document_id = document.id

    conversation_crud.delete_conversation(session, conversation.id, user.id)

    conversation = conversation_crud.get_conversation(session, conversation.id, user.id)
    assert conversation is None

    message = message_crud.get_message(session, message_id, user.id)
    assert message is None

    citation = citation_crud.get_citation(session, citation_id)
    assert citation is None

    document = document_crud.get_document(session, document_id)
    assert document is None
