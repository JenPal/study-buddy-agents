import json
import time
import os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Study Buddy Agents Monitor", layout="wide")
st.title("Study Buddy Agents Monitor")

log_path = st.sidebar.text_input("Log file path", "logs/agent_runs.jsonl")

@st.cache_data(ttl=5.0)
def load_logs(path):
    rows = []
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            for ln in f:
                ln = ln.strip()
                if not ln:
                    continue
                try:
                    rows.append(json.loads(ln))
                except Exception:
                    pass
    return pd.DataFrame(rows)

df = load_logs(log_path)
st.caption(f"Loaded {len(df)} records from {log_path}")

if not df.empty:
    # Basic columns
    cols = ["timestamp", "user_query", "answer_draft", "critic_answer", "latency_ms", "used_context", "critique_summary"]
    for c in cols:
        if c not in df.columns:
            df[c] = None
    df["when"] = pd.to_datetime(df["timestamp"], unit="s")
    st.dataframe(df[["when", "user_query", "answer_draft", "critic_answer", "latency_ms", "used_context", "critique_summary"]].sort_values("when", ascending=False), use_container_width=True)

    # Simple KPIs
    kpi1, kpi2 = st.columns(2)
    with kpi1:
        st.metric("Total Runs", len(df))
    with kpi2:
        st.metric("Median Latency (ms)", int(df["latency_ms"].median() if "latency_ms" in df else 0))

    # Latency chart
    st.subheader("Latency over time")
    st.line_chart(df.set_index("when")["latency_ms"])

else:
    st.info("No logs yet. Run the app to generate logs.")
