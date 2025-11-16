import os, requests, pandas as pd
import streamlit as st

API_BASE = os.getenv("API_BASE", "http://localhost:8000")
PORT = int(os.getenv("DASHBOARD_PORT", "8501"))

st.set_page_config(page_title="InsightHub", layout="wide")

st.title("InsightHub — Live Metrics")

colA, colB, colC, colD = st.columns(4)

@st.cache_data(ttl=5.0)
def fetch_series(minutes=15, source=None):
    params = {"minutes": minutes}
    if source:
        params["source"] = source
    r = requests.get(f"{API_BASE}/metrics/series", params=params, timeout=10)
    r.raise_for_status()
    return pd.DataFrame(r.json())

with st.sidebar:
    st.header("Filters")
    minutes = st.slider("Window (minutes)", 5, 120, 30)
    source = st.selectbox("Source", ["(all)", "web-1", "api-1", "worker-1"])
    source_val = None if source == "(all)" else source

try:
    df = fetch_series(minutes=minutes, source=source_val)
    if df.empty:
        st.info("No data yet. Give the generator a few seconds…")
    else:
        df["ts"] = pd.to_datetime(df["ts"])
        df = df.sort_values("ts")

        latest = df.tail(1).iloc[0]
        colA.metric("CPU %", f"{latest['cpu_util']:.1f}")
        colB.metric("Mem %", f"{latest['mem_util']:.1f}")
        colC.metric("Latency ms", f"{latest['latency_ms']:.0f}")
        colD.metric("Error %", f"{latest['error_rate']:.2f}")

        left, right = st.columns(2)
        with left:
            st.line_chart(df.set_index("ts")["cpu_util"], height=260)
            st.line_chart(df.set_index("ts")["latency_ms"], height=260)
        with right:
            st.line_chart(df.set_index("ts")["mem_util"], height=260)
            st.line_chart(df.set_index("ts")["error_rate"], height=260)

        st.subheader("Raw (last 50)")
        st.dataframe(df.tail(50), use_container_width=True)
except Exception as e:
    st.error(f"Dashboard error: {e}")
