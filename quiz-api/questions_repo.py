from __future__ import annotations

import os
import sqlite3
from contextlib import closing
from typing import Optional

from app import DB_PATH, Question  # type: ignore  # noqa: WPS433
from serializers import dict_to_question, question_to_dict


# ---------------------------------------------------------------------------
# Fonctions bas niveau (SQL brut) pour Question
# ---------------------------------------------------------------------------


def _get_connection() -> sqlite3.Connection:
    """Ouvre une connexion SQLite en mode transaction manuelle."""
    conn = sqlite3.connect(DB_PATH)
    conn.isolation_level = None  # on gère BEGIN/COMMIT à la main
    return conn


def insert_question_raw(question: Question) -> int:
    """Insère la question en SQL brut et renvoie l'id attribué.

    Args:
        question: instance déjà valorisée (sans id).

    Returns:
        Identifiant auto-incrémenté généré par SQLite.
    """
    with closing(_get_connection()) as conn, closing(conn.cursor()) as cur:
        try:
            cur.execute("begin")
            cur.execute(
                "INSERT INTO question (position, title, text, image_b64) VALUES (?, ?, ?, ?)",
                (
                    question.position,
                    question.title,
                    question.text,
                    question.image_b64,
                ),
            )
            last_id = cur.lastrowid
            cur.execute("commit")
            return last_id
        except Exception:  # noqa: BLE001
            cur.execute("rollback")
            raise


def select_question_raw(question_id: int) -> Optional[Question]:
    """Charge une question depuis SQLite et renvoie une instance Question."""
    with closing(_get_connection()) as conn, closing(conn.cursor()) as cur:
        cur.execute(
            "SELECT id, position, title, text, image_b64 FROM question WHERE id = ?", (question_id,)
        )
        row = cur.fetchone()
        if row is None:
            return None
        data_dict = {
            "id": row[0],
            "position": row[1],
            "title": row[2],
            "text": row[3],
            "image_b64": row[4],
        }
        # Utilise dict_to_question pour garder la logique centrale ; on injecte Question
        q = dict_to_question(data_dict, Question)
        q.id = row[0]  # type: ignore[attr-defined]
        return q
