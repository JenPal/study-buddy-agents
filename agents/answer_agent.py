import time
from typing import Dict, Any, List, Optional
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class AnswerAgent:
    def __init__(self, system_text: str, model: str = "gpt-4o-mini", temperature: float = 0.2):
        self.system_text = system_text
        self.llm = ChatOpenAI(model=model, temperature=temperature)

    def run(self, question: str, context_chunks: Optional[List[str]] = None) -> Dict[str, Any]:
        ctx = "\n\n".join(context_chunks or [])
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_text),
                ("user", "Question:\n{q}\n\nContext (optional):\n{ctx}\n\nReturn the final draft answer and a short notes string."),
            ]
        )
        chain = prompt | self.llm
        t0 = time.time()
        resp = chain.invoke({"q": question, "ctx": ctx})
        latency_ms = int((time.time() - t0) * 1000)

        text = resp.content if hasattr(resp, "content") else str(resp)
        # heuristic parsing
        final_draft = text
        notes = ""
        return {
            "final_draft": final_draft.strip(),
            "notes": notes,
            "latency_ms": latency_ms,
        }
