# -*- coding: utf-8 -*-
"""
cli_toolkit.py - Menu-Driven Command Line Classical Cryptography Toolkit
Fulfills all menu requirements specified in Mini Project1.docx.
"""

import sys
import os
import time
from ciphers_lib import (
    caesar_encrypt, caesar_decrypt,
    generate_monoalphabetic_key, monoalphabetic_encrypt, monoalphabetic_decrypt,
    playfair_encrypt, playfair_decrypt, create_playfair_matrix,
    hill_encrypt, hill_decrypt,
    vigenere_encrypt, vigenere_decrypt,
    generate_otp_key, otp_encrypt, otp_decrypt,
    rail_fence_encrypt, rail_fence_decrypt,
    columnar_encrypt, columnar_decrypt,
    benchmark_ciphers, calculate_letter_frequency, sanitize_text
)

def print_header():
    print("=" * 60)
    print("         CLASSICAL CRYPTOGRAPHY TOOLKIT - CLI MENU       ")
    print("=" * 60)

def print_menu():
    print_header()
    print("SUBSTITUTION CIPHERS")
    print("  1. Caesar Cipher")
    print("  2. Monoalphabetic Cipher")
    print("  3. Playfair Cipher")
    print("  4. Hill Cipher")
    print("  5. Vigenère (Polyalphabetic) Cipher")
    print("  6. One-Time Pad")
    print("TRANSPOSITION CIPHERS")
    print("  7. Rail Fence Cipher")
    print("  8. Columnar Transposition Cipher")
    print("UTILITY MODULES")
    print("  9. Compare Algorithms (Benchmark Execution Time)")
    print(" 10. Encrypt Text File")
    print(" 11. Decrypt Text File")
    print(" 12. Help & Cryptography Guide")
    print(" 13. Exit")
    print("=" * 60)

def get_input(prompt):
    return input(prompt).strip()

def run_caesar():
    print("\n--- CAESAR CIPHER ---")
    mode = get_input("Select Mode (1: Encrypt, 2: Decrypt): ")
    text = get_input("Enter Text: ")
    if mode in ['1', '2']:
        try:
            shift = int(get_input("Enter Shift Key (0-25): "))
            t0 = time.perf_counter()
            if mode == '1':
                res = caesar_encrypt(text, shift)
                label = "Ciphertext"
            else:
                res = caesar_decrypt(text, shift)
                label = "Decrypted Text"
            t_elapsed = (time.perf_counter() - t0) * 1000
            print("\n----- OUTPUT -----")
            print(f"Original Text  : {text}")
            print(f"Shift Key      : {shift}")
            print(f"{label:<15}: {res}")
            print(f"Execution Time : {t_elapsed:.4f} ms")
        except ValueError:
            print("[ERROR] Shift key must be an integer!")

def run_monoalphabetic():
    print("\n--- MONOALPHABETIC CIPHER ---")
    mode = get_input("Select Mode (1: Encrypt, 2: Decrypt): ")
    text = get_input("Enter Text: ")
    key = get_input("Enter 26-letter Substitution Alphabet (or press Enter to auto-generate): ")
    if not key:
        key = generate_monoalphabetic_key()
        print(f"[Generated Random Key]: {key}")
    try:
        t0 = time.perf_counter()
        if mode == '1':
            res = monoalphabetic_encrypt(text, key)
            label = "Ciphertext"
        else:
            res = monoalphabetic_decrypt(text, key)
            label = "Decrypted Text"
        t_elapsed = (time.perf_counter() - t0) * 1000
        print("\n----- OUTPUT -----")
        print(f"Original Text  : {text}")
        print(f"Substitution Key: {key}")
        print(f"{label:<15}: {res}")
        print(f"Execution Time : {t_elapsed:.4f} ms")
    except ValueError as e:
        print(f"[ERROR] {e}")

def run_playfair():
    print("\n--- PLAYFAIR CIPHER ---")
    mode = get_input("Select Mode (1: Encrypt, 2: Decrypt): ")
    text = get_input("Enter Text: ")
    key = get_input("Enter Keyword: ")
    try:
        matrix = create_playfair_matrix(key)
        print("\n[Playfair 5x5 Key Matrix]:")
        for row in matrix:
            print(" ".join(row))
        t0 = time.perf_counter()
        if mode == '1':
            res = playfair_encrypt(text, key)
            label = "Ciphertext"
        else:
            res = playfair_decrypt(text, key)
            label = "Decrypted Text"
        t_elapsed = (time.perf_counter() - t0) * 1000
        print("\n----- OUTPUT -----")
        print(f"Original Text  : {text}")
        print(f"Key Keyword    : {key}")
        print(f"{label:<15}: {res}")
        print(f"Execution Time : {t_elapsed:.4f} ms")
    except Exception as e:
        print(f"[ERROR] {e}")

def run_hill():
    print("\n--- HILL CIPHER (2x2 Matrix) ---")
    mode = get_input("Select Mode (1: Encrypt, 2: Decrypt): ")
    text = get_input("Enter Plaintext/Ciphertext: ")
    print("Enter 2x2 Key Matrix elements:")
    try:
        a = int(get_input("Element [1][1]: "))
        b = int(get_input("Element [1][2]: "))
        c = int(get_input("Element [2][1]: "))
        d = int(get_input("Element [2][2]: "))
        key_matrix = [[a, b], [c, d]]
        
        t0 = time.perf_counter()
        if mode == '1':
            res = hill_encrypt(text, key_matrix)
            label = "Ciphertext"
        else:
            res = hill_decrypt(text, key_matrix)
            label = "Decrypted Text"
        t_elapsed = (time.perf_counter() - t0) * 1000
        print("\n----- OUTPUT -----")
        print(f"Original Text  : {text}")
        print(f"Key Matrix     :\n [{a} {b}]\n [{c} {d}]")
        print(f"{label:<15}: {res}")
        print(f"Execution Time : {t_elapsed:.4f} ms")
    except ValueError as e:
        print(f"[ERROR] Invalid Matrix or Determinant: {e}")

def run_vigenere():
    print("\n--- VIGENÈRE CIPHER ---")
    mode = get_input("Select Mode (1: Encrypt, 2: Decrypt): ")
    text = get_input("Enter Text: ")
    key = get_input("Enter Key Phrase: ")
    try:
        t0 = time.perf_counter()
        if mode == '1':
            res = vigenere_encrypt(text, key)
            label = "Ciphertext"
        else:
            res = vigenere_decrypt(text, key)
            label = "Decrypted Text"
        t_elapsed = (time.perf_counter() - t0) * 1000
        print("\n----- OUTPUT -----")
        print(f"Original Text  : {text}")
        print(f"Key Phrase     : {key}")
        print(f"{label:<15}: {res}")
        print(f"Execution Time : {t_elapsed:.4f} ms")
    except ValueError as e:
        print(f"[ERROR] {e}")

def run_otp():
    print("\n--- ONE-TIME PAD CIPHER ---")
    mode = get_input("Select Mode (1: Encrypt, 2: Decrypt): ")
    text = get_input("Enter Text: ")
    clean_len = len(sanitize_text(text))
    key = get_input(f"Enter Key (Length >= {clean_len}, or press Enter to auto-generate): ")
    if not key:
        key = generate_otp_key(clean_len)
        print(f"[Generated OTP Key]: {key}")
    try:
        t0 = time.perf_counter()
        if mode == '1':
            res = otp_encrypt(text, key)
            label = "Ciphertext"
        else:
            res = otp_decrypt(text, key)
            label = "Decrypted Text"
        t_elapsed = (time.perf_counter() - t0) * 1000
        print("\n----- OUTPUT -----")
        print(f"Original Text  : {text}")
        print(f"OTP Key        : {key}")
        print(f"{label:<15}: {res}")
        print(f"Execution Time : {t_elapsed:.4f} ms")
    except ValueError as e:
        print(f"[ERROR] {e}")

def run_rail_fence():
    print("\n--- RAIL FENCE CIPHER ---")
    mode = get_input("Select Mode (1: Encrypt, 2: Decrypt): ")
    text = get_input("Enter Text: ")
    try:
        rails = int(get_input("Enter Number of Rails (Depth): "))
        t0 = time.perf_counter()
        if mode == '1':
            res = rail_fence_encrypt(text, rails)
            label = "Ciphertext"
        else:
            res = rail_fence_decrypt(text, rails)
            label = "Decrypted Text"
        t_elapsed = (time.perf_counter() - t0) * 1000
        print("\n----- OUTPUT -----")
        print(f"Original Text  : {text}")
        print(f"Rails          : {rails}")
        print(f"{label:<15}: {res}")
        print(f"Execution Time : {t_elapsed:.4f} ms")
    except ValueError:
        print("[ERROR] Rails must be an integer!")

def run_columnar():
    print("\n--- COLUMNAR TRANSPOSITION CIPHER ---")
    mode = get_input("Select Mode (1: Encrypt, 2: Decrypt): ")
    text = get_input("Enter Text: ")
    key = get_input("Enter Key Word: ")
    try:
        t0 = time.perf_counter()
        if mode == '1':
            res = columnar_encrypt(text, key)
            label = "Ciphertext"
        else:
            res = columnar_decrypt(text, key)
            label = "Decrypted Text"
        t_elapsed = (time.perf_counter() - t0) * 1000
        print("\n----- OUTPUT -----")
        print(f"Original Text  : {text}")
        print(f"Columnar Key   : {key}")
        print(f"{label:<15}: {res}")
        print(f"Execution Time : {t_elapsed:.4f} ms")
    except ValueError as e:
        print(f"[ERROR] {e}")

def run_comparator():
    print("\n--- ALGORITHM COMPARATOR & BENCHMARK ---")
    sample = get_input("Enter Sample Text for Benchmark (Press Enter for default): ")
    results = benchmark_ciphers(sample)
    print("\n" + "="*70)
    print(f"{'Algorithm Name':<25} | {'Type':<25} | {'Exec Time (ms)':<12}")
    print("="*70)
    for r in results:
        print(f"{r['name']:<25} | {r['type']:<25} | {r['time_ms']:<12.4f}")
    print("="*70)

def file_operation(encrypt_mode=True):
    action = "Encrypt" if encrypt_mode else "Decrypt"
    print(f"\n--- {action.upper()} TEXT FILE ---")
    filepath = get_input("Enter Path to .txt File: ")
    if not os.path.exists(filepath):
        print("[ERROR] File does not exist!")
        return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    print("\nSelect Cipher for File:")
    print("1. Caesar | 2. Monoalphabetic | 3. Playfair | 4. Vigenère | 5. Rail Fence")
    c_choice = get_input("Enter choice: ")

    try:
        if c_choice == '1':
            shift = int(get_input("Shift (1-25): "))
            res = caesar_encrypt(content, shift) if encrypt_mode else caesar_decrypt(content, shift)
        elif c_choice == '2':
            k = get_input("26-letter key: ")
            res = monoalphabetic_encrypt(content, k) if encrypt_mode else monoalphabetic_decrypt(content, k)
        elif c_choice == '3':
            k = get_input("Keyword: ")
            res = playfair_encrypt(content, k) if encrypt_mode else playfair_decrypt(content, k)
        elif c_choice == '4':
            k = get_input("Key phrase: ")
            res = vigenere_encrypt(content, k) if encrypt_mode else vigenere_decrypt(content, k)
        elif c_choice == '5':
            r = int(get_input("Rails: "))
            res = rail_fence_encrypt(content, r) if encrypt_mode else rail_fence_decrypt(content, r)
        else:
            print("[ERROR] Invalid Cipher Choice.")
            return

        out_path = filepath + (".enc" if encrypt_mode else ".dec.txt")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(res)
        print(f"\n[SUCCESS] Processed file saved to: {out_path}")

    except Exception as e:
        print(f"[ERROR] File processing failed: {e}")

def run_help():
    print("\n" + "="*60)
    print("                     HELP & CRYPTOGRAPHY GUIDE               ")
    print("="*60)
    print("1. Caesar: Shifts each letter by a fixed key value k (mod 26).")
    print("2. Monoalphabetic: Replaces each letter with a 1-to-1 mapped alphabet key.")
    print("3. Playfair: Encrypts digraphs using a 5x5 matrix generated by keyword.")
    print("4. Hill Cipher: Uses matrix multiplication modulo 26 to encrypt n-letter blocks.")
    print("5. Vigenère: Uses repeating key phrase values to shift corresponding letters.")
    print("6. One-Time Pad: Perfect secrecy cipher using random non-repeating key matching text length.")
    print("7. Rail Fence: Transposition cipher writing message in diagonal wave across depth rails.")
    print("8. Columnar Transposition: Arranges text in rows and reads out in sorted column order.")
    print("="*60)

def main():
    while True:
        print_menu()
        choice = get_input("Enter your Choice (1-13): ")
        if choice == '1':
            run_caesar()
        elif choice == '2':
            run_monoalphabetic()
        elif choice == '3':
            run_playfair()
        elif choice == '4':
            run_hill()
        elif choice == '5':
            run_vigenere()
        elif choice == '6':
            run_otp()
        elif choice == '7':
            run_rail_fence()
        elif choice == '8':
            run_columnar()
        elif choice == '9':
            run_comparator()
        elif choice == '10':
            file_operation(encrypt_mode=True)
        elif choice == '11':
            file_operation(encrypt_mode=False)
        elif choice == '12':
            run_help()
        elif choice == '13':
            print("\nThank you for using Classical Cryptography Toolkit! Exiting...")
            sys.exit(0)
        else:
            print("\n[INVALID CHOICE] Please select a number between 1 and 13.")
        
        get_input("\nPress Enter to return to main menu...")

if __name__ == "__main__":
    main()
