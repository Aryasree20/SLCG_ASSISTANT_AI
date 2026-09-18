import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "learning_data.json"

def _load_courses():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def check_eligibility(topic: str, completed_topics: list[str]) -> dict:
    """Check prerequisites for an exact topic in the local corpus."""
    if not isinstance(topic, str) or not topic.strip():
        return {"success": False, "error": "Topic must be a non-empty string."}

    if not isinstance(completed_topics, list):
        return {"success": False, "error": "completed_topics must be a list of topic names."}

    courses = _load_courses()
    lookup = {c["topic"].lower(): c for c in courses}
    selected = lookup.get(topic.lower().strip())

    if selected is None:
        return {
            "success": False,
            "error": f"Topic '{topic}' was not found in the learning database."
        }

    completed = {str(x).lower().strip() for x in completed_topics}
    missing = [p for p in selected["prerequisites"] if p.lower() not in completed]

    return {
        "success": True,
        "topic": selected["topic"],
        "eligible": len(missing) == 0,
        "prerequisites": selected["prerequisites"],
        "missing_prerequisites": missing,
        "next_topics": selected["next_topics"],
        "level": selected["level"]
    }

def recommend_next_topics(completed_topics: list[str], preference: str = "") -> dict:
    """Find corpus topics whose prerequisites are satisfied and rank them by simple fit."""
    if not isinstance(completed_topics, list):
        return {"success": False, "error": "completed_topics must be a list."}

    courses = _load_courses()
    completed = {str(x).lower().strip() for x in completed_topics}
    preference = (preference or "").lower()

    candidates = []
    for c in courses:
        if c["topic"].lower() in completed:
            continue
        if all(p.lower() in completed for p in c["prerequisites"]):
            score = 0
            if "practical" in preference or "hands-on" in preference:
                if "project" in c["description"].lower() or c["topic"] in {"Agentic AI Projects","Software Engineering Basics"}:
                    score += 1
            candidates.append({
                "topic": c["topic"],
                "level": c["level"],
                "description": c["description"],
                "score": score,
                "prerequisites": c["prerequisites"]
            })

    candidates.sort(key=lambda x: (-x["score"], x["level"], x["topic"]))
    return {"success": True, "completed_topics": completed_topics, "count": len(candidates), "recommendations": candidates[:5]}
