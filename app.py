from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse
from client_store import ClientStore
from wrapper import PQCWrapper
import json, os, datetime
app = FastAPI()
store = ClientStore()
LOG_FILE = "traffic_logs.json"
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_msg = str(exc)
    print(f"[SYSTEM ERROR]: {error_msg}")
    return JSONResponse(
        status_code=400,
        content={"error": "Gateway Processing Error", "message": error_msg},
    )
def log_event(client_name, action):
    entry = {"time": datetime.datetime.now().strftime("%H:%M:%S"), "client": client_name, "action": action}
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")
@app.post("/register")
def reg(name: str): 
    print(f"[*] Onboarding New Entity: {name}")
    client_data = store.register_client(name)
    log_event(name, "REGISTERED (Keys Issued)")
    return client_data
@app.post("/wrap")
async def wrap(request: Request, x_api_key: str = Header(None)):
    sender = store.get_by_api_key(x_api_key)
    if not sender:
        return JSONResponse(status_code=401, content={"error": "Unauthorized: Invalid API Key"})
    data = await request.json()
    rsa_ciphertext = data.get('rsa_ciphertext')
    print(f"[*] Processing WRAP request for {sender['name']}...")
    pqc_envelope = PQCWrapper.wrap(str(rsa_ciphertext), sender)
    log_event(sender['name'], "WRAP (RSA Armored with PQC)")
    return pqc_envelope
@app.post("/unwrap")
async def unwrap(request: Request, x_api_key: str = Header(None)):
    receiver = store.get_by_api_key(x_api_key)
    if not receiver:
        return JSONResponse(status_code=401, content={"error": "Unauthorized: Invalid API Key"})
    data = await request.json()
    payload = data.get('payload')
    sender_name = str(payload.get('sender')).lower().strip()
    print(f"[*] Receiver '{receiver['name']}' is unwrapping packet from '{sender_name}'")
    sender = next((c for c in store.clients.values() if c['name'] == sender_name), None)
    if not sender:
        print(f"ERROR: Sender '{sender_name}' not found in database.")
        return JSONResponse(status_code=400, content={"error": f"Identity Mismatch: Sender '{sender_name}' unknown to gateway."})
    decrypted_rsa = PQCWrapper.unwrap(payload, receiver, sender)
    print(f"SUCCESS: PQC Verification passed for {sender_name}")
    log_event(receiver['name'], f"UNWRAP (Verified {sender_name}'s Signature)")
    return {"rsa_ciphertext": decrypted_rsa}
#uvicorn app:app --host 0.0.0.0 --port 8000