"""Routes d'administration (rebuild, bulk insert, cleanup)."""
from flask import Blueprint, request, jsonify
from models import db, Quiz, Question, Choice, Attempt, Answer
from middleware import require_auth


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/rebuild', methods=['POST'])
@require_auth
def rebuild_db():
    """Supprime puis recrée le schéma et insère 3 quizzes par défaut.

    - Bases du tennis (Facile) id=1
    - Roland-Garros id=2
    - Tennis avancé / technique id=3
    """
    try:
        db.drop_all()
        db.create_all()

        default_quizzes = [
            {"id": 1, "title": "Bases du tennis (Facile)", "description": "Règles et notions essentielles pour débuter.", "difficulty": "easy"},
            {"id": 2, "title": "Roland-Garros", "description": "Le tournoi parisien sur terre battue.", "difficulty": "medium"},
            {"id": 3, "title": "Tennis avancé / technique", "description": "Grips, effets et tactiques.", "difficulty": "hard"},
        ]

        for q in default_quizzes:
            if not Quiz.query.get(q["id"]):
                quiz = Quiz(**q)  # type: ignore[arg-type]
                db.session.add(quiz)

        db.session.commit()
        return jsonify({"message": "Database rebuilt successfully"}), 200
    except Exception as e:  # noqa: BLE001
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


def _parse_quiz_id(raw_value, default_value: int = 1) -> int:
    """Convertit divers formats de quiz_id en entier.

    Accepte: int, str numérique, alias ('bases'→1, 'roland'→2, 'avance'→3).
    """
    if raw_value is None:
        return int(default_value)
    if isinstance(raw_value, int):
        return raw_value
    try:
        text = str(raw_value).strip().lower()
        if text.isdigit():
            return int(text)
        alias = {
            'bases': 1,
            'roland': 2,
            'avance': 3,
            'advanced': 3,
            'hard': 3,
            'medium': 2,
            'easy': 1,
        }
        return int(alias.get(text, default_value))
    except Exception:
        return int(default_value)


def _normalize_question_payload(raw: dict, position_fallback: int, fallback_quiz_id: int = 1, forced_quiz_id: int | None = None) -> dict:
    """Normalise différents formats d'entrée en payload standard Question+Choices.

    Accepte:
    - { quiz_id, position, title, text, choices: [{text, is_correct}] }
    - { quizId, position, question, choices: {A: str, B: str, ...}, correct: 'A' }
    - { quiz_id?, question, possibleAnswers: [str], correctIndex|answerIndex: int }
    """
    import json

    # Déterminer le quiz cible
    if forced_quiz_id is not None:
        quiz_id = int(forced_quiz_id)
    else:
        provided = raw.get("quiz_id") or raw.get("quizId")
        if provided is not None:
            quiz_id = _parse_quiz_id(provided, default_value=fallback_quiz_id)
        else:
            # Mapper automatiquement par difficulté si fournie
            diff = str(raw.get("difficulty", "easy")).lower().strip()
            diff_to_quiz = {"easy": 1, "medium": 2, "hard": 3}
            quiz_id = diff_to_quiz.get(diff, fallback_quiz_id)
    title = raw.get("title") or raw.get("question") or "Question"
    text = raw.get("text") or raw.get("question") or ""
    position = raw.get("position") or position_fallback

    # Construire la liste choices
    choices = []
    if isinstance(raw.get("choices"), list):
        # Déjà sous forme [{text, is_correct}]
        choices = [
            {"text": c.get("text", ""), "is_correct": bool(c.get("is_correct", False))}
            for c in raw["choices"]
        ]
    elif isinstance(raw.get("choices"), dict):
        correct_letter = (raw.get("correct") or raw.get("answer") or "").strip()
        for letter in ["A", "B", "C", "D"]:
            if letter in raw["choices"]:
                choices.append({
                    "text": raw["choices"][letter],
                    "is_correct": letter == correct_letter,
                })
    elif isinstance(raw.get("possibleAnswers"), list):
        idx = raw.get("correctIndex")
        if idx is None:
            idx = raw.get("answerIndex")
        for i, text_choice in enumerate(raw["possibleAnswers"]):
            choices.append({
                "text": text_choice,
                "is_correct": (i == idx),
            })

    return {
        "quiz_id": int(quiz_id),
        "position": int(position),
        "title": str(title),
        "text": str(text),
        "choices": choices,
        "tags": json.dumps(raw.get("tags", [])),
        "difficulty": raw.get("difficulty", "easy"),
        "explanation": raw.get("explanation"),
    }


@admin_bp.route('/questions/bulk', methods=['POST'])
@require_auth
def bulk_insert_questions():
    """Insère en masse un tableau de questions.

    Accepte divers formats (voir _normalize_question_payload). Idempotent côté positions
    si vous fournissez des positions explicites.
    """
    try:
        payload = request.get_json(force=True)
        if not isinstance(payload, list):
            return jsonify({"error": "Expected an array of questions"}), 400

        # Optionnel: override quiz_id via query string (?quiz_id=1)
        override_quiz_id = request.args.get('quiz_id', type=str)
        forced_quiz_id: int | None = None
        if override_quiz_id is not None:
            forced_quiz_id = _parse_quiz_id(override_quiz_id, default_value=1)

        # Crée les quizzes par défaut s'ils n'existent pas
        if not Quiz.query.get(1):
            db.session.add(Quiz(id=1, title="Bases du tennis (Facile)", description="Règles et notions essentielles pour débuter.", difficulty="easy"))
        if not Quiz.query.get(2):
            db.session.add(Quiz(id=2, title="Roland-Garros", description="Le tournoi parisien sur terre battue.", difficulty="medium"))
        if not Quiz.query.get(3):
            db.session.add(Quiz(id=3, title="Tennis avancé / technique", description="Grips, effets et tactiques.", difficulty="hard"))
        db.session.flush()

        created = 0
        for idx, raw in enumerate(payload, start=1):
            normalized = _normalize_question_payload(
                raw,
                position_fallback=idx,
                fallback_quiz_id=1,
                forced_quiz_id=forced_quiz_id,
            )

            question = Question(
                quiz_id=normalized["quiz_id"],
                position=normalized["position"],
                title=normalized["title"],
                text=normalized["text"],
                difficulty=normalized["difficulty"],
                tags=normalized["tags"],
                explanation=normalized["explanation"],
            )
            db.session.add(question)
            db.session.flush()

            for c in normalized["choices"]:
                db.session.add(Choice(question_id=question.id, text=c["text"], is_correct=bool(c.get("is_correct", False))))

            created += 1

        db.session.commit()
        return jsonify({"inserted": created}), 201
    except Exception as e:  # noqa: BLE001
        db.session.rollback()
        return jsonify({"error": str(e)}), 400


@admin_bp.route('/cleanup', methods=['DELETE'])
@require_auth
def cleanup_participations():
    """Supprime toutes les tentatives/answers (utile après des tests)."""
    try:
        Answer.query.delete()
        Attempt.query.delete()
        db.session.commit()
        return '', 204
    except Exception as e:  # noqa: BLE001
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


