"""Routes pour les quizzes."""
from flask import Blueprint, request, jsonify
from models import db, Quiz, Question
from middleware import require_auth

quiz_bp = Blueprint('quiz', __name__)


@quiz_bp.route('', methods=['GET'])
def get_quizzes():
    """Liste tous les quizzes publiés."""
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

