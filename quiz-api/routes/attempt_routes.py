"""Routes pour les tentatives de quiz."""
from flask import Blueprint, request, jsonify
from models import db, Attempt, Answer, Question, Choice, Quiz

attempt_bp = Blueprint('attempt', __name__)


@attempt_bp.route('', methods=['POST'])
def submit_attempt():
    """Soumettre une tentative de quiz complète."""
    try:
        data = request.get_json()
        
        # Valider les données requises
        if 'quiz_id' not in data or 'player_name' not in data or 'answers' not in data:
            return jsonify({'error': 'Missing required fields'}), 400
        
        quiz_id = data['quiz_id']
        player_name = data['player_name']
        answers_data = data['answers']
        time_spent = data.get('time_spent', 0)
        
        # Vérifier que le quiz existe
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        # Créer la tentative
        total_questions = quiz.questions.count()
        attempt = Attempt(
            quiz_id=quiz_id,
            player_name=player_name,
            total_questions=total_questions,
            time_spent=time_spent,
            score=0  # Sera calculé après
        )
        db.session.add(attempt)
        db.session.flush()  # Pour obtenir l'ID
        
        # Traiter chaque réponse
        correct_count = 0
        correct_answers = []
        
        for answer_data in answers_data:
            question_id = answer_data['question_id']
            choice_id = answer_data['choice_id']
            
            # Vérifier si la réponse est correcte
            choice = Choice.query.get(choice_id)
            if not choice or choice.question_id != question_id:
                continue
            
            is_correct = choice.is_correct
            if is_correct:
                correct_count += 1
                correct_answers.append(question_id)
            
            # Enregistrer la réponse
            answer = Answer(
                attempt_id=attempt.id,
                question_id=question_id,
                choice_id=choice_id,
                is_correct=is_correct
            )
            db.session.add(answer)
        
        # Mettre à jour le score
        attempt.score = correct_count
        db.session.commit()
        
        # Retourner le résultat
        return jsonify({
            'id': attempt.id,
            'score': attempt.score,
            'total_questions': attempt.total_questions,
            'percentage': round((attempt.score / attempt.total_questions * 100), 2) if attempt.total_questions > 0 else 0,
            'time_spent': attempt.time_spent,
            'correct_answers': correct_answers
        }), 201
        
    except KeyError as e:
        db.session.rollback()
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@attempt_bp.route('/<int:attempt_id>', methods=['GET'])
def get_attempt(attempt_id):
    """Récupérer les détails d'une tentative."""
    attempt = Attempt.query.get_or_404(attempt_id)
    return jsonify(attempt.to_dict(include_answers=True)), 200


@attempt_bp.route('/player/<player_name>', methods=['GET'])
def get_player_attempts(player_name):
    """Récupérer toutes les tentatives d'un joueur."""
    attempts = Attempt.query.filter_by(player_name=player_name).order_by(Attempt.created_at.desc()).all()
    return jsonify([attempt.to_dict() for attempt in attempts]), 200

