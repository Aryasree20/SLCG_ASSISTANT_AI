from tools.course_search import search_courses
from tools.learning_path import check_eligibility

def test_course_search():
    result = search_courses("Python")
    assert result["success"] is True
    assert result["count"] > 0

def test_unknown_topic():
    result = check_eligibility("Quantum AI Architecture", [])
    assert result["success"] is False

def test_missing_prerequisite():
    result = check_eligibility("Agent Architecture", ["Python Basics"])
    assert result["success"] is True
    assert result["eligible"] is False
    assert "LLM Fundamentals" in result["missing_prerequisites"]
