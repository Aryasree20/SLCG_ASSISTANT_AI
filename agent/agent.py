import json
from openai import OpenAI

from tools.course_search import search_courses
from tools.learning_path import check_eligibility, recommend_next_topics
from memory.memory_manager import MemoryManager
from utils.logger import log_event

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_courses",
            "description": "Search the local learning database for topics or courses matching the learner's query. Use when exact course/topic information is needed.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Topic, course, skill, or career-related search phrase."},
                    "level": {"type": "string", "description": "Optional level such as Beginner, Intermediate, or Advanced."},
                    "career_role": {"type": "string", "description": "Optional career role such as AI Engineer or Data Scientist."}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_eligibility",
            "description": "Check whether a learner has completed the prerequisites for an exact topic in the local learning database.",
            "parameters": {
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "Exact target topic name from the learning database."},
                    "completed_topics": {"type": "array", "items": {"type": "string"}, "description": "Topics the learner has already completed."}
                },
                "required": ["topic", "completed_topics"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "recommend_next_topics",
            "description": "Recommend next topics from the local corpus using completed topics and a saved learner preference. Use when the learner asks what to learn next.",
            "parameters": {
                "type": "object",
                "properties": {
                    "completed_topics": {"type": "array", "items": {"type": "string"}},
                    "preference": {"type": "string"}
                },
                "required": ["completed_topics"]
            }
        }
    }
]

SYSTEM_PROMPT = """You are a Student Learning and Course Guidance Agent.

You help learners choose topics and learning paths using a local learning knowledge base.

Rules:
- Never invent a course, prerequisite, eligibility result, or database fact.
- Use tools when exact local-corpus information is required.
- If a tool says information is unavailable, clearly communicate that limitation.
- Consider the saved learner preference when making recommendations.
- Session context may contain earlier learner statements.
- Be concise, practical, and beginner-friendly.
- Do not claim that a career outcome is guaranteed.
"""

class LearningAgent:
    def __init__(self, client: OpenAI, model: str = "gpt-4o-mini"):
        self.client = client
        self.model = model
        self.memory = MemoryManager()

    def _tools_available(self):
        return TOOLS

    def _save_preference_if_requested(self, text: str):
        lower = text.lower()
        if "remember" in lower and ("prefer" in lower or "preference" in lower):
            self.memory.save_preference(text)
            log_event("PERSISTENT MEMORY UPDATED", text)
            return True
        return False

    def run(self, user_input: str) -> str:
        log_event("USER REQUEST", user_input)
        self.memory.add_message("user", user_input)

        if self._save_preference_if_requested(user_input):
            answer = "Saved. I’ll use that learning preference in future recommendations."
            self.memory.add_message("assistant", answer)
            log_event("FINAL RESPONSE", answer)
            return answer

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(self.memory.get_session_messages()[-10:])
        messages[0]["content"] += f"\nSaved learner preference: {self.memory.get_preference() or 'None'}"

        while True:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self._tools_available(),
                tool_choice="auto",
                temperature=0.4
            )
            message = response.choices[0].message

            if not message.tool_calls:
                answer = message.content or "I could not generate a response."
                self.memory.add_message("assistant", answer)
                log_event("FINAL RESPONSE", answer)
                return answer

            messages.append(message)

            for call in message.tool_calls:
                name = call.function.name
                try:
                    args = json.loads(call.function.arguments or "{}")
                except json.JSONDecodeError:
                    result = {"success": False, "error": "The model produced invalid tool arguments."}
                    log_event("TOOL ARGUMENT ERROR", result)
                else:
                    log_event("TOOL SELECTED", name)
                    log_event("TOOL INPUT", args)
                    try:
                        if name == "search_courses":
                            result = search_courses(**args)
                        elif name == "check_eligibility":
                            result = check_eligibility(**args)
                        elif name == "recommend_next_topics":
                            result = recommend_next_topics(
                                completed_topics=args.get("completed_topics", []),
                                preference=args.get("preference") or self.memory.get_preference() or ""
                            )
                        else:
                            result = {"success": False, "error": f"Unknown tool: {name}"}
                    except Exception as exc:
                        result = {"success": False, "error": f"Tool execution failed: {exc}"}
                    log_event("TOOL RESULT", result)

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result)
                })
