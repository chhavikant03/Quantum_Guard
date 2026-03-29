import tkinter as tk
from tkinter import scrolledtext
from sympy import factorint

class RSABreakerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Cryptanalysis Engine")
        self.root.geometry("780x680")
        self.root.configure(bg="#0a0a0a")

        tk.Label(root, text="RSA CRYPTANALYSIS ENGINE",
                 font=("Courier", 16, "bold"),
                 fg="#00ff41", bg="#0a0a0a").pack(pady=15)

        # Inputs
        self.create_input("Modulus (n):", "9173503", "modulus")
        self.create_input("Public Exponent (e):", "17", "exponent")
        self.create_input("Ciphertext(s) (space separated):",
                          "3000 1317 745 745 2182", "cipher")

        # Button
        tk.Button(root, text="BREAK & DECRYPT",
                  command=self.execute,
                  bg="#333", fg="#00ff41",
                  font=("Courier", 12, "bold")).pack(pady=20)

        # Output
        self.log = scrolledtext.ScrolledText(
            root, height=20, width=95,
            bg="black", fg="#00ff41",
            font=("Consolas", 10)
        )
        self.log.pack(pady=10)

    def create_input(self, label, default, attr):
        tk.Label(self.root, text=label,
                 fg="white", bg="#0a0a0a").pack()
        entry = tk.Entry(self.root, width=85,
                         bg="#111", fg="#00ff41",
                         insertbackground="white")
        entry.insert(0, default)
        entry.pack(pady=5)
        setattr(self, attr, entry)

    def log_msg(self, msg):
        self.log.insert(tk.END, f"> {msg}\n")
        self.log.see(tk.END)
        self.root.update()

    def execute(self):
        try:
            # 🔥 Clear previous output (IMPORTANT FIX)
            self.log.delete(1.0, tk.END)

            # 🔥 Force fresh read
            self.root.update_idletasks()

            n = int(self.modulus.get().strip())
            e = int(self.exponent.get().strip())
            cipher_input = self.cipher.get().strip()

            self.log_msg(f"[INPUT] n={n}, e={e}")
            self.log_msg(f"[INPUT RAW CIPHERS] {cipher_input}")

            # Split multiple values
            cipher_list = cipher_input.split()

            # Convert all inputs
            c_values = []
            for val in cipher_list:
                if val.startswith("0x"):
                    c_values.append(int(val, 16))
                else:
                    c_values.append(int(val))

            self.log_msg("🔍 Factoring modulus n...")

            # Factor n
            factors = factorint(n)
            primes = []
            for p, count in factors.items():
                primes.extend([p] * count)

            if len(primes) != 2:
                self.log_msg("[!] Invalid RSA modulus")
                self.log_msg(f"Factors: {primes}")
                return

            p, q = primes
            self.log_msg(f"✅ p = {p}, q = {q}")
            self.log_msg(f"🔢 Key size: {n.bit_length()} bits")

            # Compute phi
            phi = (p - 1) * (q - 1)

            # Compute d
            try:
                d = pow(e, -1, phi)
                self.log_msg(f"🔑 Private key d = {d}")
            except:
                self.log_msg("❌ Invalid e (not coprime with phi)")
                return

            self.log_msg("="*45)

            # 🔥 Decrypt all blocks
            message = ""

            for c in c_values:
                self.log_msg(f"[DEBUG] Using ciphertext: {c}")

                m = pow(c, d, n)
                self.log_msg(f"→ Decrypted integer: {m}")

                if 0 <= m <= 255:
                    char = chr(m)
                    message += char
                    self.log_msg(f"→ Character: {char}")
                else:
                    self.log_msg(f"[!] Non-ASCII: {m}")

                self.log_msg("-"*30)

            # Final message
            if message:
                self.log_msg("="*45)
                self.log_msg(f"📜 FINAL MESSAGE: {message}")
                self.log_msg("="*45)

        except Exception as err:
            self.log_msg(f"[CRITICAL ERROR] {str(err)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = RSABreakerGUI(root)
    root.mainloop()