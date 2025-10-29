"""Modèles SQLAlchemy pour l'application Quiz."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Quiz(db.Model):
    """Modèle représentant un quiz complet."""
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    difficulty = db.Column(db.String(20), default='easy')  # easy, medium, hard
    is_published = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    questions = db.relationship('Question', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')
    attempts = db.relationship('Attempt', backref='quiz', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_questions=False):
        data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'difficulty': self.difficulty,
            'is_published': self.is_published,
            'question_count': self.questions.count(),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_questions:
            data['questions'] = [q.to_dict() for q in self.questions.order_by(Question.position)]
        return data


class Question(db.Model):
    """Modèle représentant une question du quiz."""
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    text = db.Column(db.Text, nullable=False)
    image = db.Column(db.Text)  # URL ou base64
    difficulty = db.Column(db.String(20), default='easy')
    tags = db.Column(db.Text)  # JSON array as string
    explanation = db.Column(db.Text)  # Explication de la réponse correcte
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    choices = db.relationship('Choice', backref='question', lazy='dynamic', cascade='all, delete-orphan')
    answers = db.relationship('Answer', backref='question', lazy='dynamic', cascade='all, delete-orphan')
    
    __table_args__ = (db.UniqueConstraint('quiz_id', 'position', name='uq_quiz_position'),)
    
    def to_dict(self, include_correct=False):
        """Convertit en dictionnaire. include_correct pour admin seulement."""
        import json
        data = {
            'id': self.id,
            'position': self.position,
            'title': self.title,
            'text': self.text,
            'image': self.image,
            'difficulty': self.difficulty,
            'tags': json.loads(self.tags) if self.tags else [],
            'possibleAnswers': [c.to_dict(include_correct) for c in self.choices]
        }
        if include_correct and self.explanation:
            data['explanation'] = self.explanation
        return data


class Choice(db.Model):
    """Modèle représentant un choix de réponse."""
    __tablename__ = 'choices'
    
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    answers = db.relationship('Answer', backref='choice', lazy='dynamic')
    
    def to_dict(self, include_correct=False):
        """Convertit en dictionnaire. Expose toujours 'isCorrect' (false par défaut)."""
        return {
            'id': self.id,
            'text': self.text,
            'isCorrect': bool(self.is_correct) if include_correct else False
        }


class Attempt(db.Model):
    """Modèle représentant une tentative de quiz par un joueur."""
    __tablename__ = 'attempts'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    player_name = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, nullable=False)
    time_spent = db.Column(db.Integer, default=0)  # en secondes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    answers = db.relationship('Answer', backref='attempt', lazy='dynamic', cascade='all, delete-orphan')
    
    def to_dict(self, include_answers=False):
        data = {
            'id': self.id,
            'player_name': self.player_name,
            'score': self.score,
            'total_questions': self.total_questions,
            'percentage': round((self.score / self.total_questions * 100), 2) if self.total_questions > 0 else 0,
            'time_spent': self.time_spent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
        if include_answers:
            data['answers'] = [a.to_dict() for a in self.answers]
        return data


class Answer(db.Model):
    """Modèle représentant une réponse individuelle dans une tentative."""
    __tablename__ = 'answers'
    
    id = db.Column(db.Integer, primary_key=True)
    attempt_id = db.Column(db.Integer, db.ForeignKey('attempts.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    choice_id = db.Column(db.Integer, db.ForeignKey('choices.id'), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('attempt_id', 'question_id', name='uq_attempt_question'),)
    
    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'choice_id': self.choice_id,
            'is_correct': self.is_correct,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }

