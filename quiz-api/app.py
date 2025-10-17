from flask import Flask, request, jsonify
# --- extensions & ORM ---
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
# autres imports
import hashlib
import os
from jwt_utils import build_token

# ---------------------------
# Config Flask & SQLAlchemy
# ---------------------------

app = Flask(__name__)
CORS(app)

# Chemin absolu vers le fichier SQLite placé dans quiz-api/quiz.db
DB_PATH = os.path.join(os.path.dirname(__file__), "quiz.db")
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialisation ORM
db = SQLAlchemy(app)

# ---------------------------
# Modèles
# ---------------------------


class Question(db.Model):
    """Modèle représentant une question du quiz (réponses simulées côté endpoint)."""

    id = db.Column(db.Integer, primary_key=True)
    position = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    image_b64 = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "position": self.position,
            "title": self.title,
            "text": self.text,
            "image_b64": self.image_b64,
        }


# Hash md5 du mot de passe "iloveflask" calculé une fois
ADMIN_PWD_HASH = b"\xd2x\x07{\xbf\xe7(Z\x14MK[\x11\xad\xb9\xcf"


@app.route('/')
def hello_world():
    return "Hello, world"


@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json(force=True)
    tried_password = payload.get('password', '').encode('utf-8')
    hashed = hashlib.md5(tried_password).digest()

    if hashed == ADMIN_PWD_HASH:
        token = build_token()
        return jsonify({"token": token}), 200

    return 'Unauthorized', 401


@app.route('/quiz-info', methods=['GET'])
def get_quiz_info():
    """Renvoie les infos générales du quiz (version initiale vide)."""
    size = Question.query.count()
    return {"size": size, "scores": []}, 200


# ---------------------------
# Endpoints Questions
# ---------------------------


from jwt_utils import decode_token, JwtError  # noqa: E402  pylint: disable=wrong-import-position
from questions_service import create_question, update_question as update_question_service  # noqa: E402  pylint: disable=wrong-import-position


def _check_admin_token(auth_header: str | None):
    """Valide le header Authorization et lève 401 en cas de problème."""
    if not auth_header or not auth_header.startswith('Bearer '):
        return False
    token = auth_header.split(' ', 1)[1]
    try:
        decode_token(token)
        return True
    except JwtError:
        return False


@app.route('/questions', methods=['POST'])
def post_question():
    """Crée une nouvelle question. Protégé par JWT."""
    if not _check_admin_token(request.headers.get('Authorization')):
        return 'Unauthorized', 401

    try:
        data = request.get_json(force=True)
        question = create_question(data, db=db, Question=Question)
        # Réponses simulées, à affiner plus tard
        dummy_answers = [
            {"id": 1, "text": "Réponse A"},
            {"id": 2, "text": "Réponse B"},
            {"id": 3, "text": "Réponse C"},
        ]
        return {**question.to_dict(), "answers": dummy_answers}, 201
    except ValueError as exc:
        return str(exc), 400


# ---------------------------
# Endpoints lecture Questions (public)
# ---------------------------


def _dummy_answers():  # provisoire
    return [
        {"id": 1, "text": "Réponse A"},
        {"id": 2, "text": "Réponse B"},
        {"id": 3, "text": "Réponse C"},
    ]


@app.route('/questions', methods=['GET'])
def get_question_by_position():
    """Retourne la question selon ?position= (public)."""
    pos = request.args.get('position', type=int)
    if pos is None:
        return 'Missing query param position', 400

    question = Question.query.filter_by(position=pos).first()
    if question is None:
        return 'Not found', 404
    return {**question.to_dict(), "answers": _dummy_answers()}, 200


@app.route('/questions/<int:question_id>', methods=['GET'])
def get_question_by_id(question_id: int):
    question = Question.query.get(question_id)
    if question is None:
        return 'Not found', 404
    return {**question.to_dict(), "answers": _dummy_answers()}, 200


@app.route('/questions/<int:question_id>', methods=['PUT'])
def update_question(question_id: int):
    if not _check_admin_token(request.headers.get('Authorization')):
        return 'Unauthorized', 401

    question = Question.query.get(question_id)
    if question is None:
        return 'Not found', 404

    try:
        data = request.get_json(force=True)
    except Exception:  # noqa: BLE001
        return 'Invalid JSON', 400

    try:
        updated = update_question_service(question, data, db=db, Question=Question)  # type: ignore
        return {**updated.to_dict(), "answers": _dummy_answers()}, 200
    except ValueError as exc:
        return str(exc), 400


# ---------------------------
# Création auto de la base au premier lancement
# ---------------------------

# Crée les tables manquantes au démarrage (idempotent)
with app.app_context():
    inspector = db.inspect(db.engine)
    if 'question' not in inspector.get_table_names():
        db.create_all()


if __name__ == "__main__":
    app.run(port=5001, debug=True)