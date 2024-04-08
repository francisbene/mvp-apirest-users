from flask import Blueprint, request, jsonify
from models.user import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """
    Retorna uma lista de todos os usuários.
    ---
    responses:
      200:
        description: Lista de usuários.
    """
    users = [{'id': user.id, 'username': user.username, 'email': user.email}
             for user in User.select()]
    return jsonify(users)

@user_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retorna detalhes de um usuário com o ID fornecido.
    ---
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID do usuário a ser retornado.
    responses:
      200:
        description: Detalhes do usuário.
      404:
        description: Usuário não encontrado.
    """
    user = User.get_or_none(id=user_id)
    if user:
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
    else:
        return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users', methods=['POST'])
def create_user():
    """
    Cria um novo usuário com base nos dados fornecidos.
    ---
    parameters:
      - in: body
        name: user
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Nome de usuário.
            email:
              type: string
              format: email
              description: Endereço de e-mail do usuário.
    responses:
      201:
        description: Usuário criado com sucesso.
    """
    data = request.json
    user = User.create(username=data['username'], email=data['email'])
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Atualiza os detalhes de um usuário existente com base nos dados fornecidos.
    ---
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID do usuário a ser atualizado.
      - in: body
        name: user
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
              description: Novo nome de usuário.
            email:
              type: string
              format: email
              description: Novo endereço de e-mail do usuário.
    responses:
      200:
        description: Detalhes do usuário atualizados com sucesso.
      404:
        description: Usuário não encontrado.
    """
    data = request.json
    user = User.get_or_none(id=user_id)
    if user:
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.save()
        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
    else:
        return jsonify({'error': 'User not found'}), 404

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Exclui um usuário existente com base no ID fornecido.
    ---
    parameters:
      - in: path
        name: user_id
        type: integer
        required: true
        description: ID do usuário a ser excluído.
    responses:
      200:
        description: Usuário excluído com sucesso.
      404:
        description: Usuário não encontrado.
    """
    user = User.get_or_none(id=user_id)
    if user:
        user.delete_instance()
        return jsonify({'message': 'User deleted successfully'})
    else:
        return jsonify({'error': 'User not found'}), 404