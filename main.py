from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
from agent.agent import LearningAgent

def main():
    client = OpenAI(api_key=OPENAI_API_KEY)
    agent = LearningAgent(client, model=OPENAI_MODEL)

    print("=" * 65)
    print("AI-POWERED LEARNING & COURSE GUIDANCE AGENT")
    print("=" * 65)
    print("Type 'exit' to quit.")
    print("Try:")
    print("  I know Python Basics. What should I learn next?")
    print("  Am I ready for Agent Architecture?")
    print("  Remember that I prefer practical projects.")
    print()

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if not user_input:
            continue

        try:
            answer = agent.run(user_input)
            print(f"\nAgent: {answer}\n")
        except Exception as exc:
            print("\nAgent: I couldn't complete that request safely.")
            print(f"[TRACE ERROR] {exc}\n")

if __name__ == "__main__":
    main()
