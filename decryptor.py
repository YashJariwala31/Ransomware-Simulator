from cryptography.fernet import Fernet
import os

with open("keyfile.key", "rb") as f:
    key = f.read()

fernet = Fernet(key)
target_folder = "test_files"

for root, _, files in os.walk(target_folder):
    for file in files:
        if file.endswith(".txt"):
            filepath = os.path.join(root, file)
            with open(filepath, "rb") as f:
                data = f.read()
            decrypted = fernet.decrypt(data)
            with open(filepath, "wb") as f:
                f.write(decrypted)
