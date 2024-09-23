from flask import Blueprint, jsonify, request
from app.db_handler import read_data, write_data

users_bp = Blueprint('users', __name__)

# Rota para listar todos os usuários
@users_bp.route('/users', methods=['GET'])
def get_users():
    data = read_data()
    return jsonify(data['users'])

# Rota para adicionar um novo usuário
@users_bp.route('/users', methods=['POST'])
def add_user():
    new_user = request.json
    data = read_data()

    # Verificar se o ID do usuário já existe
    if any(user['id'] == new_user['id'] for user in data['users']):
        return jsonify({"error": "User with this ID already exists"}), 400

    data['users'].append(new_user)
    write_data(data)
    return jsonify(new_user), 201

# Rota para alterar um usuário existente
@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = read_data()
    updated_user = request.json

    for user in data['users']:
        if user['id'] == user_id:
            user.update(updated_user)
            write_data(data)
            return jsonify(user), 200

    return jsonify({"error": "User not found"}), 404

# Rota para deletar um usuário
@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    data = read_data()
    user_to_delete = next((user for user in data['users'] if user['id'] == user_id), None)

    if user_to_delete:
        data['users'].remove(user_to_delete)
        write_data(data)
        return jsonify({"message": "User deleted successfully"}), 200

    return jsonify({"error": "User not found"}), 404
