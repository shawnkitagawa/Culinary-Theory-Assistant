import pytest
from uuid import UUID 
from datetime import datetime 


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        ({"content": "How do I make a good stock?"}, 201),
        ({"content": "What are the most important cutting skills to have?"}, 201),
        ({"content": ""}, 400),
        ({"content": "   "}, 400),
        ({}, 400),
    ],
)

def test_create_message(client, payload, expected_status): 

    #Create a chat
    create_chat_response = client.post("/chats", json = {"question": "How to make an icecream"} )

    assert create_chat_response.status_code == 201

    create_data = create_chat_response.json()

    response = client.post(f"/chats/{create_data['id']}/messages", json = payload)

    assert response.status_code == expected_status

    data = response.json()

    if response.status_code == 201: 

        message_id = UUID(data["id"])
        chat_id = UUID(create_data["id"])

        assert data["chat_id"] == create_data["id"]

        assert isinstance(message_id, UUID)
        assert isinstance(chat_id, UUID)
        assert data["role"] == "user"
        assert isinstance(data["content"], str) 
        assert data["content"] == payload["content"]
        
        created_at = datetime.fromisoformat(data["created_at"].replace("Z", "+00:00"))

        assert isinstance(created_at, datetime) 
        assert data["self"].endswith(f"messages/{message_id}")
        assert data["chat"].endswith(f"chats/{chat_id}")
    
    elif response.status_code == 400: 
        assert data["Error"] == "The request body is missing at least one of the required attributes"


def test_create_message_not_found(client):


    chat_id = "00000000-0000-0000-0000-000000000000"

    response = client.post(f"/chats/{chat_id}/messages", json={"content": "What is the science behind boiling water"})


    assert response.status_code == 404

    data = response.json()

    assert data["Error"] == "No chat with this chat_id exists" 


@pytest.mark.parametrize(
    "messages, expected_status",
    [
        (
            [
                {"content": "How do I make a good stock?"},
                {"content": "What are the most important cutting skills to have?"},
            ],
            200,
        ),
        (
            [
                {"content": "How do I make pasta taste better?"},
            ],
            200,
        ),
        (
            [],
            200,
        ),
    ],
)
def test_list_messages_for_chat(client, messages, expected_status):
    # Create a chat first
    create_chat_response = client.post(
        "/chats",
        json={"question": "How do I make ice cream?"},
    )

    assert create_chat_response.status_code == 201

    chat_data = create_chat_response.json()
    chat_id = chat_data["id"]

    # Create sample messages
    for message in messages:
        create_message_response = client.post(
            f"/chats/{chat_id}/messages",
            json=message,
        )

        assert create_message_response.status_code == 201

    response = client.get(f"/chats/{chat_id}/messages")

    assert response.status_code == expected_status

    data = response.json()

    assert isinstance(data, list)
    assert len(data) == len(messages)

    for message in data:
        assert "id" in message
        assert message["chat_id"] == chat_id
        assert message["role"] == "user"
        assert isinstance(message["content"], str)
        assert "created_at" in message
        assert "self" in message