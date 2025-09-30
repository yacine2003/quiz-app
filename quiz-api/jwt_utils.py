import jwt
import datetime
from werkzeug.exceptions import Unauthorized


class JwtError(Exception):
    """Exception levée pour les erreurs JWT"""

    def __init__(self, message="Jwt error"):
        super().__init__(message)


secret = "Groupe 2"
expiration_in_seconds = 3600


def build_token():
    """Génère un token JWT HS256 expirant dans `expiration_in_seconds`."""
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expiration_in_seconds),
        'iat': datetime.datetime.utcnow(),
        'sub': 'quiz-app-admin'
    }
    return jwt.encode(payload, secret, algorithm="HS256")


def decode_token(auth_token):
    """Vérifie et décode le token JWT passé en paramètre."""
    try:
        payload = jwt.decode(auth_token, secret, algorithms=["HS256"])
        return payload['sub']
    except jwt.ExpiredSignatureError as e:
        raise JwtError('Signature expired. Please log in again.') from e
    except jwt.InvalidTokenError as e:
        raise JwtError('Invalid token. Please log in again.') from e
