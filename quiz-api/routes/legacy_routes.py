"""Routes legacy nécessaires pour les tests Postman TDD."""
from flask import Blueprint, jsonify
from models import db, Question, Attempt, Choice, Answer
from middleware import require_auth


legacy_bp = Blueprint('legacy', __name__)


@legacy_bp.route('/questions/all', methods=['DELETE'])
@require_auth
def delete_all_questions_legacy():
    """Supprime toutes les questions (idempotent)."""
    try:
        # Supprimer d'abord les réponses et choix (delete bulk ne déclenche pas toujours les cascades)
        Answer.query.delete()
        Choice.query.delete()
        deleted = Question.query.delete()
        db.session.commit()
        if deleted > 0:
            return jsonify({'message': f'{deleted} questions deleted'}), 200
        return '', 204
    except Exception as e:  # noqa: BLE001
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@legacy_bp.route('/participations/all', methods=['DELETE'])
@require_auth
def delete_all_participations_legacy():
    """Supprime toutes les tentatives (idempotent)."""
    try:
        Answer.query.delete()
        Attempt.query.delete()
        db.session.commit()
        return '', 204
    except Exception as e:  # noqa: BLE001
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@legacy_bp.route('/quiz-info', methods=['GET'])
@legacy_bp.route('/quizzes/quiz-info', methods=['GET'])
def get_quiz_info_legacy():
    """Retourne un objet {size, scores[]} pour compat ancienne API."""
    size = Question.query.count()
    return jsonify({'size': size, 'scores': []}), 200


