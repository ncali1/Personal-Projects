import time

def caesar_cipher(plaintext, shift):
    ciphertext = ""

    for ch in plaintext:
        if ch.isalpha():
            shift_base = ord('A') if ch.isupper() else ord('a')
            shifted_ch = chr((ord(ch) - shift_base + shift) % 26 + shift_base)
            ciphertext += shifted_ch
        else:
            ciphertext += ch
    return ciphertext


def caesar_decipher(ciphertext, shift):
    plaintext = ""

    for ch in ciphertext:
        if ch.isalpha():
            shift_base = ord('A') if ch.isupper() else ord('a')
            shifted_ch = chr((ord(ch) - shift_base - shift) % 26 + shift_base)
            plaintext += shifted_ch
        else:
            plaintext += ch

    return plaintext


def main():
    action = input("Do you want to cipher or decipher?: ").strip().lower()
    
    if action == 'cipher':
        plaintext = input("Enter the plaintext: ")
        shift = int(input("Enter the shift: "))
        ciphertext = caesar_cipher(plaintext, shift)
        print(f"Ciphertext: {ciphertext}")
    
    elif action == 'decipher':
        ciphertext = input("Enter the ciphertext: ")
        shift = int(input("Enter the shift: "))
        plaintext = caesar_decipher(ciphertext, shift)
        print(f"Plaintext: {plaintext}")

    else:
        print("Invalid action. Exiting...")
        return

if __name__ == "__main__":
    main()