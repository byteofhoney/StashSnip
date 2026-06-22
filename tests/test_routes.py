import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client

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
    response = client.post("/add", data={
        "title": "Test Snippet",
        "language": "python",
        "code": "print('hello')",
        "description": "A test snippet",
        "tags": "test, pytest"
    })
    assert response.status_code == 302