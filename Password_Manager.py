import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import os

# --- Encryption Logic ---
def load_key():
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()

        with open("secret.key", "wb") as key_file:
            key_file.write(key)

    with open("secret.key", "rb") as key_file:
        return key_file.read()


key = load_key()
fer = Fernet(key)

# --- Functions ---
def save_password():
    website = website_entry.get()
    user = user_entry.get()
    pwd = pass_entry.get()

    if not website or not user or not pwd:
        messagebox.showwarning("Error", "Please fill in all fields!")
        return

    # Encrypt password
    encrypted_pwd = fer.encrypt(pwd.encode()).decode()

    with open("passwords.txt", "a") as f:
        f.write(f"{website} | {user} | {encrypted_pwd}\n")

    # Clear fields
    website_entry.delete(0, tk.END)
    user_entry.delete(0, tk.END)
    pass_entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Password saved securely!")


def view_passwords():
    if not os.path.exists("passwords.txt"):
        messagebox.showinfo("Info", "No saved data found.")
        return

    view_window = tk.Toplevel(root)
    view_window.title("Saved Passwords")
    view_window.geometry("600x400")

    with open("passwords.txt", "r") as f:
        for line in f.readlines():
            data = line.rstrip()
            w, u, p = data.split(" | ")

            # Decrypt password
            decrypted_p = fer.decrypt(p.encode()).decode()

            tk.Label(
                view_window,
                text=f"Site: {w} | User: {u} | Pass: {decrypted_p}",
                font=("Arial", 10),
                anchor="w",
                justify="left"
            ).pack(fill="x", padx=10, pady=2)


# --- GUI Design ---
root = tk.Tk()
root.title("Python Secure Password Manager")
root.geometry("400x300")
root.resizable(False, False)

tk.Label(root, text="Website:", font=("Arial", 10, "bold")).pack(pady=5)
website_entry = tk.Entry(root, width=40)
website_entry.pack()

tk.Label(root, text="Username / Email:", font=("Arial", 10, "bold")).pack(pady=5)
user_entry = tk.Entry(root, width=40)
user_entry.pack()

tk.Label(root, text="Password:", font=("Arial", 10, "bold")).pack(pady=5)
pass_entry = tk.Entry(root, width=40, show="*")
pass_entry.pack()

tk.Button(
    root,
    text="Save Password",
    command=save_password,
    bg="#4CAF50",
    fg="white",
    width=20
).pack(pady=15)

tk.Button(
    root,
    text="View Saved Passwords",
    command=view_passwords,
    bg="#2196F3",
    fg="white",
    width=20
).pack()

root.mainloop()
