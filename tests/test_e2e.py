import requests

BASE_URL = "http://127.0.0.1:8080"

def test_e2e_get_users():
    response = requests.get(f"{BASE_URL}/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert '1' in data  # Exemple d'utilisateur présent

def test_e2e_add_user():
    new_user = {"name": "Charlie", "email": "charlie@example.com"}
    response = requests.post(f"{BASE_URL}/users", json=new_user)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Charlie"
    assert data["email"] == "charlie@example.com"
