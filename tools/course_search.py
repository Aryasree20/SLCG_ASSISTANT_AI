import json
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "learning_data.json"

def _load_courses():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def search_courses(query: str, level: str = "", career_role: str = "") -> dict:
    """Search the local learning corpus. Returns only data present in the corpus."""
    if not isinstance(query, str) or not query.strip():
        return {"success": False, "error": "Query must be a non-empty string.", "results": []}

    courses = _load_courses()
    q = query.lower().strip()
    level = level.lower().strip()
    career_role = career_role.lower().strip()

    results = []
    for course in courses:
        haystack = " ".join([
            course["topic"], course["description"],
            course["level"], " ".join(course["career_roles"]),
            " ".join(course["next_topics"])
        ]).lower()
        level_ok = not level or course["level"].lower() == level
        role_ok = not career_role or any(career_role in r.lower() for r in course["career_roles"])
        if q in haystack and level_ok and role_ok:
            results.append(course)

    return {
        "success": True,
        "query": query,
        "count": len(results),
        "results": results
    }
