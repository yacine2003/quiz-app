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
    # TODO: mettra à jour avec données réelles plus tard
    return {"size": 0, "scores": []}, 200


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