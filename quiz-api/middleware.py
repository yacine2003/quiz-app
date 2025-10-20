"""Middleware pour l'authentification et la validation."""
from functools import wraps
from flask import request, jsonify
from jwt_utils import decode_token, JwtError


def require_auth(f):
    """Décorateur pour protéger les routes admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'No authorization header'}), 401
        
        if not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Invalid authorization header format'}), 401
        
        token = auth_header.split(' ', 1)[1]
        
        try:
            decode_token(token)
        except JwtError:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated_function

