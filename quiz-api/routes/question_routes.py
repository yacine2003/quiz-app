"""Routes pour les questions."""
from flask import Blueprint, request, jsonify
from models import db, Question, Choice, Quiz
from middleware import require_auth
import json

question_bp = Blueprint('question', __name__)


@question_bp.route('', methods=['GET'])
def get_questions():
    """Récupère les questions (par position ou toutes)."""
    position = request.args.get('position', type=int)
    quiz_id = request.args.get('quiz_id', type=int)
    
    # Si position est fournie (compatibilité ancienne API)
    if position is not None:
        question = Question.query.filter_by(position=position).first()
        if question is None:
            return jsonify({'error': 'Question not found'}), 404
        return jsonify(question.to_dict(include_correct=False)), 200
    
    # Si quiz_id est fourni
    if quiz_id is not None:
        questions = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.position).all()
        return jsonify([q.to_dict(include_correct=False) for q in questions]), 200
    
    # Sinon toutes les questions
    questions = Question.query.order_by(Question.position).all()
    return jsonify([q.to_dict(include_correct=False) for q in questions]), 200


@question_bp.route('/<int:question_id>', methods=['GET'])
def get_question(question_id):
    """Récupère une question spécifique."""
    question = Question.query.get_or_404(question_id)
    return jsonify(question.to_dict(include_correct=False)), 200


@question_bp.route('', methods=['POST'])
@require_auth
def create_question():
    """Créer une nouvelle question avec ses choix (admin only)."""
    try:
        data = request.get_json()
        
        # Vérifier que le quiz existe
        quiz = Quiz.query.get(data['quiz_id'])
        if not quiz:
            return jsonify({'error': 'Quiz not found'}), 404
        
        # Créer la question
        question = Question(
            quiz_id=data['quiz_id'],
            position=data['position'],
            title=data['title'],
            text=data['text'],
            image=data.get('image'),
            difficulty=data.get('difficulty', 'easy'),
            tags=json.dumps(data.get('tags', [])),
            explanation=data.get('explanation')
        )
        db.session.add(question)
        db.session.flush()  # Pour obtenir l'ID
        
        # Créer les choix
        if 'choices' in data:
            for choice_data in data['choices']:
                choice = Choice(
                    question_id=question.id,
                    text=choice_data['text'],
                    is_correct=choice_data.get('is_correct', False)
                )
                db.session.add(choice)
        
        db.session.commit()
        return jsonify(question.to_dict(include_correct=True)), 201
    except KeyError as e:
        db.session.rollback()
        return jsonify({'error': f'Missing field: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@question_bp.route('/<int:question_id>', methods=['PUT'])
@require_auth
def update_question(question_id):
    """Mettre à jour une question (admin only)."""
    try:
        question = Question.query.get_or_404(question_id)
        data = request.get_json()
        
        # Mettre à jour les champs
        if 'title' in data:
            question.title = data['title']
        if 'text' in data:
            question.text = data['text']
        if 'image' in data:
            question.image = data['image']
        if 'difficulty' in data:
            question.difficulty = data['difficulty']
        if 'tags' in data:
            question.tags = json.dumps(data['tags'])
        if 'explanation' in data:
            question.explanation = data['explanation']
        if 'position' in data:
            question.position = data['position']
        
        # Mettre à jour les choix si fournis
        if 'choices' in data:
            # Supprimer les anciens choix
            Choice.query.filter_by(question_id=question_id).delete()
            # Ajouter les nouveaux
            for choice_data in data['choices']:
                choice = Choice(
                    question_id=question.id,
                    text=choice_data['text'],
                    is_correct=choice_data.get('is_correct', False)
                )
                db.session.add(choice)
        
        db.session.commit()
        return jsonify(question.to_dict(include_correct=True)), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@question_bp.route('/<int:question_id>', methods=['DELETE'])
@require_auth
def delete_question(question_id):
    """Supprimer une question (admin only)."""
    try:
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return jsonify({'message': 'Question deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

