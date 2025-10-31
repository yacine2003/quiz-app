#!/usr/bin/env python3
"""Script pour importer les questions depuis le fichier JSON."""
import json
import sys
import os

# Ajouter le répertoire parent au path pour importer les modules
sys.path.insert(0, os.path.dirname(__file__))

from app_new import create_app, db
from models import Quiz, Question, Choice


def import_questions(json_file_path):
    """Importe les questions depuis un fichier JSON."""
    app = create_app('development')
    
    with app.app_context():
        # Lire le fichier JSON
        with open(json_file_path, 'r', encoding='utf-8') as f:
            questions_data = json.load(f)
        
        # Créer ou récupérer le quiz
        quiz = Quiz.query.filter_by(title='Quiz Tennis').first()
        if not quiz:
            quiz = Quiz(
                title='Quiz Tennis',
                description='Testez vos connaissances sur le tennis !',
                difficulty='easy',
                is_published=True
            )
            db.session.add(quiz)
            db.session.commit()
            print(f"✅ Quiz créé : {quiz.title} (ID: {quiz.id})")
        else:
            print(f"ℹ️  Quiz existant trouvé : {quiz.title} (ID: {quiz.id})")
            # Supprimer les anciennes questions si on réimporte
            Question.query.filter_by(quiz_id=quiz.id).delete()
            db.session.commit()
            print("🗑️  Anciennes questions supprimées")
        
        # Importer chaque question
        for idx, q_data in enumerate(questions_data, 1):
            # Créer la question
            question = Question(
                quiz_id=quiz.id,
                position=idx,
                title=f"Question {idx}",
                text=q_data['question'],
                image=q_data.get('image'),  # Ajouter le champ image
                difficulty=q_data.get('difficulty', 'easy'),
                tags=json.dumps(q_data.get('tags', [])),
                explanation=q_data.get('explanation', '')
            )
            db.session.add(question)
            db.session.flush()  # Pour obtenir l'ID
            
            # Créer les choix
            choices_dict = q_data['choices']
            correct_letter = q_data['correct']
            
            for letter in ['A', 'B', 'C', 'D']:
                if letter in choices_dict:
                    choice = Choice(
                        question_id=question.id,
                        text=choices_dict[letter],
                        is_correct=(letter == correct_letter)
                    )
                    db.session.add(choice)
            
            print(f"  ✓ Question {idx} importée")
        
        db.session.commit()
        print(f"\n🎉 Import terminé ! {len(questions_data)} questions importées.")


if __name__ == '__main__':
    # Chemin vers le fichier JSON
    json_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        'data',
        'questions.json'
    )
    
    if not os.path.exists(json_path):
        print(f"❌ Erreur : Fichier {json_path} introuvable")
        sys.exit(1)
    
    import_questions(json_path)

