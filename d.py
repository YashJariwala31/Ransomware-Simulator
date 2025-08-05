# open_keyfile.py
with open("keyfile.key", "rb") as f:
    key = f.read()
    print("Decryption Key:", key.decode())
