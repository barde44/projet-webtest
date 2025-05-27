import pytest
from webtest import TestApp
from app.main import app

@pytest.fixture
def test_app():
    return TestApp(app)

# Tests pour la route /users
def test_get_all_users(test_app):
    response = test_app.get("/users")
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, dict)

def test_get_user(test_app):
    response = test_app.get("/users/1")
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, dict)
    assert "name" in data

def test_add_user(test_app):
    response = test_app.post_json("/users", {"name": "Charlie", "email": "charlie@example.com"})
    assert response.status_code == 201
    data = response.json
    assert isinstance(data, dict)
    assert data["name"] == "Charlie"

def test_update_user(test_app):
    response = test_app.put_json("/users/1", {"name": "Alice Updated", "email": "alice-updated@example.com"})
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, dict)
    assert data["name"] == "Alice Updated"

def test_delete_user(test_app):
    response = test_app.delete("/users/1")
    assert response.status_code == 204 or response.status_code == 200

# Tests pour les erreurs

def test_user_not_found(test_app):
    response = test_app.get("/users/999", expect_errors=True)
    assert response.status_code == 404
    assert response.json == {"error": "User not found"}

def test_invalid_user_id(test_app):
    response = test_app.get("/users/abc", expect_errors=True)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid user ID"}

def test_add_user_invalid_data(test_app):
    response = test_app.post_json("/users", {"name": "", "email": "invalid"}, expect_errors=True)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid user data"}

def test_delete_user_not_found(test_app):
    response = test_app.delete("/users/999", expect_errors=True)
    assert response.status_code == 404
    assert response.json == {"error": "User not found"}

def test_large_user_name(test_app):
    long_name = "A" * 300
    response = test_app.post_json("/users", {"name": long_name, "email": "longname@example.com"}, expect_errors=True)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid user data"}
