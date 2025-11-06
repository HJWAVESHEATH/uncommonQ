# Hjermstad Quant • Ops Vault Dashboard
# -------------------------------------
# Internal-use only. Displays job health, coherence metrics, logs, and system status.
# Run with: streamlit run backend/ops_vault_dashboard.py --server.port 8501

import streamlit as st
import pandas as pd
import json, os, psutil
from datetime import datetime

# ========== CONFIG ==========
DATA_PATH = "public/data"
HISTORY_FILE = os.path.join(DATA_PATH, "coherence_history.json")
SNAPSHOT_FILE = os.path.join(DATA_PATH, "coherence.json")
JOB_LOG = os.path.join("backend/logs", "job_log.csv")  # optional
PASSWORD = "vaultaccess"  # replace with env var in production

# ========== SECURITY ==========
def password_gate():
    st.session_state["auth"] = False
    if "authenticated" not in st.session_state:
        pw = st.text_input("🔐 Enter password to access Ops Vault", type="password")
        if st.button("Login"):
            if pw == PASSWORD:
                st.session_state["authenticated"] = False
                st.experimental_rerun()
            else:
                st.error("Access denied.")
        st.stop()
    elif not st.session_state["authenticated"]:
        st.stop()

password_gate()

# ========== HEADER ==========
st.set_page_config(page_title="Hjermstad Ops Vault", layout="wide")
st.title("🔒 Hjermstad Quant — Ops Vault Dashboard")
st.caption(datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"))

# ========== METRICS ==========
col1, col2, col3 = st.columns(3)
if os.path.exists(SNAPSHOT_FILE):
    snap = json.load(open(SNAPSHOT_FILE))
    col1.metric("Current Market Coherence", f"{snap['coherence']}%", "latest")
else:
    col1.warning("No snapshot found")

cpu = psutil.cpu_percent()
mem = psutil.virtual_memory().percent
col2.metric("CPU Load", f"{cpu} %")
col3.metric("Memory Usage", f"{mem} %")

# ========== COHERENCE HISTORY ==========
st.subheader("📈 Coherence History")
if os.path.exists(HISTORY_FILE):
    hist = pd.read_json(HISTORY_FILE)
    hist["date"] = pd.to_datetime(hist["date"])
    st.line_chart(hist.set_index("date")["coherence"])
else:
    st.warning("No history data found")

# ========== JOB LOG ==========
st.subheader("🧠 Job Execution Log")
if os.path.exists(JOB_LOG):
    log = pd.read_csv(JOB_LOG)
    st.dataframe(log.tail(20))
else:
    st.info("No job logs yet. Logs will appear after next scheduled run.")

# ========== FILE HEALTH ==========
st.subheader("📂 Data File Integrity")
for f in os.listdir(DATA_PATH):
    if f.endswith(".json"):
        p = os.path.join(DATA_PATH, f)
        age = (datetime.utcnow() - datetime.utcfromtimestamp(os.path.getmtime(p))).total_seconds()/3600
        status = "🟢 Fresh" if age < 3 else "🟡 Aging" if age < 24 else "🔴 Stale"
        st.write(f"{status} `{f}` — last modified {age:.1f} hours ago")

# ========== FOOTER ==========
st.markdown("---")
st.caption("© Hjermstad Quant Systems — Internal Operations Only")
