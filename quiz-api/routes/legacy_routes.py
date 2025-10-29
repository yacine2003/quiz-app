"""Routes legacy nécessaires pour les tests Postman TDD."""
from flask import Blueprint, jsonify, request
from models import db, Question, Attempt, Choice, Answer, Quiz
from middleware import require_auth


legacy_bp = Blueprint('legacy', __name__)

first_delete_all_called = False


@legacy_bp.route('/questions/all', methods=['DELETE'])
@require_auth
def delete_all_questions_legacy():
    """Supprime toutes les questions (toujours idempotent): retourne 204."""
    try:
        # Suppression bulk des réponses, choix et questions
        Answer.query.delete()
        Choice.query.delete()
        Question.query.delete()
        db.session.commit()
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
    """Retourne un objet {size, scores[]} pour compat ancienne API.
    - size: nombre de questions du quiz 1
    - scores: liste des participations {playerName, score} dans l'ordre d'insertion
    """
    quiz_id = 1
    size = Question.query.filter_by(quiz_id=quiz_id).count()

    attempts = (Attempt.query
                .filter_by(quiz_id=quiz_id)
                .order_by(Attempt.score.desc(), Attempt.id.asc())
                .all())
    scores = [{'playerName': a.player_name, 'score': a.score} for a in attempts]
    return jsonify({'size': size, 'scores': scores}), 200


@legacy_bp.route('/rebuild-db', methods=['POST'])
@require_auth
def rebuild_db_legacy():
    """Rebuild minimal du schéma (compat TDD): drop + create, retourne 'Ok'."""
    try:
        db.drop_all()
        db.create_all()
        return 'Ok', 200
    except Exception as e:  # noqa: BLE001
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@legacy_bp.route('/participations', methods=['POST'])
def create_participation_legacy():
    """Compat POST /participations (TDD).
    Accepte plusieurs formats:
    - { quiz_id|quizId?, player_name|playerName, answers: [ {question_id|questionId, choice_id|choiceId|answer(A/B/C/D|index)} ] }
    - quiz_id par défaut = 1 si absent
    """
    data = request.get_json(silent=True) or {}
    player_name = data.get('player_name') or data.get('playerName')
    answers_data = data.get('answers')
    if not player_name or not isinstance(answers_data, list) or len(answers_data) == 0:
        return jsonify({'error': 'Missing required fields'}), 400

    quiz_id = data.get('quiz_id') or data.get('quizId') or 1
    quiz = Quiz.query.get(quiz_id)
    if not quiz:
        # Créer un quiz par défaut si absent pour compat
        quiz = Quiz(id=quiz_id, title=f'Quiz {quiz_id}', description=None)
        db.session.add(quiz)
        db.session.flush()

    # Nombre de questions attendues pour ce quiz
    questions_in_quiz = Question.query.filter_by(quiz_id=quiz_id).order_by(Question.position.asc()).all()
    total_questions = len(questions_in_quiz)

    # Cas 1: format TDD liste d'entiers/lettres par position [1,2,3,...]
    items_are_scalars = all(not isinstance(x, dict) for x in answers_data)
    if items_are_scalars:
        # Si le nombre ne correspond pas, c'est une participation incomplète / overcomplete → 400
        if len(answers_data) != total_questions:
            return jsonify({'error': 'answers length mismatch'}), 400

    attempt = Attempt(
        quiz_id=quiz_id,
        player_name=player_name,
        total_questions=total_questions,
        score=0,
        time_spent=data.get('time_spent', 0)
    )
    db.session.add(attempt)
    db.session.flush()

    correct = 0

    if items_are_scalars:
        # Parcours par position 1..N
        for idx_pos, answered in enumerate(answers_data, start=1):
            # Récupérer la question à cette position
            q = next((q for q in questions_in_quiz if q.position == idx_pos), None)
            if not q:
                continue
            qid = q.id
            # Récupérer les choix triés
            choices = Choice.query.filter_by(question_id=qid).order_by(Choice.id.asc()).all()
            # Convertir la réponse en index 0..3
            if isinstance(answered, str):
                letter = answered.strip().upper()
                mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
                idx_choice = mapping.get(letter)
            else:
                try:
                    idx_choice = int(answered)
                    if idx_choice >= 1:
                        idx_choice = idx_choice - 1
                except Exception:
                    idx_choice = None
            cid = None
            if idx_choice is not None and 0 <= idx_choice < len(choices):
                cid = choices[idx_choice].id
            choice = Choice.query.get(cid) if cid else None
            if not choice or choice.question_id != qid:
                continue
            is_correct = bool(choice.is_correct)
            if is_correct:
                correct += 1
            ans = Answer(
                attempt_id=attempt.id,
                question_id=qid,
                choice_id=choice.id,
                is_correct=is_correct
            )
            db.session.add(ans)
    else:
        # Cas 2: format objet [{question_id, choice_id|answer}]
        for a in answers_data:
            qid = a.get('question_id') or a.get('questionId')
            cid = a.get('choice_id') or a.get('choiceId')
            answered = a.get('answer')  # index ou lettre
            if not qid:
                continue
            # Résoudre choice_id si non fourni
            if not cid and answered is not None:
                # récupérer les choix par ordre d'id
                choices = Choice.query.filter_by(question_id=qid).order_by(Choice.id.asc()).all()
                if isinstance(answered, str):
                    letter = answered.strip().upper()
                    mapping = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
                    idx = mapping.get(letter)
                else:
                    try:
                        idx = int(answered)
                        # si 1..4 → convertir en 0..3
                        if idx >= 1:
                            idx = idx - 1
                    except Exception:
                        idx = None
                if idx is not None and 0 <= idx < len(choices):
                    cid = choices[idx].id
            # Vérifier le choix
            choice = Choice.query.get(cid) if cid else None
            if not choice or choice.question_id != qid:
                # en cas d’incohérence, on ignore la réponse
                continue
            is_correct = bool(choice.is_correct)
            if is_correct:
                correct += 1
            ans = Answer(
                attempt_id=attempt.id,
                question_id=qid,
                choice_id=choice.id,
                is_correct=is_correct
            )
            db.session.add(ans)

    attempt.score = correct
    db.session.commit()
    # Le TDD attend 200 OK et des clés camelCase
    total = attempt.total_questions or 0
    percentage = round(100 * attempt.score / total, 2) if total > 0 else 0
    return jsonify({
        'id': attempt.id,
        'playerName': attempt.player_name,
        'score': attempt.score,
        'totalQuestions': total,
        'percentage': percentage
    }), 200


