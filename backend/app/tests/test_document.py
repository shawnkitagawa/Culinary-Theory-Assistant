import pytest
from uuid import UUID
from datetime import datetime


@pytest.mark.parametrize(
    "payload, expected_status",
    [
        # Valid: all fields
        (
            {
                "title": "The Professional Chef",
                "total_page": 1230,
                "author": "The Culinary Institute of America",
                "published_at": "2011-09-13T00:00:00Z",
                "file_path": "uploads/the_professional_chef.pdf",
            },
            201,
        ),

        # Valid: optional fields missing
        (
            {
                "title": "On Food and Cooking",
                "total_page": 896,
                "file_path": "uploads/on_food_and_cooking.pdf",
            },
            201,
        ),

        # Missing required title
        (
            {
                "total_page": 1230,
                "author": "The Culinary Institute of America",
                "published_at": "2011-09-13T00:00:00Z",
                "file_path": "uploads/missing_title.pdf",
            },
            400,
        ),

        # Missing required total_page
        (
            {
                "title": "Missing Total Page",
                "author": "Test Author",
                "published_at": "2011-09-13T00:00:00Z",
                "file_path": "uploads/missing_total_page.pdf",
            },
            400,
        ),

        # Missing required file_path
        (
            {
                "title": "Missing File Path",
                "total_page": 100,
                "author": "Test Author",
                "published_at": "2011-09-13T00:00:00Z",
            },
            400,
        ),

        # Empty body
        ({}, 400),

        # Empty title
        (
            {
                "title": "",
                "total_page": 100,
                "file_path": "uploads/empty_title.pdf",
            },
            400,
        ),

        # Whitespace-only title
        (
            {
                "title": "   ",
                "total_page": 100,
                "file_path": "uploads/whitespace_title.pdf",
            },
            400,
        ),

        # Empty file_path
        (
            {
                "title": "Empty File Path",
                "total_page": 100,
                "file_path": "",
            },
            400,
        ),

        # Whitespace-only file_path
        (
            {
                "title": "Whitespace File Path",
                "total_page": 100,
                "file_path": "   ",
            },
            400,
        ),

        # Invalid total_page: zero
        (
            {
                "title": "Invalid Total Page Zero",
                "total_page": 0,
                "file_path": "uploads/zero_pages.pdf",
            },
            400,
        ),

        # Invalid total_page: negative
        (
            {
                "title": "Invalid Total Page Negative",
                "total_page": -5,
                "file_path": "uploads/negative_pages.pdf",
            },
            400,
        ),

        # Invalid total_page type
        (
            {
                "title": "Invalid Total Page Type",
                "total_page": "many",
                "file_path": "uploads/invalid_total_page_type.pdf",
            },
            400,
        ),

        # Invalid published_at format
        (
            {
                "title": "Invalid Published Date",
                "total_page": 100,
                "published_at": "not-a-date",
                "file_path": "uploads/invalid_date.pdf",
            },
            400,
        ),
    ],
)
def test_create_document(client, payload, expected_status):
    response = client.post("/documents", json=payload)

    assert response.status_code == expected_status

    data = response.json()

    if response.status_code == 201:
        document_id = UUID(data["document_id"])

        assert isinstance(document_id, UUID)
        assert data["title"] == payload["title"]
        assert data["total_page"] == payload["total_page"]
        assert data["file_path"] == payload["file_path"]

        # Important:
        # This assumes POST /documents also processes the document
        # and creates chunks/embeddings immediately.
        assert data["status"] == "processed"

        if "author" in payload:
            assert data["author"] == payload["author"]
        else:
            assert data["author"] is None

        if "published_at" in payload:
            published_at = datetime.fromisoformat(
                data["published_at"].replace("Z", "+00:00")
            )
            assert isinstance(published_at, datetime)
        else:
            assert data["published_at"] is None

        created_at = datetime.fromisoformat(
            data["created_at"].replace("Z", "+00:00")
        )
        assert isinstance(created_at, datetime)

        assert data["self"].endswith(f"/documents/{document_id}")

    elif response.status_code == 400:
        assert data["Error"] == (
            "The request body is missing at least one of the required attributes"
        )

def test_create_document_duplicate_file_path(client):
    payload = {
        "title": "Duplicate Document Test",
        "total_page": 100,
        "author": "Test Author",
        "published_at": "2011-09-13T00:00:00Z",
        "file_path": "uploads/duplicate_document_test.pdf",
    }

    first_response = client.post("/documents", json=payload)

    assert first_response.status_code == 201
    assert first_response.json()["status"] == "processed"

    second_response = client.post("/documents", json=payload)

    assert second_response.status_code == 409

    data = second_response.json()

    assert data["Error"] == "A document with this file_path already exists"



def test_get_document(client):
    payload = {
        "title": "The Professional Chef",
        "total_page": 1230,
        "author": "The Culinary Institute of America",
        "published_at": "2011-09-13T00:00:00Z",
        "file_path": "uploads/the_professional_chef_get_test.pdf",
    }

    create_response = client.post("/documents", json=payload)

    assert create_response.status_code == 201

    created_document = create_response.json()
    document_id = created_document["document_id"]

    response = client.get(f"/documents/{document_id}")

    assert response.status_code == 200

    data = response.json()

    parsed_document_id = UUID(data["document_id"])

    assert isinstance(parsed_document_id, UUID)
    assert data["document_id"] == document_id
    assert data["title"] == payload["title"]
    assert data["total_page"] == payload["total_page"]
    assert data["author"] == payload["author"]
    assert data["published_at"] == payload["published_at"]
    assert data["file_path"] == payload["file_path"]
    assert data["status"] in ["pending", "processed", "failed"]

    created_at = datetime.fromisoformat(
        data["created_at"].replace("Z", "+00:00")
    )

    assert isinstance(created_at, datetime)
    assert data["self"].endswith(f"/documents/{document_id}")


def test_get_document_not_found(client):
    document_id = "00000000-0000-0000-0000-000000000000"

    response = client.get(f"/documents/{document_id}")

    assert response.status_code == 404

    data = response.json()

    assert data["Error"] == "No document with this document_id exists"




def create_sample_document(client, index):
    payload = {
        "title": f"Test Culinary Document {index}",
        "total_page": 100 + index,
        "author": f"Test Author {index}",
        "published_at": "2011-09-13T00:00:00Z",
        "file_path": f"uploads/test_culinary_document_{index}.pdf",
    }

    response = client.post("/documents", json=payload)

    assert response.status_code == 201

    return response.json()


def test_list_documents_default_pagination(client):
    # Create sample documents
    for i in range(3):
        create_sample_document(client, i)

    response = client.get("/documents")

    assert response.status_code == 200

    data = response.json()

    assert "entries" in data
    assert "next" in data

    assert isinstance(data["entries"], list)

    for document in data["entries"]:
        document_id = UUID(document["document_id"])

        assert isinstance(document_id, UUID)
        assert isinstance(document["title"], str)
        assert isinstance(document["total_page"], int)
        assert document["total_page"] > 0

        assert "author" in document
        assert "published_at" in document
        assert "created_at" in document
        assert "status" in document
        assert "file_path" in document
        assert "self" in document

        created_at = datetime.fromisoformat(
            document["created_at"].replace("Z", "+00:00")
        )
        assert isinstance(created_at, datetime)

        assert document["status"] in ["pending", "processed", "failed"]
        assert document["self"].endswith(f"/documents/{document_id}")




def test_delete_document(client):
    payload = {
        "title": "The Professional Chef",
        "total_page": 1230,
        "author": "The Culinary Institute of America",
        "published_at": "2011-09-13T00:00:00Z",
        "file_path": "uploads/the_professional_chef_delete_test.pdf",
    }

    create_response = client.post("/documents", json=payload)

    assert create_response.status_code == 201

    document_id = create_response.json()["document_id"]

    # Make sure document_id is a valid UUID
    parsed_document_id = UUID(document_id)
    assert isinstance(parsed_document_id, UUID)

    # Delete document
    delete_response = client.delete(f"/documents/{document_id}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    # Make sure document no longer exists
    get_response = client.get(f"/documents/{document_id}")

    assert get_response.status_code == 404

    data = get_response.json()

    assert data["Error"] == "No document with this document_id exists"


def test_delete_document_not_found(client):
    document_id = "00000000-0000-0000-0000-000000000000"

    response = client.delete(f"/documents/{document_id}")

    assert response.status_code == 404

    data = response.json()

    assert data["Error"] == "No document with this document_id exists"



