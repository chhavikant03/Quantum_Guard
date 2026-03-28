import streamlit as st
import requests, os, json, time

st.set_page_config(page_title="Quantum Guard Admin", layout="wide")
API_URL = "http://localhost:8000"

st.sidebar.title("🛡️ Admin Panel")
menu = ["1. API Registration", "2. Traffic Monitor"]
choice = st.sidebar.radio("Navigation", menu)

if choice == "1. API Registration":
    st.header("Stage 1: Client Onboarding")
    name = st.text_input("Register Name:")
    if st.button("Generate API Key"):
        res = requests.post(f"{API_URL}/register?name={name}").json()
        st.success(f"Key issued for {name}")
        st.code(res['api_key'])

elif choice == "2. Traffic Monitor":
    st.header("Stage 2: Network Audit")
    placeholder = st.empty()
    while True:
        if os.path.exists("traffic_logs.json"):
            with open("traffic_logs.json", "r") as f:
                
                lines = f.readlines()
                logs = [json.loads(line) for line in lines]
                placeholder.table(logs[::-1])
        time.sleep(1)