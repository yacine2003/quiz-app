from typing import Dict, Any


# ---------------------------------------------------------------------------
# Service layer – CRUD Question
# ---------------------------------------------------------------------------


def create_question(data: Dict[str, Any], *, db, Question):  # type: ignore[N803]
    """Crée et persiste une Question.

    Le modèle `Question` et l'instance `db` sont injectés par le contrôleur
    afin d'éviter toute dépendance circulaire.
    """

    required = {'position', 'title', 'text'}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"Champs manquants: {', '.join(missing)}")

    # Vérifier unicité de la position
    if Question.query.filter_by(position=data['position']).first():
        raise ValueError('Une question existe déjà pour cette position')

    q = Question(
        position=data['position'],
        title=data['title'],
        text=data['text'],
        image_b64=data.get('image_b64'),
    )
    db.session.add(q)
    db.session.commit()
    return q


def update_question(question, data: Dict[str, Any], *, db, Question):  # type: ignore[N803]
    """Met à jour une question existante avec les champs fournis."""
    if 'position' in data and data['position'] != question.position:
        # Unicité position
        if Question.query.filter_by(position=data['position']).first():
            raise ValueError('Une question existe déjà pour cette position')
        question.position = data['position']

    for field in ('title', 'text', 'image_b64'):
        if field in data:
            setattr(question, field, data[field])

    db.session.commit()
    return question
