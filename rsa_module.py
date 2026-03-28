import random
from sympy import isprime, mod_inverse
class RSAModule:
    @staticmethod
    def generate_64bit_keys():
        def gen_prime():
            while True:
                p = random.getrandbits(32)
                if isprime(p): return p
        while True:
            try:
                p, q = gen_prime(), gen_prime()
                n = p * q
                phi = (p - 1) * (q - 1)
                e = 65537
                d = mod_inverse(e, phi)
                return {"n": n, "e": e}, {"n": n, "d": d}
            except:
                continue
    @staticmethod
    def encrypt(message, n, e):
        m_int = int.from_bytes(message.encode('utf-8'), 'big')
        return pow(m_int, e, n)

    @staticmethod
    def decrypt(cipher_int, n, d):
        m_int = pow(cipher_int, d, n)
        return m_int.to_bytes((m_int.bit_length() + 7) // 8, 'big').decode('utf-8')
