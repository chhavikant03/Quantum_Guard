import requests
import json
import os
from rsa_module import RSAModule

def main():
    print("""
🛡️ QUANTUM GUARD: AUTO-TRANSFER CLIENT
---------------------------------------
    """)
    
    server_url = input("Enter Gateway URL: ").strip("/")
    api_key = input("Enter your X-API-KEY: ").strip()
    API_BASE = server_url

    print("\nSelect Mode:")
    print("1 - [ALICE] Send Message (Saves to file)")
    print("2 - [BOB]   Receive Message (Reads from file)")
    mode = input("\nChoice: ")

    if mode == '1':
        msg = input("\nAlice, enter message: ")
        
        # 1. RSA Layer
        pub, priv = RSAModule.generate_64bit_keys()
        cipher = RSAModule.encrypt(msg, pub['n'], pub['e'])
        
        # 2. PQC Layer
        headers = {"x-api-key": api_key}
        payload = {"rsa_ciphertext": str(cipher)}
        
        try:
            response = requests.post(f"{API_BASE}/wrap", json=payload, headers=headers)
            if response.status_code == 200:
                pqc_envelope = response.json()
                
                # Create a "Demo Packet" with PQC data + RSA keys for Bob
                demo_packet = {
                    "pqc_payload": pqc_envelope,
                    "rsa_n": pub['n'],
                    "rsa_d": priv['d']
                }
                
                # SAVE TO FILE
                with open("transfer.json", "w") as f:
                    json.dump(demo_packet, f)
                
                print("\n✅ SUCCESS: 'transfer.json' created!")
                print("Give this file to Bob.")
            else:
                print(f"❌ Error: {response.json().get('error')}")
        except Exception as e:
            print(f"❌ Connection Failed: {e}")

    elif mode == '2':
        if not os.path.exists("transfer.json"):
            print("❌ Error: 'transfer.json' not found! Alice hasn't sent anything.")
            return

        print("\n[*] Loading 'transfer.json'...")
        with open("transfer.json", "r") as f:
            demo_packet = json.load(f)
            
        # Extract data
        pqc_packet = demo_packet['pqc_payload']
        n_val = demo_packet['rsa_n']
        d_val = demo_packet['rsa_d']
        
        # 3. Request Unwrap from Gateway
        headers = {"x-api-key": api_key}
        try:
            # We send the 'pqc_payload' part to the API
            response = requests.post(f"{API_BASE}/unwrap", json={"payload": pqc_packet}, headers=headers)
            
            if response.status_code == 200:
                res_data = response.json()
                recovered_cipher = int(res_data['rsa_ciphertext'])
                
                # 4. Final RSA Decrypt
                final_msg = RSAModule.decrypt(recovered_cipher, n_val, d_val)
                print(f"\n🔓 [VERIFIED MESSAGE]: {final_msg}")
            else:
                print(f"❌ Gateway Error: {response.json().get('error')}")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
