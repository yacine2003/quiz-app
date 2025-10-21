"""Routes pour le leaderboard."""
from flask import Blueprint, request, jsonify
from models import Attempt
from sqlalchemy import desc

leaderboard_bp = Blueprint('leaderboard', __name__)


@leaderboard_bp.route('/<int:quiz_id>', methods=['GET'])
def get_leaderboard(quiz_id):
    """Récupère le classement d'un quiz."""
    # Paramètres de pagination
    limit = request.args.get('limit', default=50, type=int)
    limit = min(limit, 100)  # Max 100 entrées
    
    # Récupérer les meilleures tentatives
    # Trié par score DESC, puis temps ASC (le plus rapide gagne en cas d'égalité)
    attempts = (Attempt.query
                .filter_by(quiz_id=quiz_id)
                .order_by(desc(Attempt.score), Attempt.time_spent.asc(), desc(Attempt.created_at))
                .limit(limit)
                .all())
    
    return jsonify([attempt.to_dict() for attempt in attempts]), 200


@leaderboard_bp.route('', methods=['GET'])
def get_global_leaderboard():
    """Récupère le classement global (tous les quizzes)."""
    limit = request.args.get('limit', default=50, type=int)
    limit = min(limit, 100)
    
    attempts = (Attempt.query
                .order_by(desc(Attempt.score), Attempt.time_spent.asc(), desc(Attempt.created_at))
                .limit(limit)
                .all())
    
    return jsonify([attempt.to_dict() for attempt in attempts]), 200

