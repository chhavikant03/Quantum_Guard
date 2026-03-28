import json, os, oqs, secrets
DB_FILE = "clients.json"
class ClientStore:
    def __init__(self):
        self.clients = self._load()
    def _load(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    def _save(self):
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.clients, f, indent=4)
    def register_client(self, name):
        name_lower = name.lower().strip()
        self.clients = {k: v for k, v in self.clients.items() if v['name'] != name_lower}
        api_key = secrets.token_hex(16)
        with oqs.KeyEncapsulation("Kyber512") as kem:
            pk_kem = kem.generate_keypair().hex()
            sk_kem = kem.export_secret_key().hex()
        with oqs.Signature("Dilithium2") as sig:
            pk_sig = sig.generate_keypair().hex()
            sk_sig = sig.export_secret_key().hex()
        client_data = {
            "name": name_lower,
            "api_key": api_key,
            "kem_pub": pk_kem,
            "kem_priv": sk_kem,
            "sig_pub": pk_sig,
            "sig_priv": sk_sig
        }
        self.clients[api_key] = client_data
        self._save()
        return client_data
    def get_by_api_key(self, api_key):
        return self.clients.get(api_key)