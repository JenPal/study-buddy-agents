# Study Buddy Agents

A tiny multi-agent demo where an **Answer Agent** drafts a response and a **Critic Agent** improves it.
Shows:

- Multi-agent handoff (Answer → Critic)
- Prompt design via clean system prompts
- Retrieval memory with Chroma (via LangChain)
- Simple monitoring with a JSONL log + Streamlit dashboard
- Containerized runnable app

## Quickstart

```bash
git clone https://github.com/your-username/study-buddy-agents.git
cd study-buddy-agents
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # add your OpenAI API key
python main.py --q "How do I use the combined gas law?"

# Monitor logs
streamlit run monitor/streamlit_dashboard.py
```

> First run will build a small vector store from `data/seed_docs` for retrieval.

## Project Layout

```
study-buddy-agents/
│── agents/
│   ├── answer_agent.py         # LLM prompt for draft
│   └── critic_agent.py         # LLM prompt for critique/improve
│── memory/
│   └── vector_store.py         # Chroma store + ingestion/search
│── monitor/
│   ├── logger.py               # JSONL logger
│   └── streamlit_dashboard.py  # quick observability UI
│── prompts/
│   ├── answer_system.txt
│   └── critic_system.txt
│── data/seed_docs/             # tiny sample corpus
│── main.py                     # orchestrates Answer → Critic
│── requirements.txt
│── Dockerfile (optional)
│── .env.example
│── LICENSE
└── README.md
```

## Usage

```bash
python main.py --q "Explain triangle similarity with an example."
python main.py --q "A gas expands from 3.5 L at 86.7 kPa and 20°C to 8.0 L at 56.7 kPa. What's T₂?" --k 2
```

The app will:
1. Retrieve up to `k` context chunks.
2. Generate a draft with **Answer Agent**.
3. Improve it with **Critic Agent**.
4. Log everything to `logs/agent_runs.jsonl`.

Open the **Streamlit dashboard** to inspect runs:
```bash
streamlit run monitor/streamlit_dashboard.py
```

## Config

Configure via `.env`:
- `OPENAI_API_KEY`: your key
- `OPENAI_MODEL`: default `gpt-4o-mini` (adjust as needed)
- `VECTOR_DB_DIR`: default `storage/chroma`
- `LOG_PATH`: default `logs/agent_runs.jsonl`

## Notes

- Prompts are plain text in `prompts/` so you can iterate without touching code.
- The vector store persists on disk; delete the folder to rebuild.
- For demo purposes, the agents return unstructured text; you can switch to structured outputs later.

## Extend

- Add **RAG citations**: include the top sources inline.
- Add **guardrails**: refusal policies; hallucination checks.
- Replace Streamlit with your favorite observability stack.
- Add **FastAPI** endpoint to serve the agent remotely.
- Swap vector DBs (FAISS, PGVector) or embedding models.

## License

MIT
