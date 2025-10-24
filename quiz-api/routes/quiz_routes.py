"""Routes pour les quizzes."""
from flask import Blueprint, request, jsonify
from models import db, Quiz, Question, Choice
from middleware import require_auth
import os
import json

quiz_bp = Blueprint('quiz', __name__)


def _ensure_default_quizzes():
    """Crée les 3 quizzes par défaut s'ils n'existent pas."""
    defaults = [
        {"id": 1, "title": "Bases du tennis (Facile)", "description": "Règles et notions essentielles pour débuter.", "difficulty": "easy"},
        {"id": 2, "title": "Roland-Garros", "description": "Le tournoi parisien sur terre battue.", "difficulty": "medium"},
        {"id": 3, "title": "Tennis avancé / technique", "description": "Grips, effets et tactiques.", "difficulty": "hard"},
    ]
    created = False
    for data in defaults:
        if not Quiz.query.get(data["id"]):
            db.session.add(Quiz(**data))  # type: ignore[arg-type]
            created = True
    if created:
        db.session.commit()


def _auto_restore_questions_if_empty():
    """Si les 3 quizzes par défaut sont vides, restaure depuis data/questions.json.

    Objectif: garantir que le front affiche toujours 15/15/15 (easy/medium/hard)
    même si des tests TDD ont vidé la base.
    """
    _ensure_default_quizzes()
    counts = {
        1: Question.query.filter_by(quiz_id=1).count(),
        2: Question.query.filter_by(quiz_id=2).count(),
        3: Question.query.filter_by(quiz_id=3).count(),
    }
    if counts[1] == 0 and counts[2] == 0 and counts[3] == 0:
        # Charger le fichier JSON canonical
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        json_path = os.path.join(repo_root, 'data', 'questions.json')
        if not os.path.exists(json_path):
            return  # rien à faire
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                raw = json.load(f)
        except Exception:
            return

        # Positions par quiz
        next_pos = {1: 1, 2: 1, 3: 1}
        for item in (raw or []):
            difficulty = str(item.get('difficulty', 'easy')).lower().strip()
            target_quiz = 1 if difficulty == 'easy' else 2 if difficulty == 'medium' else 3

            title = item.get('title') or item.get('question') or f"Question {next_pos[target_quiz]}"
            text = item.get('text') or item.get('question') or title

            q = Question(
                quiz_id=target_quiz,
                position=next_pos[target_quiz],
                title=title,
                text=text,
                difficulty=difficulty,
            )
            db.session.add(q)
            db.session.flush()

            # choices: dict {A:..., B:...} + correct; ou liste [{text,is_correct}]
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

            next_pos[target_quiz] += 1

        db.session.commit()


@quiz_bp.route('', methods=['GET'])
def get_quizzes():
    """Liste tous les quizzes publiés, avec auto-restauration si nécessaire."""
    _auto_restore_questions_if_empty()
    quizzes = Quiz.query.filter_by(is_published=True).all()
    return jsonify([quiz.to_dict() for quiz in quizzes]), 200


@quiz_bp.route('/<int:quiz_id>', methods=['GET'])
def get_quiz(quiz_id):
    """Détails d'un quiz spécifique."""
    quiz = Quiz.query.get_or_404(quiz_id)
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

