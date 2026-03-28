import random
def is_prime(n):
    if n < 2:
        return False
    # Check for factors up to the square root of n
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True
def generate_prime(bits=32):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a
def generate_keys(e_value=None):
    while True:
        p = generate_prime(32)
        q = generate_prime(32)
        if p != q:
            break
    n = p * q
    phi = (p - 1) * (q - 1)
    if e_value:
        e = int(e_value)
        if gcd(e, phi) != 1:
            raise ValueError("The provided 'e' is not coprime with phi(n). Try a different value.")
    else:
        e = 65537
    return n, e
def encrypt_message(message, e, n):
    encrypted = []
    for char in message:
        m = ord(char)
        if m >= n:
            raise ValueError(f"Character '{char}' (val: {m}) is too large for modulus n.")
        c = pow(m, e, n)
        encrypted.append(c)
    return encrypted
if __name__ == "__main__":
    print("RSA 64-bit Encryptor")
    user_msg = input("Enter message to encrypt: ")
    user_e = input("Enter Public Exponent (e) [Press Enter for default 65537]: ")
    try:
        n, e = generate_keys(user_e if user_e.strip() else None)
        cipher_list = encrypt_message(user_msg, e, n)
        print("\n" + "="*40)
        print(f"PUBLIC KEY (n, e):")
        print(f"n: {n}")
        print(f"e: {e}")
        print("-" * 20)
        print(f"CIPHERTEXT (Decimal):")
        print(" ".join(map(str, cipher_list)))
        print("-" * 20)
        print(f"CIPHERTEXT (Hex):")
        print(" ".join(hex(c) for c in cipher_list))
        print("="*40)
    except Exception as err:
        print(f"\n[ERROR]: {err}")