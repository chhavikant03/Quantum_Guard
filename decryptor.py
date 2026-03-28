from sympy import factorint

def crack_rsa(n, e, ciphers):
    factors_dict = factorint(n)
    primes = []
    for p, count in factors_dict.items():
        primes.extend([p] * count)
    if len(primes) != 2:
        return None
    p, q = primes
    phi = (p - 1) * (q - 1)
    try:
        d = pow(e, -1, phi)
    except ValueError:
        return None
    decrypted_text = ""
    for c in ciphers:
        m = pow(c, d, n)
        if 0 <= m <= 255:
            decrypted_text += chr(m)
        else:
            decrypted_text += f"[{m}]"
    return decrypted_text

if __name__ == "__main__":
    n_in = int(input("Enter Modulus (n): "))
    e_in = int(input("Enter Public Exponent (e): "))
    c_in = input("Enter Ciphertext(s) (space separated): ").split()
    c_list = [int(val, 16) if val.startswith("0x") else int(val) for val in c_in]
    result = crack_rsa(n_in, e_in, c_list)
    if result:
        print(f"Decrypted: {result}")