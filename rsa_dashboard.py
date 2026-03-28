import streamlit as st 

st.set_page_config(
    page_title="Quantum Guard",
    layout="wide"
)
 #crazy animation -----------------
st.markdown("""
    <style>
    @keyframes revolve {
        0%   { transform: rotateY(0deg); }
        100% { transform: rotateY(360deg); }
    }
    @keyframes shadow-pulse {
        0%   { transform: scaleX(1); opacity: 0.8; }
        50%  { transform: scaleX(0.3); opacity: 0.3; }
        100% { transform: scaleX(1); opacity: 0.8; }
    }
    .shield-wrapper {
        text-align: center;
        padding: 20px;
    }
    .shield {
        font-size: 80px;
        display: inline-block;
        animation: revolve 2s linear infinite;
    }
    .shield-shadow {
        width: 60px;
        height: 10px;
        background: radial-gradient(ellipse, #c0c0c0, transparent);
        border-radius: 50%;
        margin: 0 auto;
        animation: shadow-pulse 2s linear infinite;
    }
    </style>
    <div class="shield-wrapper">
        <span class="shield">🛡️</span>
        <div class="shield-shadow"></div>
    </div>
""", unsafe_allow_html=True)


#sidebar ---------------
st.sidebar.title("Dashboard")
page = st.sidebar.radio("**Navigate to:**", ["Home Page", "RSA Encryptor", "RSA Breaker"])

#Home page ----------
if page == "Home Page":
    #--Hero section
    st.markdown("""
    <div style= "text-align:center;
                padding : 0px 20px 30px 20px;">
    <div style = "
                font-size : 70px;
                font-weight : 900;
                letter-spacing:6px;
                background: linear-gradient(135deg, #00d4ff 0%, #a855f7 50%, #00ff88 100%);
                -webkit-background-clip: text ; 
                -webkit-text-fill-color:transparent;
                font-family: sans-serif;
                line-height: 1.1;">
                QUANTUM GUARD </div>
    <div style = "
                font-size:21px;
                color : white;
                letter-spacing: 4px
                text-transform: uppercase
                margin-top:8px
                font-family:8px
                font-weight:100"> 
                Post Quantum Cryptography Defence System
                </div>
    </div>

""", unsafe_allow_html=True)
#about box --------------
    st.markdown("""
    <div style ="
                font-size:16.5px;
                font-weight:380;
                line-height:1.9;
                background:rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 14px;
                padding : 24px 28px;
                margin-bottom: 24px;
                font-family: 'Courier New', monospace;
                color:white;
                ">
                A next-generation cryptographic dashboard combining classical RSA encryption with Post-Quantum security layers.<br>
            This tool was built to demonstrate secure communication between parties using RSA key generation, encryption, decryption, and cryptanalysis — all in one place.<br><br>
            <strong style="color:#00d4ff;">What can you do here?</strong><br>
            1. 🔐 Encrypt messages using RSA<br>
            2. 🔓 Break weak RSA keys using cryptanalysis<br>
            3. 📡 Securely send & receive messages between Sender & Receiver</div>
    """, unsafe_allow_html=True)

#rsa encryptor----------
elif page == "RSA Encryptor":
    st.markdown("""
    <div style= "text-align:center;
                padding : 0px 20px 30px 20px;">
        <div style = "
                font-size : 55px;
                font-weight : 900;
                letter-spacing:6px;
                background: linear-gradient(135deg, #00d4ff 0%, #a855f7 50%, #00ff88 100%);
                -webkit-background-clip: text ; 
                -webkit-text-fill-color:transparent;
                font-family: sans-serif;
                line-height: 1.1;">
                RSA Encryptor </div>
    """, unsafe_allow_html=True)
    message = st.text_input("Enter Your Message:")
    e_value = st.text_input("Enter Public Exponent e: ")

    if st.button("ENCRYPT"):
        if message:
            from encryptor import generate_keys, encrypt_message
            n, e = generate_keys(e_value if e_value else None)
            cipher = encrypt_message(message, e, n)
            st.success("Encryption Successful!")
            st.write(f"**Public Key (n, e):** {n}, {e}")
            st.write("**Cipher (decimal):**")
            st.code(" ".join(map(str, cipher)))
            st.write("**Cipher (hex):**")
            st.code(" ".join([hex(c) for c in cipher]))
        else:
            st.warning("⚠️ Please enter a message!")

#rsa breaker---------
elif page == "RSA Breaker":
    st.markdown("""
<div style= "text-align:center;
                padding : 0px 20px 30px 20px;">
        <div style = "
                font-size : 55px;
                font-weight : 900;
                letter-spacing:6px;
                background: linear-gradient(135deg, #00d4ff 0%, #a855f7 50%, #00ff88 100%);
                -webkit-background-clip: text ; 
                -webkit-text-fill-color:transparent;
                font-family: sans-serif;
                line-height: 1.1;">
                RSA Breaker </div>
    """, unsafe_allow_html=True)

    n = st.text_input("Modulus (n):")
    e = st.text_input("Public Exponent (e):")
    cipher_input = st.text_input("Ciphertext(s):")

    if st.button("DECRYPT"):
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

            with st.spinner("Factoring modulus n"):
                factors = factorint(n)
                primes = []
                for p, count in factors.items():
                    primes.extend([p] * count)

            if len(primes) != 2:
                st.error("Invalid RSA modulus!")
            else:
                p, q = primes
                st.success(f"Factored! p = {p}, q = {q}")

                phi = (p - 1) * (q - 1)
                d = pow(e, -1, phi)

                st.info(f"Private key d = {d}")

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

                st.success(f"FINAL MESSAGE: {message}")
        else:
            st.warning("Please fill all fields!")


#messenger---------------
