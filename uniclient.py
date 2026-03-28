import requests
import json
import os
import time
import datetime
import threading
import base64
from rsa_module import RSAModule
from fastapi import FastAPI, Request
import uvicorn

# ══════════════════════════════════════════════════════════════════════════════
#  INTERNAL LISTENER (BACKGROUND THREAD)
# ══════════════════════════════════════════════════════════════════════════════
app = FastAPI()

@app.post("/receive")
async def handle_incoming_packet(request: Request):
    """Background endpoint to catch incoming PQC packets via ngrok on Port 8001"""
    try:
        data = await request.json()
        # Save as transfer.json for the main thread to pick up
        with open("transfer.json", "w") as f:
            json.dump(data, f, indent=4)
        return {"status": "SUCCESS", "node": "QUANTUM_GUARD_NODE"}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def run_listener():
    """Starts the PQC listener on Port 8001 (Avoiding Port 8000 conflict)"""
    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="error")

# ══════════════════════════════════════════════════════════════════════════════
#  CLIENT UI & TACTICAL LOGIC
# ══════════════════════════════════════════════════════════════════════════════
def display_packet(data, title="PQC DATA INSPECTION"):
    """Displays raw JSON to prove data is dynamic and real"""
    print(f"\n{'='*60}")
    print(f"🛰️  {title}")
    print(f"{'='*60}")
    # Truncate long base64 strings for readability in the console
    clean_data = json.loads(json.dumps(data))
    if 'file_data' in clean_data:
        clean_data['file_data'] = clean_data['file_data'][:50] + "... [TRUNCATED]"
    print(json.dumps(clean_data, indent=4))
    print(f"{'='*60}\n")

def main():
    # Initialize the background listener thread
    listener_thread = threading.Thread(target=run_listener, daemon=True)
    listener_thread.start()

    print("""
    ░░▒▒▓▓ ████████████████████████████████████████████████ ██ ▓▓▒▒░░
    ░░▒▒▓▓ █                                              █ ▓▓▒▒░░
    ░░▒▒▓▓ █   QUANTUM GUARD: UNIFIED TACTICAL CLIENT     █ ▓▓▒▒░░
    ░░▒▒▓▓ █      [ SECURE MESSAGE & FILE TRANSFER ]      █ ▓▓▒▒░░
    ░░▒▒▓▓ █                                              █ ▓▓▒▒░░
    ░░▒▒▓▓ ████████████████████████████████████████████████ ██ ▓▓▒▒░░
    """)
    print("📡 System: Background Listener Active on Port 8001")
    
    server_url = input("🔗 Enter PQC Gateway URL (ngrok): ").strip("/")
    api_key = input("🔑 Enter X-API-KEY: ").strip()

    while True:
        print("\n[ STRATEGIC COMMAND MENU ]")
        print("1 — [SEND MESSAGE]  Encrypt & Push Text")
        print("2 — [SEND FILE]     Encrypt & Push File")
        print("3 — [RECEIVE/WAIT]  Process Incoming Signal")
        print("4 — [EXIT]          Terminate Node")
        choice = input("\nSELECT ACTION: ")

        if choice in ['1', '2']:
            rec_url = input(f"[{'SENDER'}] Enter Receiver's ngrok URL: ").strip("/")
            content = ""
            filename = "N/A"
            
            if choice == '1':
                content = input("[SENDER] Enter secret message: ")
            else:
                path = input("[SENDER] Enter file path: ")
                if not os.path.exists(path):
                    print("❌ Error: File not found.")
                    continue
                filename = os.path.basename(path)
                with open(path, "rb") as f:
                    content = base64.b64encode(f.read()).decode()

            print("\n[*] Initializing Hybrid RSA-PQC Handshake...")
            pub, priv = RSAModule.generate_64bit_keys()
            cipher = RSAModule.encrypt(content, pub['n'], pub['e'])
            
            headers = {"x-api-key": api_key}
            payload = {"rsa_ciphertext": str(cipher)}
            
            try:
                # Protective PQC wrapping against Shor's algorithm
                response = requests.post(f"{server_url}/wrap", json=payload, headers=headers)
                if response.status_code == 200:
                    pqc_envelope = response.json()
                    
                    demo_packet = {
                        "pqc_payload": pqc_envelope,
                        "rsa_n": pub['n'],
                        "rsa_d": priv['d'],
                        "metadata": {
                            "type": "MESSAGE" if choice == '1' else "FILE",
                            "filename": filename,
                            "timestamp": str(datetime.datetime.now())
                        }
                    }
                    
                    display_packet(demo_packet, "OUTGOING TACTICAL PAYLOAD")
                    
                    print(f"[*] Pushing to {rec_url}...")
                    push_res = requests.post(f"{rec_url}/receive", json=demo_packet, timeout=15)
                    if push_res.status_code == 200:
                        print("✅ SUCCESS: Handshake confirmed by peer.")
                else:
                    print(f"❌ Gateway Error: {response.json().get('error')}")
            except Exception as e:
                print(f"❌ Connection Error: {e}")

        elif choice == '3':
            if not os.path.exists("transfer.json"):
                print("\n⏳ Monitoring local interface... (No signals detected)")
                continue

            print("\n🚀 [SIGNAL ACQUIRED] Decoding PQC Signal...")
            with open("transfer.json", "r") as f:
                demo_packet = json.load(f)
            
            display_packet(demo_packet, "INCOMING SIGNAL ANALYSIS")
            
            print("[*] Requesting PQC Decapsulation from Gateway...")
            headers = {"x-api-key": api_key}
            try:
                response = requests.post(f"{server_url}/unwrap", json={"payload": demo_packet['pqc_payload']}, headers=headers)
                
                if response.status_code == 200:
                    recovered_cipher = int(response.json()['rsa_ciphertext'])
                    final_data = RSAModule.decrypt(recovered_cipher, demo_packet['rsa_n'], demo_packet['rsa_d'])
                    
                    if demo_packet['metadata']['type'] == "FILE":
                        orig_name = "recovered_" + demo_packet['metadata']['filename']
                        with open(orig_name, "wb") as f:
                            f.write(base64.b64decode(final_data))
                        print(f"\n🔓 [FILE RECOVERED]: Saved as '{orig_name}'")
                    else:
                        print(f"\n🔓 [VERIFIED MESSAGE]: {final_data}")
                    
                    os.remove("transfer.json") 
                else:
                    print(f"❌ Gateway Error: {response.json().get('error')}")
            except Exception as e:
                print(f"❌ Decapsulation Error: {e}")

        elif choice == '4':
            print("System Offline.")
            break

if __name__ == "__main__":
    main()
