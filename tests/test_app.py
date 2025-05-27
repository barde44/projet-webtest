import pytest
from webtest import TestApp
from app.main import app

@pytest.fixture
def test_app():
    return TestApp(app)

def test_get_all_users(test_app):
    response = test_app.get("/users")
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, dict)
    assert "1" in data  # ID en tant que string dans JSON


def test_get_user(test_app):
    response = test_app.get("/users/1")
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, dict)
    assert data["name"] == "Alice"
    assert "name" in data

def test_add_user(test_app):
    response = test_app.post_json("/users", {"name": "Charlie", "email": "charlie@example.com"})
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json["name"] == "Charlie"

def test_update_user(test_app):
    test_app.post_json("/users", {"name": "David", "email": "david@example.com"})
    response = test_app.put_json("/users/3", {"name": "David Jr", "email": "dj@example.com"})
    assert response.status_code == 200
    assert response.json["name"] == "David Jr"

def test_delete_user(test_app):
    test_app.post_json("/users", {"name": "Eve", "email": "eve@example.com"})
    response = test_app.delete("/users/4")
    assert response.status_code == 200
    assert response.json == {"message": "User deleted"}

# Tests pour les erreurs

def test_invalid_user_id(test_app):
    response = test_app.get("/users/invalid", expect_errors=True)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid user ID"}

def test_user_not_found(test_app):
    response = test_app.get("/users/999", expect_errors=True)
    assert response.status_code == 404
    assert response.json == {"error": "User not found"}

def test_create_user_invalid_data(test_app):
    response = test_app.post_json("/users", {"name": "", "email": "invalid"}, expect_errors=True)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid user data"}

def test_update_user_not_found(test_app):
    response = test_app.put_json("/users/999", {"name": "X", "email": "x@example.com"}, expect_errors=True)
    assert response.status_code == 404
    assert response.json == {"error": "User not found"}

def test_delete_user_not_found(test_app):
    response = test_app.delete("/users/999", expect_errors=True)
    assert response.status_code == 404
    assert response.json == {"error": "User not found"}

def test_large_user_name(test_app):
    long_name = "A" * 300
    response = test_app.post_json("/users", {"name": long_name, "email": "longname@example.com"}, expect_errors=True)
    assert response.status_code == 400
    assert response.json == {"error": "Invalid user data"}
