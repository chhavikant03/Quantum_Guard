import streamlit as st
from styles import section_header, load_css

st.set_page_config(
    page_title="Quantum Guard",
    page_icon="🛡️",
    layout="wide"
)

# ── Load Global CSS ───────────────────────────────────────────────────────────
st.markdown(load_css(), unsafe_allow_html=True)


st.markdown("""
<style>
@import url('https://api.fontshare.com/v2/css?f[]=satoshi@400,500,700&f[]=cabinet-grotesk@700,800&display=swap');

/* ── Page Background ── */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(145deg, #eef2ff 0%, #f8faff 40%, #f0f4ff 70%, #f5f0ff 100%) !important;
    min-height: 100vh;
}
[data-testid="stHeader"] {
    background: rgba(255,255,255,0.7) !important;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.9);
    box-shadow: 0 1px 12px rgba(99,102,241,0.06);
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.70) !important;
    backdrop-filter: blur(28px) !important;
    -webkit-backdrop-filter: blur(28px) !important;
    border-right: 1px solid rgba(255,255,255,0.80) !important;
    box-shadow: 4px 0 32px rgba(99,102,241,0.07);
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #6b7280 !important;
    font-family: 'Satoshi', sans-serif !important;
}

/* ── Sidebar Dashboard Card ── */
.sidebar-brand-card {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 60%, #a855f7 100%);
    border-radius: 18px;
    padding: 24px 20px;
    margin-bottom: 24px;
    text-align: center;
    box-shadow: 0 8px 32px rgba(99,102,241,0.35);
}
.sidebar-brand-card .brand-title {
    font-family: 'Cabinet Grotesk', 'Satoshi', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: white;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.sidebar-brand-card .brand-sub {
    font-family: 'Satoshi', sans-serif;
    font-size: 12px;
    color: rgba(255,255,255,0.78);
    letter-spacing: 0.5px;
}

/* ── Metric Cards ── */
[data-testid="metric-container"] {
    background: rgba(255,255,255,0.75) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255,255,255,0.95) !important;
    border-radius: 18px !important;
    padding: 20px 18px !important;
    box-shadow: 0 4px 24px rgba(99,102,241,0.09), 0 1px 4px rgba(99,102,241,0.06) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}
[data-testid="metric-container"]:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(99,102,241,0.14) !important;
}
[data-testid="metric-container"] * { color: #6b7280 !important; }
[data-testid="stMetricValue"] {
    font-family: 'Cabinet Grotesk', 'Satoshi', sans-serif !important;
    font-size: 28px !important;
    font-weight: 800 !important;
    color: #4f46e5 !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Satoshi', sans-serif !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    color: #64748b !important;
}
[data-testid="stMetricDelta"] { color: #6366f1 !important; }

/* ── Hero Banner (like screenshot) ── */
.qg-hero-banner {
    background: rgba(255,255,255,0.80);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255,255,255,0.95);
    border-radius: 22px;
    padding: 36px 44px;
    margin-bottom: 28px;
    box-shadow: 0 8px 40px rgba(99,102,241,0.10), 0 2px 8px rgba(99,102,241,0.06);
}
.qg-hero-title {
    font-family: 'Cabinet Grotesk', 'Satoshi', sans-serif;
    font-size: 62px;
    font-weight: 800;
    letter-spacing: -1px;
    background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #0891b2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.1;
    margin-bottom: 8px;
}
.qg-hero-sub {
    font-family: 'Satoshi', sans-serif;
    font-size: 15px;
    color: #64748b;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-weight: 500;
    margin-top: 6px;
}

/* ── Inputs ── */
.stTextInput input, .stTextArea textarea {
    background: rgba(255,255,255,0.80) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(99,102,241,0.20) !important;
    border-radius: 12px !important;
    color: #6b7280 !important;
    font-family: 'Satoshi', sans-serif !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.06) !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: rgba(99,102,241,0.50) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.10) !important;
}
.stTextInput label, .stTextArea label {
    color: #6b7280 !important;
    font-family: 'Satoshi', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}

/* ── Buttons ── */
.stButton > button {
    background: rgba(255,255,255,0.80) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1.5px solid rgba(99,102,241,0.30) !important;
    border-radius: 12px !important;
    color: #4338ca !important;
    font-family: 'Satoshi', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.8px !important;
    padding: 10px 22px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 12px rgba(99,102,241,0.10) !important;
}
.stButton > button:hover {
    background: rgba(99,102,241,0.10) !important;
    border-color: rgba(99,102,241,0.55) !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.18) !important;
    transform: translateY(-1px) !important;
}


/* ── st.code — keep dark bg, force white text ── */
pre, pre *, pre code, pre span {
    color: #ffffff !important;
    font-family: 'JetBrains Mono', 'Courier New', monospace !important;
}
[data-testid="stCodeBlock"] {
    border: 1px solid rgba(99,102,241,0.30) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}



/* ── Alerts ── */
.stAlert {
    background: rgba(255,255,255,0.75) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(99,102,241,0.18) !important;
    border-radius: 12px !important;
    color: #6b7280 !important;
    font-family: 'Satoshi', sans-serif !important;
}

/* ── Radio ── */
.stRadio label { color: #6b7280 !important; font-family: 'Satoshi', sans-serif !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #6366f1 !important; }

/* ── Force all st. text to grey ── */
.stMarkdown p, .stMarkdown li, .stMarkdown ol,
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
.stMarkdown h4, .stMarkdown h5, .stMarkdown h6,
.stText, [data-testid="stText"],
[data-testid="stWrite"] p,
[data-testid="stWrite"] div,
[data-testid="stWrite"] span,
.element-container p,
.element-container span,
.element-container li,
.stAlert p, .stAlert div, .stAlert span,
[data-testid="stSuccess"] p,
[data-testid="stSuccess"] div,
[data-testid="stInfo"] p,
[data-testid="stInfo"] div,
[data-testid="stWarning"] p,
[data-testid="stWarning"] div,
[data-testid="stError"] p,
[data-testid="stError"] div,
.stSelectbox label, .stMultiSelect label,
.stNumberInput label, .stSlider label,
.stRadio label, .stCheckbox label,
.stFileUploader label,
div[data-testid="stVerticalBlock"] p,
div[data-testid="stHorizontalBlock"] p,
.streamlit-expanderHeader,
.streamlit-expanderContent p,
.streamlit-expanderContent span {
    color: #6b7280 !important;
}

/* ── Shield animation ── */
@keyframes revolve {
    0%   { transform: rotateY(0deg); }
    100% { transform: rotateY(360deg); }
}
@keyframes shadow-pulse {
    0%   { transform: scaleX(1); opacity: 0.8; }
    50%  { transform: scaleX(0.3); opacity: 0.3; }
    100% { transform: scaleX(1); opacity: 0.8; }
}
.shield-wrapper { text-align: center; padding: 10px 20px 4px 20px; }
.shield {
    font-size: 64px;
    display: inline-block;
    animation: revolve 2s linear infinite;
    filter: drop-shadow(0 4px 16px rgba(99,102,241,0.25));
}
.shield-shadow {
    width: 50px; height: 8px;
    background: radial-gradient(ellipse, rgba(99,102,241,0.30), transparent);
    border-radius: 50%;
    margin: 0 auto;
    animation: shadow-pulse 2s linear infinite;
}
</style>
""", unsafe_allow_html=True)

# ── Revolving Shield ──────────────────────────────────────────────────────────
st.markdown("""
    <div class="shield-wrapper">
        <span class="shield">🛡️</span>
        <div class="shield-shadow"></div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="sidebar-brand-card">
    <div class="brand-title">DASHBOARD</div>
    <div class="brand-sub">v2.0 | Quantum Guard PQC</div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio(
    "**Navigate to** :",
    ["Home Page", "RSA Encryptor", "RSA Breaker", "Messaging"]
)

if page == "Home Page":

    # Hero Banner — styled like the screenshot's "Quantum Guard" hero card
    st.markdown("""
    <div class="qg-hero-banner">
        <div class="qg-hero-title">Quantum Guard</div>
        <div class="qg-hero-sub">Advanced PQC Secure Gateway</div>
    </div>
    """, unsafe_allow_html=True)

    # About Box
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.72);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border: 1px solid rgba(255,255,255,0.95);
        border-radius: 18px;
        padding: 24px 28px;
        margin-bottom: 24px;
        font-family: 'Satoshi', 'Courier New', monospace;
        color: #6b7280;
        font-size: 16px;
        line-height: 1.9;
        box-shadow: 0 4px 24px rgba(99,102,241,0.08);
    ">
        A next-generation cryptographic dashboard combining classical RSA encryption with Post-Quantum security layers.<br><br>
        This tool was built to demonstrate secure communication between parties using RSA key generation, encryption, decryption, and cryptanalysis — all in one place.<br><br>
        <strong style="color:#4f46e5;">What can you do here?</strong><br>
        1. 🔐 Encrypt messages using RSA<br>
        2. 🔓 Break weak RSA keys using cryptanalysis<br>
        3. 📡 Securely send & receive messages between Sender & Receiver
    </div>
    """, unsafe_allow_html=True)

    # Threat Alert Banner
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.70);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(239,68,68,0.25);
        border-left: 4px solid #ef4444;
        border-radius: 16px;
        padding: 16px 22px;
        margin-bottom: 28px;
        box-shadow: 0 4px 20px rgba(239,68,68,0.07);
    ">
        <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
            <span style="font-size:22px;">⚠️</span>
            <div>
                <div style="font-size:17px; font-weight:700; color:#dc2626;
                            font-family:'Cabinet Grotesk','Satoshi',sans-serif; letter-spacing:0.5px;">
                    QUANTUM THREAT ACTIVE — HARVEST-NOW-DECRYPT-LATER ATTACKS ONGOING
                </div>
                <div style="font-size:15px; color:#6b7280; margin-top:4px;
                            font-family:'Satoshi',sans-serif;">
                    Nation-state actors are recording your encrypted TLS/HTTPS/SSH
                    traffic today. A ~4,000-qubit quantum computer will decrypt it all.
                    <strong style="color:#d97706;">Migration deadline: 2030.</strong>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Key Metrics
    st.markdown(section_header(
        "Threat Intelligence",
        subtitle="Why RSA is broken — by the numbers",
        icon="📡"
    ), unsafe_allow_html=True)

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Qubits to Break RSA-2048", "~4,000", "logical qubits")
    with m2:
        st.metric("Shor's Gate Complexity", "O(n³)", "vs classical O(e^n)")
    with m3:
        st.metric("Kyber Keygen Speed", "500× faster", "than RSA-2048")
    with m4:
        st.metric("PQC Market by 2030", "$857M", "19.8% CAGR")

    st.markdown("<br>", unsafe_allow_html=True)

    # Why Lattice Cryptography
    st.markdown(section_header(
        "Why Lattice Cryptography is Quantum-Safe",
        subtitle="The mathematics that saves us",
        icon="🔬"
    ), unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.72);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid rgba(239,68,68,0.22);
            border-left: 4px solid #ef4444;
            border-radius: 16px;
            padding: 22px;
            box-shadow: 0 4px 24px rgba(239,68,68,0.06);
        ">
            <div style="font-size:18px; font-weight:700; color:#dc2626;
                        font-family:'Cabinet Grotesk','Satoshi',sans-serif; letter-spacing:0.5px;
                        margin-bottom:14px;">
                ⚡ RSA — BROKEN BY QUANTUM
            </div>
            <div style="font-size:15px; color:#6b7280;
                        font-family:'Satoshi',sans-serif; line-height:1.85;">
                • Security based on <strong style="color:#6b7280;">integer factorization hardness</strong><br>
                • Shor's algorithm factors in <strong style="color:#dc2626;">polynomial time</strong><br>
                • Public key (e,n) → private key d <strong style="color:#dc2626;">instantly exposed</strong><br>
                • Every TLS session, SSH key, JWT token <strong style="color:#dc2626;">vulnerable</strong><br>
                • ECC and DH also broken by quantum
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div style="
            background: rgba(255,255,255,0.72);
            backdrop-filter: blur(18px);
            -webkit-backdrop-filter: blur(18px);
            border: 1px solid rgba(16,185,129,0.22);
            border-left: 4px solid #10b981;
            border-radius: 16px;
            padding: 22px;
            box-shadow: 0 4px 24px rgba(16,185,129,0.06);
        ">
            <div style="font-size:18px; font-weight:700; color:#059669;
                        font-family:'Cabinet Grotesk','Satoshi',sans-serif; letter-spacing:0.5px;
                        margin-bottom:14px;">
                🛡️ LATTICE (LWE) — QUANTUM-SAFE
            </div>
            <div style="font-size:15px; color:#6b7280;
                        font-family:'Satoshi',sans-serif; line-height:1.85;">
                • Security based on <strong style="color:#6b7280;">Learning With Errors (LWE)</strong><br>
                • <strong style="color:#059669;">No known quantum speedup</strong> against LWE<br>
                • Proven hard against Shor's, Grover's & all variants<br>
                • NIST FIPS 203/204 — <strong style="color:#059669;">finalised August 2024</strong><br>
                • Deployed by AWS, Cloudflare, Google Chrome
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)



elif page == "RSA Encryptor":

    st.markdown(section_header(
        "RSA Encryptor",
        subtitle="Generate RSA keys and encrypt your message instantly",
        icon="🔐"
    ), unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.72);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(99,102,241,0.18);
        border-radius: 14px;
        padding: 14px 20px;
        margin-bottom: 20px;
        font-family: 'Satoshi', sans-serif;
        font-size: 14px;
        color: #6b7280 !important;
        box-shadow: 0 4px 16px rgba(99,102,241,0.07);
    ">
        Enter your message below and we'll handle the math — prime generation, key creation,
        and encryption using modular exponentiation.
    </div>
    """, unsafe_allow_html=True)

    message = st.text_input("Enter your message")
    e_value = st.text_input("Public Exponent e :")

    if st.button("🔐 ENCRYPT"):
        if message:
            from test2 import generate_keys, encrypt_message
            n, e = generate_keys(e_value if e_value else None)
            cipher = encrypt_message(message, e, n)
            st.success("✅ Encryption Successful!")
            st.write(f"**Public Key (n, e):** {n}, {e}")
            st.write("**Cipher (decimal):**")
            st.code(" ".join(map(str, cipher)))
            st.write("**Cipher (hex):**")
            st.code(" ".join([hex(c) for c in cipher]))
        else:
            st.warning("⚠️ Please enter a message!")



elif page == "RSA Breaker":

    st.markdown(section_header(
        "RSA Breaker",
        subtitle="Cryptanalysis tool — break weak RSA keys",
        icon="🔓"
    ), unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.72);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(239,68,68,0.18);
        border-radius: 14px;
        padding: 14px 20px;
        margin-bottom: 20px;
        font-family: 'Satoshi', sans-serif;
        font-size: 14px;
        color: #6b7280;
        box-shadow: 0 4px 16px rgba(239,68,68,0.06);
    ">
        Given a weak RSA public key (n, e) and ciphertext, this tool factors the modulus to 
        recover the private key and decrypt the original message.<br>
        <strong style="color:#dc2626;">⚠️ For educational purposes only — works on small/weak RSA keys.</strong>
    </div>
    """, unsafe_allow_html=True)

    n = st.text_input("Modulus (n):")
    e = st.text_input("Public Exponent (e):")
    cipher_input = st.text_input("Ciphertext(s):")

    if st.button("🔓 BREAK & DECRYPT"):
        if n and e and cipher_input:
            from sympy import factorint

            n = int(n)
            e = int(e)
            cipher_list = cipher_input.strip().split()

            c_values = []
            for val in cipher_list:
                if val.startswith("0x"):
                    c_values.append(int(val, 16))
                else:
                    c_values.append(int(val))

            with st.spinner("🔍 Factoring modulus n..."):
                factors = factorint(n)
                primes = []
                for p, count in factors.items():
                    primes.extend([p] * count)

            if len(primes) != 2:
                st.error("❌ Invalid RSA modulus!")
            else:
                p, q = primes
                st.success(f"✅ Factored! p = {p}, q = {q}")

                phi = (p - 1) * (q - 1)
                d = pow(e, -1, phi)

                st.info(f"🔑 Private key d = {d}")

                message = ""
                results = []
                for c in c_values:
                    m = pow(c, d, n)
                    if 0 <= m <= 255:
                        char = chr(m)
                        message += char
                        results.append(f"Cipher {c} → {m} → '{char}'")
                    else:
                        results.append(f"Cipher {c} → {m} → Non-ASCII")

                st.write("**Decryption Steps:**")
                for r in results:
                    st.code(r)

                st.success(f"📜 FINAL MESSAGE: {message}")
        else:
            st.warning("⚠️ Please fill all fields!")



elif page == "Messaging":

    st.markdown(section_header(
        "Messenger",
        subtitle="Secure end-to-end encrypted communication",
        icon="📡"
    ), unsafe_allow_html=True)

    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.72);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(16,185,129,0.18);
        border-radius: 14px;
        padding: 14px 20px;
        margin-bottom: 20px;
        font-family: 'Satoshi', sans-serif;
        font-size: 14px;
        color: #6b7280;
        box-shadow: 0 4px 16px rgba(16,185,129,0.06);
    ">
        Messages are encrypted using RSA and wrapped with a Post-Quantum layer via the 
        Quantum Guard gateway. Sender sends, Receiver receives — fully encrypted. 🔒
    </div>
    """, unsafe_allow_html=True)

    server_url = st.text_input("Gateway URL:")
    api_key = st.text_input("API Key:", type="password")

    mode = st.radio("Select Mode:", ["🔵 Send Message", "🔴 Receive Message"])

    if mode == "🔵 Send Message":
        msg = st.text_input("Enter your message:")

        if st.button("📤 SEND"):
            if server_url and api_key and msg:
                import requests
                import json
                from rsa_module import RSAModule

                with st.spinner("🔐 Encrypting & Sending..."):
                    try:
                        pub, priv = RSAModule.generate_64bit_keys()
                        cipher = RSAModule.encrypt(msg, pub['n'], pub['e'])

                        headers = {"x-api-key": api_key}
                        payload = {"rsa_ciphertext": str(cipher)}

                        response = requests.post(f"{server_url}/wrap", json=payload, headers=headers)

                        if response.status_code == 200:
                            pqc_envelope = response.json()
                            demo_packet = {
                                "pqc_payload": pqc_envelope,
                                "rsa_n": pub['n'],
                                "rsa_d": priv['d']
                            }
                            with open("transfer.json", "w") as f:
                                json.dump(demo_packet, f)

                            st.success("✅ Message sent! 'transfer.json' created!")
                            st.info("📁 Share this file with the receiver.")
                        else:
                            st.error(f"❌ Error: {response.json().get('error')}")
                    except Exception as ex:
                        st.error(f"❌ Connection Failed: {ex}")
            else:
                st.warning("⚠️ Please fill all fields!")

    elif mode == "🔴 Receive Message":
        if st.button("📥 RECEIVE"):
            import requests
            import json
            import os
            from rsa_module import RSAModule

            if not os.path.exists("transfer.json"):
                st.error("❌ 'transfer.json' not found! Sender hasn't sent anything yet.")
            else:
                with st.spinner("🔓 Decrypting message..."):
                    try:
                        with open("transfer.json", "r") as f:
                            demo_packet = json.load(f)

                        pqc_packet = demo_packet['pqc_payload']
                        n_val = demo_packet['rsa_n']
                        d_val = demo_packet['rsa_d']

                        headers = {"x-api-key": api_key}
                        response = requests.post(
                            f"{server_url}/unwrap",
                            json={"payload": pqc_packet},
                            headers=headers
                        )

                        if response.status_code == 200:
                            res_data = response.json()
                            recovered_cipher = int(res_data['rsa_ciphertext'])
                            final_msg = RSAModule.decrypt(recovered_cipher, n_val, d_val)
                            st.success(f"🔓 Verified Message: {final_msg}")
                        else:
                            st.error(f"❌ Gateway Error: {response.json().get('error')}")
                    except Exception as ex:
                        st.error(f"❌ Error: {ex}")
