from typing import Any, Dict, Type

# ---------------------------------------------------------------------------
# Sérialisation / Désérialisation pour le modèle Question
# ---------------------------------------------------------------------------


def question_to_dict(question) -> Dict[str, Any]:  # type: ignore
    """Convertit une instance Question en dict JSON-friendly."""
    return {
        "id": question.id,
        "position": question.position,
        "title": question.title,
        "text": question.text,
        "image_b64": question.image_b64,
    }


def dict_to_question(data: Dict[str, Any], Question: Type) -> Any:  # noqa: N803  # type: ignore
    """Crée une instance Question (non encore persistée) à partir d’un dict."""
    return Question(
        position=data["position"],
        title=data["title"],
        text=data["text"],
        image_b64=data.get("image_b64"),
    )
