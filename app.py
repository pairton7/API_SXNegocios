from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from app.db_handler import read_data, write_data

app = Flask(__name__)
CORS(app)

users_bp = Blueprint('users', __name__)

# Rota para listar todos os usuários
@app.route('/users', methods=['GET'])
def get_users():
    data = read_data()
    return jsonify(data['users'])

# Rota para adicionar um novo usuário
@app.route('/users', methods=['POST'])
def add_user():
    new_user = request.json
    data = read_data()

    # Verificar se o ID do usuário já existe
    if any(user['id'] == new_user['id'] for user in data['users']):
        return jsonify({"error": "Usuário já existente."}), 400

    data['users'].append(new_user)
    write_data(data)
    return jsonify(new_user), 201

# Rota para alterar um usuário existente
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = read_data()
    updated_user = request.json

    for user in data['users']:
        if user['id'] == user_id:
            user.update(updated_user)
            write_data(data)
            return jsonify(user), 200

    return jsonify({"error": "Usuário não encontrado."}), 404

# Rota para deletar um usuário
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    data = read_data()
    user_to_delete = next((user for user in data['users'] if user['id'] == user_id), None)

    if user_to_delete:
        data['users'].remove(user_to_delete)
        write_data(data)
        return jsonify({"message": "Usuário deletado com sucesso."}), 200

    return jsonify({"error": "Usuário não encontrado."}), 404

# Função para buscar o usuário pelo email e senha
@app.route('/users/search', methods=['GET'])
def search_user():
    email = request.args.get('email')
    senha = request.args.get('senha')

    # Lê os dados do arquivo JSON
    data = read_data()

    # Verifica se 'users' existe no dicionário retornado
    if 'users' not in data:
        return jsonify({"error": "Dados inválidos, chave 'users' não encontrada."}), 500

    # Filtrar a lista de usuários
    users = data['users']

    # Para depuração: imprimir o conteúdo de users
    print(f"Users data: {users}")

    # Buscar o usuário por email e senha
    user = next((user for user in users if user.get('email') == email and user.get('senha') == senha), None)

    # Verifica se encontrou o usuário
    if user:
        return jsonify(user), 200
    else:
        return jsonify({"error": "Usuário não encontrado."}), 404

if __name__ == '__main__':
    app.run(debug=True)
