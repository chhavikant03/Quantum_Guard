import random
import tkinter as tk
from tkinter import messagebox

# ---------------- PRIME GENERATION ----------------
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def generate_prime(bits=32):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num

# ---------------- RSA KEYGEN ----------------
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
            raise Exception("e is not coprime with phi(n)")
    else:
        e = 65537

    return n, e

# ---------------- ENCRYPTION ----------------
def encrypt_message(message, e, n):
    encrypted = []
    for char in message:
        m = ord(char)
        if m >= n:
            raise Exception("Message value too large for modulus")
        c = pow(m, e, n)
        encrypted.append(c)
    return encrypted

# ---------------- GUI FUNCTION ----------------
def run_encryption():
    try:
        message = message_entry.get()
        e_value = e_entry.get()

        n, e = generate_keys(e_value if e_value else None)

        cipher = encrypt_message(message, e, n)

        output_box.delete("1.0", tk.END)
        output_box.insert(tk.END, f"Public Key (n, e):\n{n}, {e}\n\n")
        output_box.insert(tk.END, "Cipher (decimal):\n")
        output_box.insert(tk.END, " ".join(map(str, cipher)) + "\n\n")

        hex_cipher = [hex(c) for c in cipher]
        output_box.insert(tk.END, "Cipher (hex):\n")
        output_box.insert(tk.END, " ".join(hex_cipher))

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ---------------- GUI ----------------
root = tk.Tk()
root.title("RSA 64-bit Encryptor")
root.geometry("600x400")
root.configure(bg="black")

title = tk.Label(root, text="RSA ENCRYPTOR (64-bit)", fg="lime", bg="black", font=("Courier", 16))
title.pack(pady=10)

tk.Label(root, text="Message:", fg="white", bg="black").pack()
message_entry = tk.Entry(root, width=50)
message_entry.pack()

tk.Label(root, text="Public Exponent (e) [optional]:", fg="white", bg="black").pack()
e_entry = tk.Entry(root, width=20)
e_entry.pack()

encrypt_btn = tk.Button(root, text="ENCRYPT", command=run_encryption, bg="green", fg="black")
encrypt_btn.pack(pady=10)

output_box = tk.Text(root, height=12, width=70, bg="black", fg="lime")
output_box.pack()

root.mainloop()