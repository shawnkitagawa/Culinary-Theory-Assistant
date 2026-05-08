from main import app 
import pytest
from uuid import UUID
from datetime import datetime
from unittest.mock import patch 


@pytest.mark.parametrize(
    "payload",
    [
        # Required field only: API should use default top_k, strictness, response_language,
        # and create a new chat if chat_id is not provided.
        (
            {"question": "Why do chefs sear meat before braising?"}
        ),

        # Optional top_k provided: API should retrieve 6 source chunks instead of the default.
        (
            {
                "question": "Why do chefs sear meat before braising?",
                "top_k": 6,
            }
        ),

        # Optional strictness provided: API should use creative mode for answer generation.
        (
            {
                "question": "Why do chefs sear meat before braising?",
                "strictness": "creative",
            }
        ),

        # Optional response_language provided: API should automatically choose the response language.
        (
            {
                "question": "Why do chefs sear meat before braising?",
                "response_language": "auto",
            }
        ),

        # All optional fields provided except chat_id:
        # API should create a new chat and use the provided retrieval/generation settings.
        (
            {
                "question": "Why do chefs sear meat before braising?",
                "top_k": 6,
                "strictness": "creative",
                "response_language": "auto",
            }
        ),
    ],
)


def test_answer_success(client, payload): 

    response = client.post("/answer", json = payload)
    assert response.status_code == 200
    
    data = response.json()

    chat_id = UUID(data["chat_id"])
    assert isinstance(chat_id, UUID)
    assert isinstance(data["user_message"], dict)

    # User Message
    messsage_id = UUID(data["user_message"]["id"])
    assert isinstance(messsage_id, UUID)
    assert data["user_message"]["role"] == "user"
    assert isinstance(data["user_message"]["content"],str)

    created_at = datetime.fromisoformat(data["user_message"]["created_at"].replace("Z", "+00:00"))
    assert isinstance(created_at, datetime)

    # Assistant Message
    assistant_id = UUID(data["assistant_message"]["id"])
    assert isinstance(assistant_id, UUID)
    assert data["assistant_message"]["role"] == "assistant"
    assert isinstance(data["assistant_message"]["content"],str)

    created_at = datetime.fromisoformat(data["assistant_message"]["created_at"].replace("Z", "+00:00"))
    assert isinstance(created_at, datetime)

    # Source 
    for source in data["sources"]:
        assert isinstance(source["id"], int)
        assert isinstance(source["document_title"], str)
        assert isinstance(source["page_start"], int)
        assert isinstance(source["page_end"], int)
        assert isinstance(source["similarity"], (int, float))
        assert isinstance(source["chunk_text"], str)

    
@pytest.mark.parametrize(
    "payload",
    [
        # Missing required question
        ({}),

        # Empty question
        ({"question": ""}),

        # Whitespace-only question
        ({"question": "     "}),

        # Wrong question types
        ({"question": 123}),
        ({"question": True}),
        ({"question": None}),
        ({"question": ["How to cook pasta?"]}),
        ({"question": {"text": "How to cook pasta?"}}),

        # Invalid top_k: must be a positive integer
        (
            {
                "question": "Why do chefs sear meat before braising?",
                "top_k": "six",
            },
        ),
        (
            {
                "question": "Why do chefs sear meat before braising?",
                "top_k": 0,
            },
        ),
        (
            {
                "question": "Why do chefs sear meat before braising?",
                "top_k": -1,
            },
        ),

        # Invalid strictness: must be strict, balanced, creative, or recipe
        (
            {
                "question": "Why do chefs sear meat before braising?",
                "strictness": "super_strict",
            },
        ),
        (
            {
                "question": "Why do chefs sear meat before braising?",
                "strictness": 123,
            },
        ),

        # Invalid response_language: must be auto, english, or japanese
        (
            {
                "question": "Why do chefs sear meat before braising?",
                "response_language": "spanish",
            },
        ),
        (
            {
                "question": "Why do chefs sear meat before braising?",
                "response_language": 123,
            },
        ),

        # Invalid chat_id format: chat_id must be a valid UUID if provided
        (
            {
                "chat_id": "not-a-valid-uuid",
                "question": "Why do chefs sear meat before braising?",
            },
        ),
    ],
)

def test_answer_failure_bad_request(client, payload): 


    response = client.post("/answer", json = payload)

    assert response.status_code == 400
    data = response.json()

    assert data["Error"] == "The request body is either missing required fields or contains invalid data types"

def test_answer_failure_not_found(client):
    payload = {
        "chat_id": "00000000-0000-0000-0000-000000000000",
        "question": "Why do chefs sear meat before braising?"
    }
    
    response = client.post("/answer", json = payload) 

    assert response.status_code == 404

    data = response.json()

    assert data["Error"] ==  "No chat with this chat_id exists"


def test_answer_internal_server_failure(client): 
    payload = {
        "question": "Why do chefs sear meat before braising"
    }

    with patch(
        "app.routes.answer.generate_rag_answer", 
        side_effect = Exception("Something failed")
    ):
        response = client.post("/answer", json = payload) 

        assert response.status_code == 500

        data = response.json()

        assert data["Error"] == "The answer could not be generated"









    




