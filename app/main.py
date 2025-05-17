from flask import Flask, jsonify, request

app = Flask(__name__)

# Base de données en mémoire (simple dictionnaire)
users = {
    1: {"name": "Alice", "email": "alice@example.com"},
    2: {"name": "Bob", "email": "bob@example.com"}
}

# Récupérer tous les utilisateurs
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

# Récupérer un utilisateur par ID
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user), 200

# Créer un nouvel utilisateur
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    new_id = max(users.keys()) + 1
    users[new_id] = {"name": data["name"], "email": data["email"]}
    return jsonify({"id": new_id, "name": data["name"], "email": data["email"]}), 201

# Mettre à jour un utilisateur
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.json
    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    users[user_id] = {"name": data["name"], "email": data["email"]}
    return jsonify(users[user_id]), 200

# Supprimer un utilisateur
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
    
    del users[user_id]
    return jsonify({"message": "User deleted"}), 200

if __name__ == "__main__":
    app.run(port=8080)
