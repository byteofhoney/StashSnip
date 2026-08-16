import os
import sys
from datetime import datetime, UTC

import pytest
from bson import ObjectId

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("MONGO_URI", "mongodb://localhost:27017/stashsnip_test")

from app import create_app


class FakeCursor:
    def __init__(self, documents):
        self.documents = list(documents)

    def sort(self, field, direction):
        reverse = direction == -1
        self.documents.sort(key=lambda document: document[field], reverse=reverse)
        return self

    def skip(self, count):
        self.documents = self.documents[count:]
        return self

    def limit(self, count):
        self.documents = self.documents[:count]
        return self

    def __iter__(self):
        return iter(self.documents)


class FakeSnippetsCollection:
    def __init__(self):
        self.documents = []

    def find(self, filters):
        return FakeCursor(
            [document for document in self.documents if self.matches(document, filters)]
        )

    def count_documents(self, filters):
        return len([document for document in self.documents if self.matches(document, filters)])

    def distinct(self, field):
        return sorted({document[field] for document in self.documents if document.get(field)})

    def find_one(self, filters):
        target_id = filters.get("_id")
        for document in self.documents:
            if document["_id"] == target_id:
                return document
        return None

    def insert_one(self, document):
        document["_id"] = ObjectId()
        self.documents.append(document)

    def delete_one(self, filters):
        target_id = filters.get("_id")
        self.documents = [document for document in self.documents if document["_id"] != target_id]

    def update_one(self, filters, update):
        document = self.find_one(filters)
        if document:
            document.update(update.get("$set", {}))
            for key in update.get("$unset", {}):
                document.pop(key, None)

    def matches(self, document, filters):
        for key, value in filters.items():
            if key == "$or":
                if not any(self.matches(document, clause) for clause in value):
                    return False
                continue
            if isinstance(value, dict) and "$exists" in value:
                exists = value["$exists"]
                if (key in document) != exists:
                    return False
                continue
            if isinstance(value, dict) and "$ne" in value:
                if document.get(key) == value["$ne"]:
                    return False
                continue
            if isinstance(value, dict) and "$regex" in value:
                if value["$regex"].lower() not in document.get(key, "").lower():
                    return False
                continue

            doc_val = document.get(key)
            if doc_val != value:
                if not isinstance(doc_val, list) or value not in doc_val:
                    return False
        return True


@pytest.fixture
def fake_collection(monkeypatch):
    import app.routes as routes

    collection = FakeSnippetsCollection()
    monkeypatch.setattr(routes, "snippets_collection", collection)
    return collection

@pytest.fixture
def client(fake_collection):
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


def make_test_snippet(index, language="python", tags=None):
    return {
        "_id": ObjectId(),
        "title": f"Snippet {index:02}",
        "language": language,
        "code": f"print({index})",
        "description": f"Example snippet {index}",
        "tags": tags or [],
        "created_at": datetime(2024, 1, index),
        "updated_at": datetime(2024, 1, index),
    }


def test_home_page_loads(client):
    """Home page should return 200"""
    response = client.get("/")
    assert response.status_code == 200


def test_add_page_loads(client):
    """Add snippet page should return 200"""
    response = client.get("/add")
    assert response.status_code == 200


def test_invalid_snippet_id_returns_404(client):
    """Accessing a snippet with fake ID should return 404"""
    response = client.get("/snippet/000000000000000000000000")
    assert response.status_code == 404


def test_add_snippet_post(client):
    """Posting a valid snippet should redirect to home"""
    response = client.post(
        "/add",
        data={
            "title": "Test Snippet",
            "language": "python",
            "code": "print('hello')",
            "description": "A test snippet",
            "tags": "test, pytest",
        },
    )
    assert response.status_code == 302


def test_home_page_paginates_snippets(client, fake_collection):
    """Home page should only render one page of snippets at a time"""
    fake_collection.documents = [make_test_snippet(index) for index in range(1, 15)]

    response = client.get("/")

    assert response.status_code == 200
    assert b"14 snippets found" in response.data
    assert b"Page 1 of 2" in response.data
    assert b"Snippet 14" in response.data
    assert b"Snippet 03" in response.data
    assert b"Snippet 02" not in response.data
    assert b"Snippet 01" not in response.data


def test_pagination_preserves_filters(client, fake_collection):
    """Page links should keep search and filter query params"""
    fake_collection.documents = [
        make_test_snippet(index, language="python", tags=["flask"])
        for index in range(1, 15)
    ]
    fake_collection.documents.append(make_test_snippet(15, language="javascript", tags=["node"]))

    response = client.get("/?q=snippet&language=python&tag=flask")

    assert response.status_code == 200
    assert b"14 snippets found" in response.data
    assert b"page=2" in response.data
    assert b"q=snippet" in response.data
    assert b"language=python" in response.data
    assert b"tag=flask" in response.data
    assert b"Snippet 15" not in response.data


def test_pagination_handles_empty_results(client, fake_collection):
    """Home page should not show pagination when there are no snippets"""
    fake_collection.documents = []

    response = client.get("/")

    assert response.status_code == 200
    assert b"0 snippets found" in response.data
    assert b"Page 1 of" not in response.data


def test_search_matches_code_field(client, fake_collection):
    """Search query should match content in the code field"""
    snip1 = make_test_snippet(1)
    snip1["code"] = "def secret_function(): pass"
    snip2 = make_test_snippet(2)
    snip2["code"] = "console.log('hello')"
    fake_collection.documents = [snip1, snip2]

    response = client.get("/?q=secret_function")
    assert response.status_code == 200
    assert b"1 snippet found" in response.data
    assert b"Snippet 01" in response.data
    assert b"Snippet 02" not in response.data


def test_stats_page_loads_and_shows_data(client, fake_collection):
    """Stats page should load and render counts correctly"""
    fake_collection.documents = [
        make_test_snippet(1, language="python", tags=["flask", "api"]),
        make_test_snippet(2, language="python", tags=["flask"]),
        make_test_snippet(3, language="javascript", tags=["node"]),
    ]

    response = client.get("/stats")
    assert response.status_code == 200
    assert b"Stash Statistics" in response.data
    assert b"Total Snippets" in response.data
    assert b"3" in response.data


def test_stats_page_empty_state(client, fake_collection):
    """Stats page should render gracefully when no snippets exist"""
    fake_collection.documents = []

    response = client.get("/stats")
    assert response.status_code == 200
    assert b"Stash Statistics" in response.data
    assert b"0" in response.data

