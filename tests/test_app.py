import sys
import os
import pytest
from webtest import TestApp

# Ajouter le chemin du module app pour l'import
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from app.main import app  # Importer l'application Flask

@pytest.fixture
def test_app():
    return TestApp(app)

def test_get_all_users(test_app):
    response = test_app.get("/users")
    assert response.status_code == 200
    data = response.json
    assert isinstance(data, dict)
    assert "1" in data  # Clé en chaîne de caractères

def test_get_single_user(test_app):
    response = test_app.get("/users/1")
    assert response.status_code == 200
    assert response.json["name"] == "Alice"

def test_get_user_not_found(test_app):
    response = test_app.get("/users/999", expect_errors=True)
    assert response.status_code == 404
    assert "User not found" in response.json["error"]

def test_create_user(test_app):
    new_user = {"name": "Charlie", "email": "charlie@example.com"}
    response = test_app.post_json("/users", new_user)
    assert response.status_code == 201
    assert response.json["name"] == "Charlie"

def test_update_user(test_app):
    updated_user = {"name": "Alice Updated", "email": "alice@newmail.com"}
    response = test_app.put_json("/users/1", updated_user)
    assert response.status_code == 200
    assert response.json["name"] == "Alice Updated"

def test_update_user_not_found(test_app):
    updated_user = {"name": "Unknown", "email": "unknown@example.com"}
    response = test_app.put_json("/users/999", updated_user, expect_errors=True)
    assert response.status_code == 404
    assert "User not found" in response.json["error"]

def test_delete_user(test_app):
    response = test_app.delete("/users/2")
    assert response.status_code == 200
    assert "User deleted" in response.json["message"]

def test_delete_user_not_found(test_app):
    response = test_app.delete("/users/999", expect_errors=True)
    assert response.status_code == 404
    assert "User not found" in response.json["error"]
