import streamlit as st
from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL
from agent.agent import LearningAgent


st.set_page_config(
    page_title="Learning Guidance Agent",
    page_icon="🎓",
    layout="centered"
)

st.title("🎓 AI Learning & Course Guidance Agent")
st.caption(
    "Find what to learn next, check prerequisites, "
    "and get learning guidance."
)


# Create the agent once
if "agent" not in st.session_state:
    client = OpenAI(api_key=OPENAI_API_KEY)

    st.session_state.agent = LearningAgent(
        client,
        model=OPENAI_MODEL
    )


# Store chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []


# Sidebar
with st.sidebar:
    st.header("Quick Start")

    examples = [
        "I know Python Basics. What should I learn next?",
        "Am I ready for Agent Architecture?",
        "Search for topics related to LLM",
        "Remember that I prefer practical projects."
    ]

    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.pending_prompt = example

    st.divider()

    st.subheader("About")

    st.write(
        "This interface connects to the learning agent, "
        "course search, learning-path tools, and memory."
    )


# Display previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
prompt = st.chat_input(
    "What would you like to learn?"
)


# Handle sidebar buttons
if "pending_prompt" in st.session_state:

    prompt = st.session_state.pop(
        "pending_prompt"
    )


# Process user message
if prompt:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)


    # Generate agent response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                answer = st.session_state.agent.run(
                    prompt
                )

                st.markdown(answer)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )

            except Exception as exc:

                st.error(
                    "I couldn't complete that request."
                )

                st.caption(
                    f"Error: {exc}"
                )