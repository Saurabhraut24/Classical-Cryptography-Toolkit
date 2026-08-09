# -*- coding: utf-8 -*-
"""
ciphers_lib.py - Classical Cryptography Toolkit Core Library
Implements 8 Classical Encryption Algorithms & Utility Functions:
1. Caesar Cipher
2. Monoalphabetic Cipher
3. Playfair Cipher
4. Hill Cipher (2x2 & 3x3 with Mod 26 Inverse Matrix)
5. Vigenère Cipher
6. One-Time Pad Cipher
7. Rail Fence Cipher
8. Columnar Transposition Cipher
"""

import math
import random
import time
import numpy as np

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def sanitize_text(text, keep_spaces=False):
    """Sanitize text to uppercase A-Z only or preserve spaces if requested."""
    text = text.upper()
    if keep_spaces:
        return "".join(ch for ch in text if ch.isalpha() or ch.isspace())
    return "".join(ch for ch in text if ch.isalpha())

# ==========================================
# 1. CAESAR CIPHER
# ==========================================
def caesar_encrypt(text, shift):
    shift = shift % 26
    result = []
    for char in text.upper():
        if char.isalpha():
            base = ord('A')
            result.append(chr((ord(char) - base + shift) % 26 + base))
        else:
            result.append(char)
    return "".join(result)

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

# ==========================================
# 2. MONOALPHABETIC CIPHER
# ==========================================
def generate_monoalphabetic_key():
    alpha_list = list(ALPHABET)
    random.shuffle(alpha_list)
    return "".join(alpha_list)

def monoalphabetic_encrypt(text, key):
    key = key.upper()
    if len(key) != 26 or len(set(key)) != 26:
        raise ValueError("Key must be a permutation of 26 unique uppercase alphabets.")
    
    mapping = {ALPHABET[i]: key[i] for i in range(26)}
    result = []
    for ch in text.upper():
        if ch in mapping:
            result.append(mapping[ch])
        else:
            result.append(ch)
    return "".join(result)

def monoalphabetic_decrypt(text, key):
    key = key.upper()
    if len(key) != 26 or len(set(key)) != 26:
        raise ValueError("Key must be a permutation of 26 unique uppercase alphabets.")
    
    reverse_mapping = {key[i]: ALPHABET[i] for i in range(26)}
    result = []
    for ch in text.upper():
        if ch in reverse_mapping:
            result.append(reverse_mapping[ch])
        else:
            result.append(ch)
    return "".join(result)

# ==========================================
# 3. PLAYFAIR CIPHER
# ==========================================
def create_playfair_matrix(key):
    key = sanitize_text(key).replace("J", "I")
    matrix = []
    used = set()

    for ch in key + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in used:
            used.add(ch)
            matrix.append(ch)

    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, ch):
    if ch == "J":
        ch = "I"
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c
    return 0, 0

def playfair_prepare_text(text):
    text = sanitize_text(text).replace("J", "I")
    prepared = []
    i = 0
    while i < len(text):
        a = text[i]
        if i + 1 < len(text):
            b = text[i+1]
            if a == b:
                prepared.append((a, 'X'))
                i += 1
            else:
                prepared.append((a, b))
                i += 2
        else:
            prepared.append((a, 'X'))
            i += 1
    return prepared

def playfair_encrypt(text, key):
    matrix = create_playfair_matrix(key)
    pairs = playfair_prepare_text(text)
    ciphertext = []

    for a, b in pairs:
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            ciphertext.append(matrix[r1][(c1 + 1) % 5])
            ciphertext.append(matrix[r2][(c2 + 1) % 5])
        elif c1 == c2:
            ciphertext.append(matrix[(r1 + 1) % 5][c1])
            ciphertext.append(matrix[(r2 + 1) % 5][c2])
        else:
            ciphertext.append(matrix[r1][c2])
            ciphertext.append(matrix[r2][c1])

    return "".join(ciphertext)

def playfair_decrypt(text, key):
    matrix = create_playfair_matrix(key)
    text = sanitize_text(text).replace("J", "I")
    if len(text) % 2 != 0:
        text += 'X'
    
    plaintext = []
    for i in range(0, len(text), 2):
        a, b = text[i], text[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)

        if r1 == r2:
            plaintext.append(matrix[r1][(c1 - 1) % 5])
            plaintext.append(matrix[r2][(c2 - 1) % 5])
        elif c1 == c2:
            plaintext.append(matrix[(r1 - 1) % 5][c1])
            plaintext.append(matrix[(r2 - 1) % 5][c2])
        else:
            plaintext.append(matrix[r1][c2])
            plaintext.append(matrix[r2][c1])

    return "".join(plaintext)

# ==========================================
# 4. HILL CIPHER
# ==========================================
def mod_inverse(a, m=26):
    a = a % m
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

def matrix_mod_inv(matrix, mod=26):
    """Calculate inverse matrix modulo 26 for 2x2 or 3x3 matrix."""
    det = int(round(np.linalg.det(matrix))) % mod
    inv_det = mod_inverse(det, mod)
    if inv_det is None:
        raise ValueError(f"Determinant ({det}) has no modular inverse mod {mod}. Matrix is not invertible!")

    n = matrix.shape[0]
    adjugate = np.zeros((n, n), dtype=int)
    
    if n == 2:
        adjugate[0, 0] = matrix[1, 1]
        adjugate[0, 1] = -matrix[0, 1]
        adjugate[1, 0] = -matrix[1, 0]
        adjugate[1, 1] = matrix[0, 0]
    elif n == 3:
        for r in range(3):
            for c in range(3):
                minor = np.delete(np.delete(matrix, r, axis=0), c, axis=1)
                cofactor = int(round(np.linalg.det(minor)))
                adjugate[c, r] = ((-1) ** (r + c)) * cofactor

    inv_matrix = (inv_det * adjugate) % mod
    return inv_matrix.astype(int)

def hill_encrypt(text, key_matrix):
    key_matrix = np.array(key_matrix, dtype=int)
    n = key_matrix.shape[0]
    text = sanitize_text(text)
    
    # Pad text with 'X' to be multiple of n
    while len(text) % n != 0:
        text += 'X'

    cipher = []
    for i in range(0, len(text), n):
        block = [ord(ch) - 65 for ch in text[i:i+n]]
        vec = np.array(block).reshape(n, 1)
        res = np.dot(key_matrix, vec) % 26
        for val in res.flatten():
            cipher.append(chr(val + 65))

    return "".join(cipher)

def hill_decrypt(text, key_matrix):
    key_matrix = np.array(key_matrix, dtype=int)
    inv_matrix = matrix_mod_inv(key_matrix, 26)
    n = key_matrix.shape[0]
    text = sanitize_text(text)

    plaintext = []
    for i in range(0, len(text), n):
        block = [ord(ch) - 65 for ch in text[i:i+n]]
        vec = np.array(block).reshape(n, 1)
        res = np.dot(inv_matrix, vec) % 26
        for val in res.flatten():
            plaintext.append(chr(val + 65))

    return "".join(plaintext)

# ==========================================
# 5. VIGENÈRE CIPHER
# ==========================================
def vigenere_encrypt(text, key):
    text_clean = sanitize_text(text)
    key_clean = sanitize_text(key)
    if not key_clean:
        raise ValueError("Key cannot be empty.")
    
    cipher = []
    for i, ch in enumerate(text_clean):
        p_val = ord(ch) - 65
        k_val = ord(key_clean[i % len(key_clean)]) - 65
        c_val = (p_val + k_val) % 26
        cipher.append(chr(c_val + 65))
    return "".join(cipher)

def vigenere_decrypt(text, key):
    text_clean = sanitize_text(text)
    key_clean = sanitize_text(key)
    if not key_clean:
        raise ValueError("Key cannot be empty.")
    
    plaintext = []
    for i, ch in enumerate(text_clean):
        c_val = ord(ch) - 65
        k_val = ord(key_clean[i % len(key_clean)]) - 65
        p_val = (c_val - k_val) % 26
        plaintext.append(chr(p_val + 65))
    return "".join(plaintext)

# ==========================================
# 6. ONE-TIME PAD (OTP) CIPHER
# ==========================================
def generate_otp_key(length):
    return "".join(random.choice(ALPHABET) for _ in range(length))

def otp_encrypt(text, key):
    text_clean = sanitize_text(text)
    key_clean = sanitize_text(key)
    if len(key_clean) < len(text_clean):
        raise ValueError(f"One-Time Pad key length ({len(key_clean)}) must be >= plaintext length ({len(text_clean)}).")

    cipher = []
    for i, ch in enumerate(text_clean):
        p_val = ord(ch) - 65
        k_val = ord(key_clean[i]) - 65
        c_val = (p_val + k_val) % 26
        cipher.append(chr(c_val + 65))
    return "".join(cipher)

def otp_decrypt(text, key):
    text_clean = sanitize_text(text)
    key_clean = sanitize_text(key)
    if len(key_clean) < len(text_clean):
        raise ValueError(f"One-Time Pad key length ({len(key_clean)}) must be >= ciphertext length ({len(text_clean)}).")

    plaintext = []
    for i, ch in enumerate(text_clean):
        c_val = ord(ch) - 65
        k_val = ord(key_clean[i]) - 65
        p_val = (c_val - k_val) % 26
        plaintext.append(chr(p_val + 65))
    return "".join(plaintext)

# ==========================================
# 7. RAIL FENCE CIPHER
# ==========================================
def rail_fence_encrypt(text, rails):
    if rails <= 1:
        return text
    text_clean = sanitize_text(text)
    fence = [[] for _ in range(rails)]
    rail = 0
    direction = 1

    for ch in text_clean:
        fence[rail].append(ch)
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction

    return "".join("".join(row) for row in fence)

def rail_fence_decrypt(text, rails):
    if rails <= 1:
        return text
    text_clean = sanitize_text(text)
    n = len(text_clean)
    
    fence = [['' for _ in range(n)] for _ in range(rails)]
    rail = 0
    direction = 1
    for i in range(n):
        fence[rail][i] = '*'
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction

    index = 0
    for r in range(rails):
        for c in range(n):
            if fence[r][c] == '*' and index < n:
                fence[r][c] = text_clean[index]
                index += 1

    plaintext = []
    rail = 0
    direction = 1
    for i in range(n):
        plaintext.append(fence[rail][i])
        rail += direction
        if rail == 0 or rail == rails - 1:
            direction = -direction

    return "".join(plaintext)

def sanitize_key_alphanumeric(key):
    """Sanitize key to preserve both alphabetic letters and numbers."""
    key = str(key).upper()
    return "".join(ch for ch in key if ch.isalnum())

# ==========================================
# 8. COLUMNAR TRANSPOSITION CIPHER
# ==========================================
def columnar_encrypt(text, key):
    text_clean = sanitize_text(text)
    key_clean = sanitize_key_alphanumeric(key)
    if not key_clean:
        raise ValueError("Key cannot be empty.")
    
    num_cols = len(key_clean)
    num_rows = math.ceil(len(text_clean) / num_cols)
    
    padded_text = text_clean.ljust(num_rows * num_cols, 'X')
    key_order = sorted(range(len(key_clean)), key=lambda k: (key_clean[k], k))
    
    matrix = [padded_text[i:i+num_cols] for i in range(0, len(padded_text), num_cols)]
    
    cipher = []
    for col_idx in key_order:
        for row in matrix:
            cipher.append(row[col_idx])

    return "".join(cipher)

def columnar_decrypt(text, key):
    text_clean = sanitize_text(text)
    key_clean = sanitize_key_alphanumeric(key)
    if not key_clean:
        raise ValueError("Key cannot be empty.")

    num_cols = len(key_clean)
    num_rows = math.ceil(len(text_clean) / num_cols)
    key_order = sorted(range(len(key_clean)), key=lambda k: (key_clean[k], k))

    grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
    
    idx = 0
    for col_idx in key_order:
        for r in range(num_rows):
            if idx < len(text_clean):
                grid[r][col_idx] = text_clean[idx]
                idx += 1

    plaintext = []
    for r in range(num_rows):
        for c in range(num_cols):
            plaintext.append(grid[r][c])

    return "".join(plaintext)

# ==========================================
# UTILITIES & COMPARATOR
# ==========================================
def calculate_letter_frequency(text):
    text_clean = sanitize_text(text)
    total = len(text_clean)
    if total == 0:
        return {}
    counts = {ch: 0 for ch in ALPHABET}
    for ch in text_clean:
        if ch in counts:
            counts[ch] += 1
    freqs = {ch: round((counts[ch] / total) * 100, 2) for ch in ALPHABET}
    return freqs

def benchmark_ciphers(text):
    text_clean = sanitize_text(text)
    if not text_clean:
        text_clean = "NETWORKSECURITYPROJECT"

    results = []

    # Caesar
    t0 = time.perf_counter()
    enc_caesar = caesar_encrypt(text_clean, 7)
    dec_caesar = caesar_decrypt(enc_caesar, 7)
    t_caesar = (time.perf_counter() - t0) * 1000
    results.append({"name": "Caesar Cipher", "time_ms": round(t_caesar, 4), "keyspace": "25 keys", "type": "Substitution"})

    # Monoalphabetic
    mono_key = "QWERTYUIOPASDFGHJKLZXCVBNM"
    t0 = time.perf_counter()
    enc_mono = monoalphabetic_encrypt(text_clean, mono_key)
    dec_mono = monoalphabetic_decrypt(enc_mono, mono_key)
    t_mono = (time.perf_counter() - t0) * 1000
    results.append({"name": "Monoalphabetic", "time_ms": round(t_mono, 4), "keyspace": "26! (~4.03 x 10^26)", "type": "Substitution"})

    # Playfair
    t0 = time.perf_counter()
    enc_pf = playfair_encrypt(text_clean, "MONARCHY")
    dec_pf = playfair_decrypt(enc_pf, "MONARCHY")
    t_pf = (time.perf_counter() - t0) * 1000
    results.append({"name": "Playfair Cipher", "time_ms": round(t_pf, 4), "keyspace": "25! (~1.55 x 10^25)", "type": "Substitution (Digraph)"})

    # Hill Cipher 2x2
    hill_k = [[7, 8], [11, 11]]
    t0 = time.perf_counter()
    enc_hill = hill_encrypt(text_clean, hill_k)
    dec_hill = hill_decrypt(enc_hill, hill_k)
    t_hill = (time.perf_counter() - t0) * 1000
    results.append({"name": "Hill Cipher (2x2)", "time_ms": round(t_hill, 4), "keyspace": "26^(n^2)", "type": "Polygraphic Substitution"})

    # Vigenere
    t0 = time.perf_counter()
    enc_vig = vigenere_encrypt(text_clean, "KEY")
    dec_vig = vigenere_decrypt(enc_vig, "KEY")
    t_vig = (time.perf_counter() - t0) * 1000
    results.append({"name": "Vigenère Cipher", "time_ms": round(t_vig, 4), "keyspace": "26^L (L=Key Length)", "type": "Polyalphabetic"})

    # One-Time Pad
    otp_key = generate_otp_key(len(text_clean))
    t0 = time.perf_counter()
    enc_otp = otp_encrypt(text_clean, otp_key)
    dec_otp = otp_decrypt(enc_otp, otp_key)
    t_otp = (time.perf_counter() - t0) * 1000
    results.append({"name": "One-Time Pad", "time_ms": round(t_otp, 4), "keyspace": "26^N (Unbreakable)", "type": "Perfect Secrecy Stream"})

    # Rail Fence
    t0 = time.perf_counter()
    enc_rf = rail_fence_encrypt(text_clean, 3)
    dec_rf = rail_fence_decrypt(enc_rf, 3)
    t_rf = (time.perf_counter() - t0) * 1000
    results.append({"name": "Rail Fence Cipher", "time_ms": round(t_rf, 4), "keyspace": "N Rails (N < Text Len)", "type": "Transposition"})

    # Columnar
    t0 = time.perf_counter()
    enc_col = columnar_encrypt(text_clean, "SECRET")
    dec_col = columnar_decrypt(enc_col, "SECRET")
    t_col = (time.perf_counter() - t0) * 1000
    results.append({"name": "Columnar Transposition", "time_ms": round(t_col, 4), "keyspace": "K! (K=Columns)", "type": "Transposition"})

    return results
