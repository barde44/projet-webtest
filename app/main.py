from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de données en mémoire
users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"}
}

# Valide les données utilisateurs
def is_valid_user(data):
    return (
        data
        and "name" in data and data["name"].strip()
        and "email" in data and "@" in data["email"]
        and len(data["name"]) <= 100
    )

# Récupérer tous les utilisateurs
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

# Récupérer un utilisateur par ID
@app.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid user ID"}), 400
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

# Créer un utilisateur
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if not is_valid_user(data):
        return jsonify({"error": "Invalid user data"}), 400
    new_id = max(users.keys()) + 1
    users[new_id] = {"name": data["name"], "email": data["email"]}
    return jsonify({"id": new_id, **users[new_id]}), 201

# Mettre à jour un utilisateur
@app.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid user ID"}), 400
    data = request.json
    if not is_valid_user(data):
        return jsonify({"error": "Invalid user data"}), 400
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    users[user_id] = {"name": data["name"], "email": data["email"]}
    return jsonify(users[user_id]), 200

# Supprimer un utilisateur
@app.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid user ID"}), 400
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    del users[user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    app.run(port=8080)
