from uuid import UUID
from datetime import datetime
from app.database.db import Chat 
from enum import Enum
import pytest

@pytest.mark.parametrize("payload, expected_status", [
      ({"question": "How do I make pasta?"}, 201),
        ({"question": "How do I make ice cream?"}, 201),
        ({}, 422),
        ({"question": ""}, 422),
        ({"question":19292929299}, 422),
        ({"question": True}, 422),
])


def test_create_chat(client, payload, expected_status, db_session): 
    response = client.post("/chats", json = payload)

    data = response.json()

    assert response.status_code == expected_status

    if expected_status == 201: 
        #Check API response
        assert isinstance(data["id"], str)
        assert isinstance(data["title"], str)
        assert isinstance(data["created_at"], str)
        assert isinstance(data["self"], str)

        chat_id  = UUID(data["id"])
        assert isinstance(chat_id, UUID)
        created_at = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
        assert isinstance(created_at,datetime)
        assert data["self"].endswith(f"/chats/{data['id']}")

        #Check actual database 
        chat = db_session.query(Chat).filter(Chat.id == UUID(data["id"])).first()

        assert chat is not None
        assert str(chat.id) == data["id"]
        assert chat.title == data["title"]
        assert isinstance(chat.created_at, datetime)
        assert data["self"].endswith(f"/chats/{data['id']}")

    if expected_status == 422: 
        assert "Error" in data 



# test only database exist
# Create -> Fetch 

class Role(str, Enum):
    user = "user"
    assistant = "assistant"



@pytest.mark.parametrize("payload", [
    {"question": "How do I make pasta?"},
    {"question": "How do I make ice cream?"},
    {"question": "How to sear steak?"},
])
def test_fetch_chat_success(client, payload): 

    # Create a post 
    create_response = client.post("/chats", json = payload)

    created_chat = create_response.json()

    assert create_response.status_code == 201

    # Fetch Data 
    get_response = client.get(f"/chats/{created_chat['id']}")
    
    data = get_response.json()

    assert get_response.status_code == 200

    chat_id = UUID(data["id"])
    assert isinstance(chat_id, UUID)
    assert isinstance(data["title"], str)

    created_at = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))
    assert isinstance(created_at, datetime )

    assert isinstance(data["messages"],list)

    for message in data["messages"]:
        assert isinstance(message, dict)

        message_id = UUID(message["id"])
        assert isinstance(message_id, UUID)
        assert message["role"] in [Role.user.value, Role.assistant.value]
        assert isinstance(message["content"], str)

        created_at = datetime.fromisoformat(message["created_at"].replace("Z","+00:00"))
        assert isinstance(created_at, datetime)

        if "source" in message: 
            for source in message["source"]:
                source_id = UUID(source["id"])
                assert isinstance(source_id, UUID)
                assert isinstance(source["document_title"], str)
                assert isinstance(source["page_start"], int)
                assert isinstance(source["page_end"], int)
                assert isinstance(source["similarity"], (int, float))
        
        assert data["self"].endswith(f"/chats/{data['id']}")



# test only database does not exist 
@pytest.mark.parametrize("chat_id, expected", [

    (91919,422),
    ("00000000-0000-0000-0000-000000000000", 404),
])


def test_fetch_chat_failure(client, chat_id, expected):

    get_response = client.get(f"/chats/{chat_id}")

    data = get_response.json()

    assert get_response.status_code == expected

    assert "Error" in  data

@pytest.mark.parametrize("url, expected_next, expected_length", [
    ("/chats", "/chats?offset=20&limit=20", 10),
    ("/chats?offset=0&limit=5", "/chats?offset=5&limit=5", 5),
    ("/chats?offset=5&limit=20", "/chats?offset=25&limit=20", 5),
    ("/chats?offset=0&limit=0", "/chats?offset=0&limit=0", 0),
])
def test_fetch_all_chat(client, url, expected_next, expected_length): 
    valid_chat_payloads = [
        {"question": "How do I make pasta?"},
        {"question": "How do I make ice cream?"},
        {"question": "How to sear steak?"},
        {"question": "How to make ramen?"},
    ]

    for i in range(10):
        payload = valid_chat_payloads[i % len(valid_chat_payloads)]

        create_response = client.get("/chats", json=payload)
        assert create_response.status_code == 201

    response = client.get(url)
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data["entries"], list)
    assert len(data["entries"]) == expected_length
    assert data["next"].endswith(expected_next)
    
    for chat in data["entries"]: 
        chat_id = UUID(chat["id"])
        assert isinstance(chat_id, UUID)

        assert isinstance(chat["title"], str)

        created_at = datetime.fromisoformat(
            chat["created_at"].replace("Z", "+00:00")
        )
        assert isinstance(created_at, datetime)

        assert chat["self"].endswith(f"/chats/{chat['id']}")


def test_delete_chat(client): 
    valid_chat_payloads = [
        {"question": "How do I make pasta?"},
        {"question": "How do I make ice cream?"},
        {"question": "How to make a beautiful cake"},
    ]

    chat_ids = []

    for payload in valid_chat_payloads: 
        create_response = client.post("/chats", json=payload)
        data = create_response.json()

        assert create_response.status_code == 201
        assert "id" in data

        chat_ids.append(data["id"])

    for chat_id in chat_ids: 
        delete_response = client.delete(f"/chats/{chat_id}")
        assert delete_response.status_code == 204

    # Try deleting the same chat again
    delete_response = client.delete(f"/chats/{chat_ids[-1]}")
    assert delete_response.status_code == 404

    #get_response to check if its deleted correctly 
    get_response = client.get("/chats")
    data = get_response.json()

    assert isinstance(data["entries"] , list)
    assert len(data["entries"]) == 0 