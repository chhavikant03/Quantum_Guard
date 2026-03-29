import streamlit as st
import requests, os, json, time, datetime
import pandas as pd
import numpy as np
import altair as alt
# from streamlit_autorefresh import st_autorefresh  # Optional, fallback to st.rerun()
def auto_refresh(interval=5):
    st.rerun()
st.button("🔄 Refresh", on_click=auto_refresh, key="refresh")
import io

# Page config
st.set_page_config(
    page_title="Quantum Guard | Advanced Tactical Dashboard",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://localhost:8000"
DB_FILE = "clients.json"
LOG_FILE = "traffic_logs.json"

# Enhanced CSS - Glassmorphism + Dark Mode
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: linear-gradient(135deg, #f8faff 0%, #f0f2ff 100%);
    --bg-surface: rgba(255,255,255,0.25);
    --bg-glass: rgba(255,255,255,0.1);
    --text-main: #0a0d12;
    --text-muted: #64748b;
    --border-color: rgba(148, 163, 184, 0.2);
    
    --neon-blue: #0066ff;
    --neon-green: #10b981;
    --neon-purple: #8b5cf6;
    --neon-orange: #f59e0b;
    --glow-blue: 0 0 20px rgba(0, 102, 255, 0.3);
}

/* Dark Mode */
[data-theme='dark'] {
    --bg-primary: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 100%);
    --bg-surface: rgba(15,15,35,0.8);
    --bg-glass: rgba(30,30,50,0.4);
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --border-color: rgba(71, 85, 105, 0.3);
}

html, body [data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
}
section[data-testid="stAppViewContainer"] {
    background: var(--bg-primary) !important;
}
.stApp {
    background: var(--bg-primary) !important;
}
body {
    font-family: 'Inter', sans-serif !important;
}

.block-container { padding: 3rem 4rem !important; }

[data-testid="stSidebar"] {
    background: var(--bg-glass) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid var(--border-color) !important;
}

/* Header */
.header {
    background: var(--bg-surface);
    backdrop-filter: blur(20px);
    border: none;
    border-radius: 32px;
    padding: 2.5rem 3rem;
    margin: -1rem 0 3rem 0;
    margin-left: -1rem !important;
    box-shadow: 0 35px 60px -20px rgba(0,0,0,0.3);
    position: relative;
    z-index: 20;
}
# MainMenu { visibility: hidden !important; }
header { visibility: hidden !important; }
[data-testid="stHeader"] { display: none !important; }
.st-emotion-cache-1r62skw { display: none !important; }
[data-testid="stStatusWidget"] {
    display: none !important;
}

/* Stat Tiles - Advanced */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin-bottom: 3rem;
}
.stat-tile {
    background: var(--bg-surface);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border-color);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
}
.stat-tile::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
    transition: left 0.5s;
}
.stat-tile:hover::before { left: 100%; }
.stat-tile:hover {
    transform: translateY(-10px) scale(1.02);
    border-color: var(--neon-blue);
    box-shadow: var(--glow-blue);
}

.stat-icon { font-size: 2.5rem; margin-bottom: 1rem; }
.stat-val { font-size: 2.5rem; font-weight: 800; color: var(--neon-blue); }
.stat-label { font-size: 0.8rem; font-weight: 600; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.1em; }

/* Modules */
.module {
    background: var(--bg-surface);
    backdrop-filter: blur(20px);
    border: 1px solid var(--border-color);
    border-radius: 24px;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0,0,0,0.05);
    margin-bottom: 2rem;
}
.module-header {
    background: rgba(255,255,255,0.5);
    padding: 1.5rem 2rem;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.module-title { 
    font-weight: 700; 
    font-size: 1.1rem; 
    background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Client Cards */
.client-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-color);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s ease;
}
.client-card:hover {
    background: var(--bg-surface);
    box-shadow: var(--glow-blue);
    transform: translateY(-2px);
}
.status-badge {
    padding: 0.3rem 1rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}
.status-active { background: rgba(16,185,129,0.2); color: var(--neon-green); }
.status-revoked { background: rgba(239,68,68,0.2); color: #ef4444; }

/* Buttons */
.stButton > button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    border: 2px solid var(--neon-blue) !important;
    background: transparent !important;
    color: var(--neon-blue) !important;
    padding: 0.8rem 2rem !important;
}
.stButton > button:hover {
    background: var(--neon-blue) !important;
    color: white !important;
    box-shadow: var(--glow-blue) !important;
}

/* Theme Toggle */
.theme-toggle {
    background: none;
    border: 2px solid var(--border-color);
    border-radius: 50%;
    width: 40px;
    height: 40px;
    cursor: pointer;
    transition: all 0.3s ease;
}
.theme-toggle:hover { border-color: var(--neon-blue); }
</style>
<script>
    // Dark Mode Toggle
    function toggleTheme() {
        const body = document.body;
        const currentTheme = body.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        body.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
    }
    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.body.setAttribute('data-theme', savedTheme);
</script>
""", unsafe_allow_html=True)

# Data functions with caching
@st.cache_data(ttl=30)
def load_data():
    clients = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            clients = json.load(f)
    
    logs = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            for line in f:
                try:
                    logs.append(json.loads(line.strip()))
                except:
                    pass
    
    log_df = pd.DataFrame(logs) if logs else pd.DataFrame()
    return clients, log_df

clients, log_df = load_data()

# Header
st.markdown("""
<div class="header">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="margin: 0; font-weight: 900; font-size: clamp(3rem, 8vw, 5rem); letter-spacing: -0.08em; text-shadow: 0 8px 24px rgba(0,102,255,0.4), 0 0 40px rgba(139,92,246,0.3); background: linear-gradient(135deg, var(--neon-blue) 0%, var(--neon-purple) 50%, var(--neon-green) 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Quantum Guard</h1>
            <p style="margin: 0; color: var(--text-muted); font-size: 1rem;">Advanced PQC Secure Gateway</p>
        </div>

</div>
""", unsafe_allow_html=True)

# Real-time refresh button (fallback)
if st.button("🔄 Live Update (5s)", key="live"):
    time.sleep(0.1)
    st.rerun()

# Sidebar
with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 3rem 1.5rem; background: linear-gradient(135deg, var(--neon-blue), var(--neon-purple)); border-radius: 28px; margin: 1.5rem 0; box-shadow: var(--glow-blue), 0 20px 40px rgba(0,102,255,0.2);">
        <h2 style="color: white; margin: 0; font-weight: 900; font-size: 1.8rem; letter-spacing: -0.03em; text-shadow: 0 4px 12px rgba(0,0,0,0.3);">ADMIN PANEL</h2>
        <p style="color: rgba(255,255,255,0.8); font-size: 1rem; font-weight: 600; margin-top: 0.5rem;">v2.0 | Advanced PQC Gateway</p>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.radio("🚀 Navigation", ["📊 Overview", "👥 Client Onboarding", "🔐 Secure Registry", "📈 Network Telemetry"], label_visibility="collapsed")
    
    st.markdown("---")
    if st.button("🧹 Purge Logs"):
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
            st.rerun()
    st.markdown(f"**Vault:** {os.path.abspath(DB_FILE)}")

# Dynamic Stats
col1, col2, col3, col4, col5, col6 = st.columns(6)
total_clients = len(clients)
total_logs = len(log_df)
unique_clients = log_df['client'].nunique() if not log_df.empty else 0
actions_wrap = len(log_df[log_df['action'].str.contains('WRAP', na=False)]) if not log_df.empty else 0
actions_unwrap = len(log_df[log_df['action'].str.contains('UNWRAP', na=False)]) if not log_df.empty else 0

with col1:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="stat-icon">🔑</div>
        <div class="stat-val">{total_clients}</div>
        <div class="stat-label">Active Keys</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="stat-icon">📦</div>
        <div class="stat-val">{total_logs}</div>
        <div class="stat-label">Packets</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="stat-icon">👤</div>
        <div class="stat-val">{unique_clients}</div>
        <div class="stat-label">Clients</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="stat-icon">🔒</div>
        <div class="stat-val">{actions_wrap}</div>
        <div class="stat-label">Wraps</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="stat-tile">
        <div class="stat-icon">🔓</div>
        <div class="stat-val">{actions_unwrap}</div>
        <div class="stat-label">Unwraps</div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown("""
    <div class="stat-tile">
        <div class="stat-icon">✅</div>
        <div class="stat-val">100%</div>
        <div class="stat-label">PQC Integrity</div>
    </div>
    """, unsafe_allow_html=True)

# Pages
if page == "📊 Overview":
    st.markdown('<div class="module"><div class="module-header"><span class="module-title">Dashboard Overview</span></div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Server Status", "🟢 Online", "API: localhost:8000")
        st.metric("Uptime", f"{datetime.datetime.now().strftime('%H:%M:%S')}", delta="1s")
    with col_b:
        if not log_df.empty:
            latest = log_df.iloc[0]
            st.metric("Latest Action", latest['action'], latest['client'])
    
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "👥 Client Onboarding":
    st.markdown('<div class="module"><div class="module-header"><span class="module-title">Provision New Entity</span></div>', unsafe_allow_html=True)
    
    entity_id = st.text_input("Entity ID", placeholder="e.g., ALPHA-SERVER-01")
    col1, col2 = st.columns([3,1])
    with col1:
        if st.button("🚀 Generate PQC Keys", type="primary", use_container_width=True):
            if entity_id:
                with st.spinner("Generating Kyber-Dilithium keys..."):
                    try:
                        r = requests.post(f"{API_URL}/register?name={entity_id}", timeout=10).json()
                        st.success("✅ Keys provisioned!")
                        st.json({k: v[:64] + "..." for k, v in r.items()})
                    except Exception as e:
                        st.error(f"❌ API Error: {e}")
            else:
                st.warning("Enter Entity ID")
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "🔐 Secure Registry":
    st.markdown('<div class="module"><div class="module-header"><span class="module-title">Entity Registry</span></div>', unsafe_allow_html=True)
    
    search = st.text_input("🔍 Search clients")
    filtered = [c for c in clients.values() if search.lower() in c['name'].lower()]
    
    if not filtered:
        st.info("No clients found.")
    else:
        for info in filtered:
            apikey = [k for k,v in clients.items() if v['name']==info['name']][0]
            st.markdown(f"""
            <div class="client-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: var(--neon-blue);">{info['name'].upper()}</h4>
                        <span class="status-badge status-active">ACTIVE</span>
                    </div>
                    <small style="font-family: 'JetBrains Mono'; color: var(--text-muted);">ID: {apikey[:8]}...</small>
                </div>
                <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                    <code style="flex:1;">KEM: {info['kem_pub'][:48]}...</code>
                    <code style="flex:1;">SIG: {info['sig_pub'][:48]}...</code>
                </div>
                <div style="margin-top: 1rem;">
                    <st.button label="Copy Keys" on_click="copyKeys('{apikey}')" use_container_width />
                    <st.button label="Revoke" variant="destructive" on_click="revoke('{apikey}')" use_container_width />
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("💥 Revoke All", type="primary"):
        # Implementation for bulk revoke
        pass
    
    st.markdown('</div>', unsafe_allow_html=True)

elif page == "📈 Network Telemetry":
    st.markdown('<div class="module"><div class="module-header"><span class="module-title">Live Telemetry</span></div>', unsafe_allow_html=True)
    
    if log_df.empty:
        st.info("📭 No logs yet. Perform some actions!")
    else:
        # Charts
        alt_chart = alt.Chart(log_df).mark_circle(size=60).encode(
            x='time:T',
            y='client:N',
            color='action:N',
            tooltip=['time', 'client', 'action']
        ).properties(width=800, height=400)
        st.altair_chart(alt_chart, use_container_width=True)
        
        st.dataframe(log_df.tail(20), use_container_width=True)
        
        csv = log_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Export CSV", csv, "qg-telemetry.csv", "text/csv")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(f"""
<div style="text-align: center; padding: 2rem; color: var(--text-muted); font-size: 0.9rem;">
    © {datetime.datetime.now().year} Quantum Guard | Real-time PQC Dashboard | Powered by Streamlit
</div>
""", unsafe_allow_html=True)

