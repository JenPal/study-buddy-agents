import time
from typing import Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

class CriticAgent:
    def __init__(self, system_text: str, model: str = "gpt-4o-mini", temperature: float = 0.2):
        self.system_text = system_text
        self.llm = ChatOpenAI(model=model, temperature=temperature)

    def critique(self, question: str, draft_answer: str) -> Dict[str, Any]:
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.system_text),
                ("user", "User question:\n{q}\n\nDraft answer:\n{a}\n\nReturn an improved answer and a bullet summary of changes."),
            ]
        )
        chain = prompt | self.llm
        t0 = time.time()
        resp = chain.invoke({"q": question, "a": draft_answer})
        latency_ms = int((time.time() - t0) * 1000)
        text = resp.content if hasattr(resp, "content") else str(resp)

        improved = text
        critique_summary = "Improvements applied."
        return {
            "improved_answer": improved.strip(),
            "critique_summary": critique_summary,
            "latency_ms": latency_ms,
        }
