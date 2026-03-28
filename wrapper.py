import oqs, os, re
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
class PQCWrapper:
    @staticmethod
    def _clean_hex(hex_str):
        if not hex_str: return ""
        return re.sub(r'[^0-9a-fA-F]', '', str(hex_str))
    @staticmethod
    def wrap(rsa_ciphertext, sender_data):
        kem_pk = bytes.fromhex(PQCWrapper._clean_hex(sender_data['kem_pub']))
        with oqs.KeyEncapsulation("Kyber512") as kem:
            pqc_cipher, shared_secret = kem.encap_secret(kem_pk)
        aes_key = shared_secret[:32]
        nonce = os.urandom(12)
        cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        clean_rsa = str(rsa_ciphertext).strip()
        wrapped_data = encryptor.update(clean_rsa.encode('utf-8')) + encryptor.finalize()
        tag = encryptor.tag
        sig_sk = bytes.fromhex(PQCWrapper._clean_hex(sender_data['sig_priv']))
        with oqs.Signature("Dilithium2", secret_key=sig_sk) as sig:
            signature = sig.sign(wrapped_data).hex()
        return {
            "wrapped_data": wrapped_data.hex(),
            "nonce": nonce.hex(),
            "tag": tag.hex(),
            "pqc_cipher": pqc_cipher.hex(),
            "signature": signature,
            "sender": sender_data['name']
        }
    @staticmethod
    def unwrap(payload, receiver_data, sender_data):
        sig_pk = bytes.fromhex(PQCWrapper._clean_hex(sender_data['sig_pub']))
        clean_data = bytes.fromhex(PQCWrapper._clean_hex(payload['wrapped_data']))
        clean_sig = bytes.fromhex(PQCWrapper._clean_hex(payload['signature']))
        with oqs.Signature("Dilithium2") as sig:
            if not sig.verify(clean_data, clean_sig, sig_pk):
                raise Exception("Dilithium Verification Failed: Identity Mismatch!")
        kem_sk = bytes.fromhex(PQCWrapper._clean_hex(sender_data['kem_priv']))
        pqc_cipher = bytes.fromhex(PQCWrapper._clean_hex(payload['pqc_cipher']))
        with oqs.KeyEncapsulation("Kyber512", secret_key=kem_sk) as kem:
            shared_secret = kem.decap_secret(pqc_cipher)
        aes_key = shared_secret[:32]
        nonce = bytes.fromhex(PQCWrapper._clean_hex(payload['nonce']))
        tag = bytes.fromhex(PQCWrapper._clean_hex(payload['tag']))
        try:
            cipher = Cipher(algorithms.AES(aes_key), modes.GCM(nonce, tag), backend=default_backend())
            decryptor = cipher.decryptor()
            return (decryptor.update(clean_data) + decryptor.finalize()).decode('utf-8')
        except Exception:
            raise Exception("AES Decryption Failed: Invalid Key or Tag. Ensure keys are fresh!")