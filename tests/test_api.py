import os
import sys
import pytest
from bson import ObjectId

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017/stashsnip_test")

from app import create_app
from tests.test_routes import FakeSnippetsCollection, make_test_snippet


@pytest.fixture
def fake_collection(monkeypatch):
    import app.api as api_module
    import app.routes as routes_module

    collection = FakeSnippetsCollection()
    monkeypatch.setattr(api_module, "snippets_collection", collection)
    monkeypatch.setattr(routes_module, "snippets_collection", collection)
    return collection


@pytest.fixture
def client(fake_collection):
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


def test_get_snippets_empty(client, fake_collection):
    """GET /api/snippets should return an empty JSON array when no snippets exist"""
    fake_collection.documents = []
    response = client.get("/api/snippets")
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)
    assert len(json_data) == 0


def test_get_snippets_populated(client, fake_collection):
    """GET /api/snippets should return all snippets in JSON format"""
    fake_collection.documents = [
        make_test_snippet(1, language="python", tags=["flask"]),
        make_test_snippet(2, language="javascript", tags=["node"]),
    ]
    response = client.get("/api/snippets")
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 2
    assert json_data[0]["language"] == "javascript"
    assert json_data[1]["language"] == "python"


def test_get_snippets_with_query_filters(client, fake_collection):
    """GET /api/snippets?language=python should return filtered snippets"""
    fake_collection.documents = [
        make_test_snippet(1, language="python", tags=["flask"]),
        make_test_snippet(2, language="javascript", tags=["node"]),
    ]
    response = client.get("/api/snippets?language=python")
    assert response.status_code == 200
    json_data = response.get_json()
    assert len(json_data) == 1
    assert json_data[0]["language"] == "python"


def test_get_snippet_by_id_success(client, fake_collection):
    """GET /api/snippets/<id> should return a single snippet document"""
    snippet = make_test_snippet(1, language="python")
    fake_collection.documents = [snippet]
    snippet_id = str(snippet["_id"])

    response = client.get(f"/api/snippets/{snippet_id}")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["_id"] == snippet_id
    assert json_data["title"] == snippet["title"]


def test_get_snippet_by_id_not_found(client, fake_collection):
    """GET /api/snippets/<id> should return 404 for non-existent ID"""
    fake_collection.documents = []
    response = client.get("/api/snippets/000000000000000000000000")
    assert response.status_code == 404
    json_data = response.get_json()
    assert "error" in json_data


def test_get_snippet_invalid_id_format(client):
    """GET /api/snippets/<id> should return 404 for invalid ObjectId format"""
    response = client.get("/api/snippets/invalid-id-string")
    assert response.status_code == 404
    json_data = response.get_json()
    assert "error" in json_data
