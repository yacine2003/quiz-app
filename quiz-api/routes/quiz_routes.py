"""Routes pour les quizzes."""
from flask import Blueprint, request, jsonify
from models import db, Quiz, Question, Choice, Answer
from middleware import require_auth
import os
import json

quiz_bp = Blueprint('quiz', __name__)


def _ensure_default_quizzes():
    """Crée les 3 quizzes par défaut s'ils n'existent pas."""
    defaults = [
        {"id": 1, "title": "Bases du tennis", "description": "Règles et notions essentielles pour débuter.", "difficulty": "easy"},
        {"id": 2, "title": "Roland-Garros", "description": "Le tournoi parisien sur terre battue.", "difficulty": "medium"},
        {"id": 3, "title": "Tennis avancé", "description": "Grips, effets et tactiques.", "difficulty": "hard"},
    ]
    created = False
    for data in defaults:
        if not Quiz.query.get(data["id"]):
            db.session.add(Quiz(**data))  # type: ignore[arg-type]
            created = True
    if created:
        db.session.commit()


def _ensure_15_per_quiz():
    """Garantit 15 questions pour chacun des quizzes 1/2/3.

    Si la répartition actuelle est différente, on réinitialise proprement les
    questions/choix des quizzes 1..3 à partir de data/questions.json, en
    distribuant 15 'easy'→1, 15 'medium'→2, 15 'hard'→3 (ou via alias quizId).
    """
    _ensure_default_quizzes()
    counts = {
        1: Question.query.filter_by(quiz_id=1).count(),
        2: Question.query.filter_by(quiz_id=2).count(),
        3: Question.query.filter_by(quiz_id=3).count(),
    }
    if counts[1] == 15 and counts[2] == 15 and counts[3] == 15:
        return

    # Résoudre de manière robuste l’emplacement du fichier questions.json
    candidates = [
        os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')), 'data', 'questions.json'),  # /app/data/questions.json
        os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')), 'data', 'questions.json'),  # /data/questions.json (au cas où)
        os.path.join('/app', 'data', 'questions.json'),
    ]
    json_path = next((p for p in candidates if os.path.exists(p)), None)
    if not json_path:
        return
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            raw = json.load(f) or []
    except Exception:
        return

    # Séparer par quiz cible
    buckets = {1: [], 2: [], 3: []}
    for item in raw:
        alias = str(item.get('quizId', '')).strip().lower()
        if alias in ('bases', 'base', 'facile', 'easy'):
            target_quiz, difficulty = 1, 'easy'
        elif alias in ('roland', 'moyen', 'medium'):
            target_quiz, difficulty = 2, 'medium'
        elif alias in ('avance', 'avancé', 'hard', 'difficile'):
            target_quiz, difficulty = 3, 'hard'
        else:
            difficulty = str(item.get('difficulty', 'easy')).lower().strip()
            target_quiz = 1 if difficulty == 'easy' else 2 if difficulty == 'medium' else 3
        buckets[target_quiz].append((item, difficulty))

    # Purge propre des questions/choices/answers des quizzes 1..3
    qids = [q.id for q in Question.query.filter(Question.quiz_id.in_([1, 2, 3])).all()]
    if qids:
        Answer.query.filter(Answer.question_id.in_(qids)).delete(synchronize_session=False)
        Choice.query.filter(Choice.question_id.in_(qids)).delete(synchronize_session=False)
        for q in Question.query.filter(Question.id.in_(qids)).all():
            db.session.delete(q)
        db.session.flush()

    # Insérer 15 questions par quiz
    for quiz_id in (1, 2, 3):
        items = buckets.get(quiz_id, [])[:15]
        pos = 1
        for item, difficulty in items:
            title = item.get('title') or item.get('question') or f"Question {pos}"
            text = item.get('text') or item.get('question') or title
            # Construire l'URL de l'image selon quiz_id et position
            image_suffix = 'base' if difficulty == 'easy' else difficulty
            image_url = item.get('image') or f"/images/questions/q{pos}{image_suffix}.png"
            q = Question(
                quiz_id=quiz_id,
                position=pos,
                title=title,
                text=text,
                difficulty=difficulty,
                image=image_url,
            )
            db.session.add(q)
            db.session.flush()

            if isinstance(item.get('choices'), dict):
                correct_letter = (item.get('correct') or '').strip()
                for letter in ['A', 'B', 'C', 'D']:
                    if letter in item['choices']:
                        db.session.add(Choice(
                            question_id=q.id,
                            text=item['choices'][letter],
                            is_correct=(letter == correct_letter),
                        ))
            else:
                for c in (item.get('choices') or []):
                    db.session.add(Choice(
                        question_id=q.id,
                        text=c.get('text', ''),
                        is_correct=bool(c.get('is_correct', False)),
                    ))
            pos += 1
    db.session.commit()


@quiz_bp.route('', methods=['GET'])
def get_quizzes():
    """Liste tous les quizzes publiés et s'assure 15/15/15 prêts pour le front.

    Normalise aussi les titres visibles par le front:
    - 1 → "Base du tennis"
    - 2 → "Roland-Garros" (inchangé)
    - 3 → "Tennis Technique"
    """
    _ensure_15_per_quiz()
    # Normaliser les noms visibles
    try:
        q1 = Quiz.query.get(1)
        if q1 and q1.title != 'Base du tennis':
            q1.title = 'Base du tennis'
        q3 = Quiz.query.get(3)
        if q3 and q3.title != 'Tennis Avancé':
            q3.title = 'Tennis Avancé'
        db.session.commit()
    except Exception:
        db.session.rollback()
    quizzes = Quiz.query.filter_by(is_published=True).all()
    return jsonify([quiz.to_dict() for quiz in quizzes]), 200


@quiz_bp.route('/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Détails d'un quiz spécifique."""
    quiz = Quiz.query.get_or_404(quiz_id)
    # Normaliser également les titres sur la page Quiz
    try:
        if quiz.id == 1 and quiz.title != 'Base du tennis':
            quiz.title = 'Base du tennis'
            db.session.commit()
        elif quiz.id == 3 and quiz.title != 'Tennis Avancé':
            quiz.title = 'Tennis Avancé'
            db.session.commit()
    except Exception:
        db.session.rollback()
    return jsonify(quiz.to_dict(include_questions=False)), 200


@quiz_bp.route('/<int:quiz_id>/questions', methods=['GET'])
def get_quiz_questions(quiz_id):
    """Liste des questions d'un quiz (sans révéler les bonnes réponses)."""
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.position).all()
    return jsonify([q.to_dict(include_correct=False) for q in questions]), 200


@quiz_bp.route('', methods=['POST'])
@require_auth
def create_quiz():
    """Créer un nouveau quiz (admin only)."""
    try:
        data = request.get_json()
        quiz = Quiz(
            title=data['title'],
            description=data.get('description'),
            difficulty=data.get('difficulty', 'easy')
        )
        db.session.add(quiz)
        db.session.commit()
        return jsonify(quiz.to_dict()), 201
    except KeyError as e:
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@quiz_bp.route('/<int:quiz_id>', methods=['PUT'])
@require_auth
def update_quiz(quiz_id):
    """Mettre à jour un quiz (admin only)."""
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        data = request.get_json()
        
        if 'title' in data:
            quiz.title = data['title']
        if 'description' in data:
            quiz.description = data['description']
        if 'difficulty' in data:
            quiz.difficulty = data['difficulty']
        if 'is_published' in data:
            quiz.is_published = data['is_published']
        
        db.session.commit()
        return jsonify(quiz.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@quiz_bp.route('/<int:quiz_id>', methods=['DELETE'])
@require_auth
def delete_quiz(quiz_id):
    """Supprimer un quiz (admin only)."""
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        db.session.delete(quiz)
        db.session.commit()
        return jsonify({'message': 'Quiz deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


# Route legacy pour compatibilité
@quiz_bp.route('/quiz-info', methods=['GET'])
def get_quiz_info():
    """Info générale du quiz (compatibilité ancienne API)."""
    # Prend le premier quiz ou crée une réponse par défaut
    quiz = Quiz.query.first()
    if quiz:
        return jsonify({
            'size': quiz.questions.count(),
            'scores': []  # To be populated from leaderboard
        }), 200
    return jsonify({'size': 0, 'scores': []}), 200

