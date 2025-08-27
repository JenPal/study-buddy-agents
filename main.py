import os, time, argparse
from dotenv import load_dotenv
from monitor.logger import JSONLLogger
from memory.vector_store import VectorStore
from agents.answer_agent import AnswerAgent
from agents.critic_agent import CriticAgent

def load_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def ensure_vector_store(vdb_dir: str, seed_dir: str):
    vs = VectorStore(persist_dir=vdb_dir)
    # Ingest only if empty directory
    if not os.path.exists(vdb_dir) or not os.listdir(vdb_dir):
        vs.ingest_folder(seed_dir)
    return vs

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Study Buddy Agents: Answer + Critic handoff")
    parser.add_argument("--q", "--question", dest="question", required=True, help="User question")
    parser.add_argument("--k", type=int, default=3, help="Top-k context chunks to retrieve")
    parser.add_argument("--model", default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    parser.add_argument("--log", default=os.getenv("LOG_PATH", "logs/agent_runs.jsonl"))
    parser.add_argument("--vdb", default=os.getenv("VECTOR_DB_DIR", "storage/chroma"))
    parser.add_argument("--seed", default="data/seed_docs")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.log), exist_ok=True)

    logger = JSONLLogger(args.log)

    answer_sys = load_text("prompts/answer_system.txt")
    critic_sys = load_text("prompts/critic_system.txt")

    vs = ensure_vector_store(args.vdb, args.seed)
    context = vs.search(args.question, k=args.k) if args.k > 0 else []

    answer_agent = AnswerAgent(answer_sys, model=args.model)
    critic_agent = CriticAgent(critic_sys, model=args.model)

    t0 = time.time()
    ans = answer_agent.run(args.question, context_chunks=context)
    mid = time.time()
    crit = critic_agent.critique(args.question, ans["final_draft"])

    total_latency = int((time.time() - t0) * 1000)

    record = {
        "user_query": args.question,
        "answer_draft": ans["final_draft"],
        "answer_notes": ans.get("notes", ""),
        "critic_answer": crit["improved_answer"],
        "critique_summary": crit.get("critique_summary", ""),
        "used_context": bool(context),
        "context_snippets": context,
        "latency_ms": total_latency,
        "answer_latency_ms": ans.get("latency_ms", 0),
        "critic_latency_ms": crit.get("latency_ms", 0),
        "model": args.model,
    }
    run_id = logger.log(record)

    print(f"\n=== Study Buddy Agents (run_id: {run_id}) ===")
    print(f"Question: {args.question}")
    print("\n--- Draft answer ---\n")
    print(ans['final_draft'])
    print("\n--- Critic improved answer ---\n")
    print(crit['improved_answer'])
    print("\nContext used:", bool(context))
    print(f"\nTotal latency: {total_latency} ms (answer {ans.get('latency_ms', 0)} ms + critic {crit.get('latency_ms', 0)} ms)\n")

if __name__ == '__main__':
    main()
