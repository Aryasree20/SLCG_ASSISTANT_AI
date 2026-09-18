# AI-Powered Learning & Course Guidance Agent

A small Agentic AI prototype that helps learners choose learning topics and pathways using an LLM, local knowledge, tools, session memory, persistent preference memory, and graceful failure handling.

## 1. Business Problem

Learners often know their current skill but are unsure what to learn next, which prerequisites they are missing, or which topics fit their learning preference.

## 2. Proposed Solution

The agent:
- understands the learner's request;
- decides when a tool is needed;
- searches a local learning corpus;
- checks prerequisites;
- recommends next topics;
- remembers a learner preference;
- uses session context;
- avoids inventing unavailable information;
- exposes simple execution traces.

## 3. Architecture

```text
Learner
  |
  v
Agent Runtime
  |
  v
LLM -----> Tool Selection
             |       |       |
             v       v       v
          Search  Eligibility  Next Topics
             \       |       /
              \      |      /
               v     v     v
                 Observation
                     |
          +----------+----------+
          |                     |
          v                     v
   Session Memory      Persistent Preference
          |                     |
          +----------+----------+
                     |
                     v
                LLM Response
                     |
                     v
                  Learner
```

## 4. Tools

### Course Search Tool
Searches `data/learning_data.json` for topic/course information.

### Learning Path / Eligibility Tool
Checks prerequisites and can recommend next topics based on completed topics.

## 5. Memory

### Session Memory
Conversation messages are kept during the current application session.

### Persistent Preference
A simple learner preference is stored in `memory/user_preferences.json`.

Example:
> Remember that I prefer practical projects.

## 6. Failure Handling

If a topic does not exist in the local corpus, the tool returns a failure result. The agent is instructed not to manufacture a course or prerequisite.

Example:
> What are the prerequisites for Quantum AI Architecture?

Expected behaviour:
> The topic is not in the current learning database, so its prerequisites cannot be verified.

## 7. Trace / Observability

The console displays:
- user request;
- selected tool;
- tool input;
- tool result;
- final response;
- errors when applicable.

## 8. LLM Anatomy

Use one project prompt such as:

> I know Python Basics. What should I learn before Agentic AI?

Explain:
`Prompt -> Tokenization -> Token IDs -> Embeddings + Positional Information -> Transformer Layers -> Q/K/V -> Self-Attention -> Residual Connection -> FFN -> Multiple Layers -> Logits -> Softmax/Probabilities -> Decoding -> Next Token`

The assignment requires each group to explain these concepts in simple language.

## 9. Temperature

For a learning recommendation:
- lower temperature generally produces more consistent wording;
- higher temperature produces more variation.

Higher temperature does not make the model more intelligent.

## 10. Framework Decision

This prototype uses a small custom runtime because the assignment's required behaviour can be demonstrated without a large framework.

For a larger production workflow, compare approaches such as LangChain, LangGraph, CrewAI and conversation-oriented multi-agent systems against requirements such as branching, retries, durable state, human approval, collaboration and traceability.

## 11. Setup

```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

Install:
```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and add your API key.

Run:
```bash
python main.py
```

## 12. Example Demonstrations

### Tool 1
`Search for topics related to LLM`

### Tool 2
`I know Python Basics. Am I ready for Agent Architecture?`

### No Tool
`What is an LLM?`

### Session Memory
`I'm learning Python Basics.`
then:
`What should I learn after that?`

### Persistent Preference
`Remember that I prefer practical projects.`
then:
`What should I learn next?`

### Failure
`What are the prerequisites for Quantum AI Architecture?`

## 13. Project Structure

```text
learning_guidance_agent/
├── agent/
│   ├── __init__.py
│   └── agent.py
├── data/
│   └── learning_data.json
├── memory/
│   ├── __init__.py
│   └── memory_manager.py
├── tools/
│   ├── __init__.py
│   ├── course_search.py
│   └── learning_path.py
├── utils/
│   ├── __init__.py
│   └── logger.py
├── tests/
│   └── test_tools.py
├── .env.example
├── .gitignore
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

## 14. Assignment Coverage

- Two meaningful tools: yes
- Three tool-selection demonstrations: yes
- Session memory: yes
- Persistent preference: yes
- Failure/fallback: yes
- Trace/log evidence: yes
- Architecture diagram: yes
- LLM Anatomy explanation: documented
- Q/K/V, FFN, residual connection, causal masking and decoding: presentation/documentation topics
- GitHub-ready README: yes

The assignment also requires every member to understand the complete project for the viva.
