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
        # Compat ancienne API : se limiter au quiz 1 par défaut
        qid = request.args.get('quiz_id', default=1, type=int)
        question = Question.query.filter_by(quiz_id=qid, position=position).first()
        if question is None:
            return jsonify({'error': 'Question not found'}), 404
        return jsonify(question.to_dict(include_correct=True)), 200
    
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
    # Pour les tests TDD, on expose isCorrect sur les réponses
    return jsonify(question.to_dict(include_correct=True)), 200


@question_bp.route('', methods=['POST'])
@require_auth
def create_question():
    """Créer une nouvelle question avec ses choix (admin only)."""
    try:
        data = request.get_json() or {}

        # Compat clé quizId
        quiz_id = data.get('quiz_id') or data.get('quizId') or 1

        # Compat ancienne clé possibleAnswers → choices
        if 'possibleAnswers' in data and 'choices' not in data:
            converted = []
            for ans in data.get('possibleAnswers', []) or []:
                converted.append({
                    'text': ans.get('text', ''),
                    'is_correct': bool(ans.get('isCorrect', ans.get('is_correct', False)))
                })
            data['choices'] = converted

        # S'assurer que le quiz existe ou le créer
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            quiz = Quiz(id=quiz_id, title=f'Quiz {quiz_id}', description=None, is_published=True)
            db.session.add(quiz)
            db.session.flush()

        # Gestion position + décalage
        requested_position = data.get('position')
        existing_count = Question.query.filter_by(quiz_id=quiz_id).count()
        if requested_position is None or requested_position <= 0:
            position = existing_count + 1
        else:
            # borne entre 1 et N+1
            position = min(max(1, requested_position), existing_count + 1)
            if position <= existing_count:
                # Phase 1: pousser loin pour casser les collisions
                rows_to_shift = (Question.query
                                  .filter(Question.quiz_id == quiz_id, Question.position >= position)
                                  .order_by(Question.position.asc())
                                  .all())
                for row in rows_to_shift:
                    row.position = row.position + 1000
                db.session.flush()

                # Phase 2: ramener à la position finale (+1)
                for row in rows_to_shift:
                    row.position = row.position - 999
                db.session.flush()

        # Créer la question
        question = Question(
            quiz_id=quiz_id,
            position=position,
            title=data.get('title') or data.get('text', ''),
            text=data.get('text') or data.get('title', ''),
            image=data.get('image'),
            difficulty=data.get('difficulty', 'easy'),
            tags=json.dumps(data.get('tags', [])),
            explanation=data.get('explanation')
        )
        db.session.add(question)
        db.session.flush()  # obtenir l'ID

        for choice_data in data.get('choices', []) or []:
            choice = Choice(
                question_id=question.id,
                text=choice_data.get('text', ''),
                is_correct=bool(choice_data.get('is_correct', False))
            )
            db.session.add(choice)

        db.session.commit()
        return jsonify({'id': question.id}), 200
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
    # Vérifier existence
    question = Question.query.get(question_id)
    if not question:
        return '', 404
    data = request.get_json()
    # Compatibilité possibleAnswers
    if 'possibleAnswers' in data and 'choices' not in data:
        data['choices'] = []
        for ans in data.get('possibleAnswers', []):
            data['choices'].append({
                'text': ans.get('text', ''),
                'is_correct': bool(ans.get('isCorrect', ans.get('is_correct', False)))
            })
    try:
        if 'position' in data:
            # Réordonnancement robuste avec phase tampon pour éviter UNIQUE
            new_pos = int(data['position'])
            quiz_id = question.quiz_id
            total = Question.query.filter_by(quiz_id=quiz_id).count()
            if new_pos < 1:
                new_pos = 1
            if new_pos > total:
                new_pos = total

            old_pos = question.position
            if new_pos != old_pos:
                # Libérer la position courante
                question.position = 0
                db.session.flush()

                if new_pos < old_pos:
                    # Déplacer le bloc [new_pos .. old_pos-1] vers +1 (phase tampon puis retour)
                    rows = (Question.query
                            .filter(Question.quiz_id == quiz_id,
                                    Question.position >= new_pos,
                                    Question.position < old_pos)
                            .order_by(Question.position.asc())
                            .all())
                    for row in rows:
                        row.position = row.position + 1000
                    db.session.flush()
                    for row in rows:
                        row.position = row.position - 999  # net +1
                else:
                    # new_pos > old_pos: déplacer (old_pos+1 .. new_pos) vers -1
                    rows = (Question.query
                            .filter(Question.quiz_id == quiz_id,
                                    Question.position <= new_pos,
                                    Question.position > old_pos)
                            .order_by(Question.position.asc())
                            .all())
                    for row in rows:
                        row.position = row.position + 1000
                    db.session.flush()
                    for row in rows:
                        row.position = row.position - 1001  # net -1

                question.position = new_pos

        db.session.commit()
        # No content si succès
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


@question_bp.route('/<int:question_id>', methods=['DELETE'])
@require_auth
def delete_question(question_id):
    """Supprime une question et re-compacte les positions du quiz."""
    q = Question.query.get(question_id)
    if not q:
        return '', 404
    try:
        quiz_id = q.quiz_id
        old_pos = q.position

        # Libérer la position de la question supprimée
        q.position = 0
        db.session.flush()

        # Décaler toutes les questions suivantes (phase tampon puis décrément)
        rows = (Question.query
                .filter(Question.quiz_id == quiz_id, Question.position > old_pos)
                .order_by(Question.position.asc())
                .all())
        for row in rows:
            row.position = row.position + 1000
        db.session.flush()
        for row in rows:
            row.position = row.position - 1001  # net -1

        # Supprimer la question
        db.session.delete(q)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

