"""Routes d'authentification."""
from flask import Blueprint, request, jsonify
import hashlib
from jwt_utils import build_token
from config import Config

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """Connexion admin avec mot de passe."""
    try:
        data = request.get_json(force=True)
        password = data.get('password', '').encode('utf-8')
        hashed = hashlib.md5(password).digest()
        
        if hashed == Config.ADMIN_PASSWORD_HASH:
            token = build_token()
            return jsonify({'token': token}), 200
        
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400

