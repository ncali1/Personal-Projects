import os
import base64
import time
import csv
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


def generateKey(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )

    key = kdf.derive(password.encode())

    return key

def encrypt(password, key):
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    password =  padder.update(password.encode()) + padder.finalize()

    updated_password = encryptor.update(password) + encryptor.finalize()
    updated_password_iv = base64.urlsafe_b64encode(iv + password).decode()

    return updated_password_iv

def export_to_csv(passwords, filename="generated_passwords.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Generated Passwords"])
        for password in passwords:
            writer.writerow([password])
    print(f"Passwords exported to {filename}")


if __name__ == "__main__":
    user_password = input("Please input your password to be encrypted: ")
    salt = os.urandom(16)
    key = generateKey(user_password, salt)
    genereated_passwords = []

    try:
        while True:
            updated_password = encrypt(user_password, key)
            genereated_passwords.append(updated_password)
            print(f"\nEncrypted password: {updated_password}\n")
            time.sleep(3)
    except KeyboardInterrupt:
        print("Exiting...")
        export_choice = input("Would you like to export the passwords to a CSV? (y/n): ").strip().lower()
        if export_choice == "y":
            export_to_csv(genereated_passwords)
        else:
            print("Exiting without exporting passwords.")