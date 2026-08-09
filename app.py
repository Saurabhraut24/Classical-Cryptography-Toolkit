# -*- coding: utf-8 -*-
"""
app.py - Pure Streamlit UI for Classical Cryptography Toolkit
No HTML/CSS/JS files required. Fully built with native Streamlit components.
"""

import time
import pandas as pd
import streamlit as st
from ciphers_lib import (
    caesar_encrypt, caesar_decrypt,
    generate_monoalphabetic_key, monoalphabetic_encrypt, monoalphabetic_decrypt,
    playfair_encrypt, playfair_decrypt, create_playfair_matrix,
    hill_encrypt, hill_decrypt,
    vigenere_encrypt, vigenere_decrypt,
    generate_otp_key, otp_encrypt, otp_decrypt,
    rail_fence_encrypt, rail_fence_decrypt,
    columnar_encrypt, columnar_decrypt,
    benchmark_ciphers, calculate_letter_frequency, sanitize_text, sanitize_key_alphanumeric
)

# Set Streamlit Page Configuration
st.set_page_config(
    page_title="Classical Cryptography Toolkit",
    page_icon="🔒",
    layout="wide"
)

# Title & Header
st.title("🔒 Classical Cryptography Toolkit")
st.caption("Network Security Mini Project | Streamlit Interactive Interface")

# Sidebar Navigation
st.sidebar.title("📌 Navigation Menu")

category = st.sidebar.radio(
    "Choose Module Category:",
    ["Substitution Ciphers", "Transposition Ciphers", "Utilities & Analysis"]
)

if category == "Substitution Ciphers":
    cipher_choice = st.sidebar.selectbox(
        "Select Cipher:",
        [
            "1. Caesar Cipher",
            "2. Monoalphabetic Cipher",
            "3. Playfair Cipher",
            "4. Hill Cipher (2x2)",
            "5. Vigenère Cipher",
            "6. One-Time Pad"
        ]
    )
elif category == "Transposition Ciphers":
    cipher_choice = st.sidebar.selectbox(
        "Select Cipher:",
        [
            "7. Rail Fence Cipher",
            "8. Columnar Transposition Cipher"
        ]
    )
else:
    cipher_choice = st.sidebar.selectbox(
        "Select Utility Module:",
        [
            "9. Compare Algorithms (Benchmark)",
            "10. File Encryption & Decryption",
            "11. Text Frequency Analysis",
            "12. Cryptography Concept Guide"
        ]
    )

st.sidebar.markdown("---")
st.sidebar.info("💡 **Course**: Network Security Mini Project\n\n**Class**: Final Year (ECM)")

# Main Content Routing

# ==========================================
# 1. CAESAR CIPHER
# ==========================================
if cipher_choice == "1. Caesar Cipher":
    st.header("1. Caesar Cipher")
    st.write("Shifts each letter in the plaintext by a fixed number of positions down the alphabet modulo 26.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input & Configuration")
        mode = st.radio("Select Mode:", ["Encrypt", "Decrypt"], horizontal=True)
        text_input = st.text_area("Input Text:", "NETWORK SECURITY", height=120)
        shift = st.slider("Shift Key (0-25):", 0, 25, 5)
        
    with col2:
        st.subheader("Output & Telemetry")
        t0 = time.perf_counter()
        if mode == "Encrypt":
            result = caesar_encrypt(text_input, shift)
        else:
            result = caesar_decrypt(text_input, shift)
        t_elapsed = (time.perf_counter() - t0) * 1000
        
        st.text_area("Result Output:", result, height=120)
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Execution Time", f"{t_elapsed:.4f} ms")
        m2.metric("Text Length", f"{len(result)} chars")
        m3.metric("Key Space", "25 Keys")
        
        st.subheader("Shift Wheel Visualizer")
        shift_table = {
            "Plain Alphabet": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
            "Cipher Shift": list(caesar_encrypt("ABCDEFGHIJKLMNOPQRSTUVWXYZ", shift))
        }
        st.dataframe(pd.DataFrame(shift_table).T)

# ==========================================
# 2. MONOALPHABETIC CIPHER
# ==========================================
elif cipher_choice == "2. Monoalphabetic Cipher":
    st.header("2. Monoalphabetic Cipher")
    st.write("Replaces each letter of the alphabet with a corresponding letter from a 26-letter substitution alphabet key.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input & Configuration")
        mode = st.radio("Select Mode:", ["Encrypt", "Decrypt"], horizontal=True)
        text_input = st.text_area("Input Text:", "HELLOWORLD", height=120)
        
        if st.button("✨ Generate Random Substitution Key"):
            st.session_state["mono_key"] = generate_monoalphabetic_key()
            
        mono_key = st.text_input("26-Letter Key:", st.session_state.get("mono_key", "QWERTYUIOPASDFGHJKLZXCVBNM"), max_chars=26)
        
    with col2:
        st.subheader("Output & Telemetry")
        try:
            t0 = time.perf_counter()
            if mode == "Encrypt":
                result = monoalphabetic_encrypt(text_input, mono_key)
            else:
                result = monoalphabetic_decrypt(text_input, mono_key)
            t_elapsed = (time.perf_counter() - t0) * 1000
            
            st.text_area("Result Output:", result, height=120)
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Execution Time", f"{t_elapsed:.4f} ms")
            m2.metric("Text Length", f"{len(result)} chars")
            m3.metric("Key Space", "26! (~4.03x10^26)")
            
            st.subheader("Substitution Mapping Table")
            map_df = pd.DataFrame({
                "Plaintext Alphabet": list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"),
                "Cipher Substitution": list(mono_key.upper())
            }).T
            st.dataframe(map_df)
        except Exception as e:
            st.error(f"Error: {e}")

# ==========================================
# 3. PLAYFAIR CIPHER
# ==========================================
elif cipher_choice == "3. Playfair Cipher":
    st.header("3. Playfair Cipher")
    st.write("Encrypts pairs of letters (digraphs) using a 5x5 key matrix constructed from a keyword.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input & Configuration")
        mode = st.radio("Select Mode:", ["Encrypt", "Decrypt"], horizontal=True)
        text_input = st.text_area("Input Text:", "INSTRUMENT", height=120)
        key_input = st.text_input("Playfair Keyword:", "MONARCHY")
        
    with col2:
        st.subheader("Output & Telemetry")
        try:
            t0 = time.perf_counter()
            if mode == "Encrypt":
                result = playfair_encrypt(text_input, key_input)
            else:
                result = playfair_decrypt(text_input, key_input)
            t_elapsed = (time.perf_counter() - t0) * 1000
            
            st.text_area("Result Output:", result, height=120)
            
            m1, m2 = st.columns(2)
            m1.metric("Execution Time", f"{t_elapsed:.4f} ms")
            m2.metric("Text Length", f"{len(result)} chars")
            
            st.subheader("5x5 Playfair Matrix Visualizer")
            matrix = create_playfair_matrix(key_input)
            matrix_df = pd.DataFrame(matrix, columns=["Col 1", "Col 2", "Col 3", "Col 4", "Col 5"])
            st.table(matrix_df)
        except Exception as e:
            st.error(f"Error: {e}")

# ==========================================
# 4. HILL CIPHER
# ==========================================
elif cipher_choice == "4. Hill Cipher (2x2)":
    st.header("4. Hill Cipher (2x2 Matrix)")
    st.write("Polygraphic substitution cipher using linear algebra matrix multiplication modulo 26.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input & Configuration")
        mode = st.radio("Select Mode:", ["Encrypt", "Decrypt"], horizontal=True)
        text_input = st.text_area("Input Text:", "HELP", height=120)
        
        st.write("Enter 2x2 Key Matrix [[a, b], [c, d]]:")
        m_col1, m_col2 = st.columns(2)
        a = m_col1.number_input("Element [1][1]", value=7)
        b = m_col2.number_input("Element [1][2]", value=8)
        c = m_col1.number_input("Element [2][1]", value=11)
        d = m_col2.number_input("Element [2][2]", value=11)
        
        key_matrix = [[int(a), int(b)], [int(c), int(d)]]
        
    with col2:
        st.subheader("Output & Telemetry")
        try:
            t0 = time.perf_counter()
            if mode == "Encrypt":
                result = hill_encrypt(text_input, key_matrix)
            else:
                result = hill_decrypt(text_input, key_matrix)
            t_elapsed = (time.perf_counter() - t0) * 1000
            
            st.text_area("Result Output:", result, height=120)
            
            m1, m2 = st.columns(2)
            m1.metric("Execution Time", f"{t_elapsed:.4f} ms")
            m2.metric("Text Length", f"{len(result)} chars")
            
            st.subheader("Matrix Multiplication Formula")
            st.latex(r"C = \begin{pmatrix} a & b \\ c & d \end{pmatrix} \cdot \begin{pmatrix} P_1 \\ P_2 \end{pmatrix} \pmod{26}")
            st.write(f"Current Matrix Key:\n`[{a}, {b}]`\n`[{c}, {d}]`")
        except Exception as e:
            st.error(f"Error: {e}")

# ==========================================
# 5. VIGENÈRE CIPHER
# ==========================================
elif cipher_choice == "5. Vigenère Cipher":
    st.header("5. Vigenère Cipher")
    st.write("Polyalphabetic cipher using repeating keyword shifts.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input & Configuration")
        mode = st.radio("Select Mode:", ["Encrypt", "Decrypt"], horizontal=True)
        text_input = st.text_area("Input Text:", "ATTACKATDAWN", height=120)
        key_input = st.text_input("Key Phrase:", "LEMON")
        
    with col2:
        st.subheader("Output & Telemetry")
        try:
            t0 = time.perf_counter()
            if mode == "Encrypt":
                result = vigenere_encrypt(text_input, key_input)
            else:
                result = vigenere_decrypt(text_input, key_input)
            t_elapsed = (time.perf_counter() - t0) * 1000
            
            st.text_area("Result Output:", result, height=120)
            
            m1, m2 = st.columns(2)
            m1.metric("Execution Time", f"{t_elapsed:.4f} ms")
            m2.metric("Text Length", f"{len(result)} chars")
            
            st.subheader("Repeating Key Alignment")
            clean_text = sanitize_text(text_input)
            clean_key = sanitize_text(key_input)
            if clean_key:
                repeated_key = (clean_key * ((len(clean_text) // len(clean_key)) + 1))[:len(clean_text)]
                st.code(f"Text: {clean_text}\nKey : {repeated_key}")
        except Exception as e:
            st.error(f"Error: {e}")

# ==========================================
# 6. ONE-TIME PAD
# ==========================================
elif cipher_choice == "6. One-Time Pad":
    st.header("6. One-Time Pad (Vernam Cipher)")
    st.write("Perfect secrecy stream cipher using a non-repeating key of length equal to the message.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input & Configuration")
        mode = st.radio("Select Mode:", ["Encrypt", "Decrypt"], horizontal=True)
        text_input = st.text_area("Input Text:", "TOPSECRET", height=120)
        
        clean_len = len(sanitize_text(text_input))
        if st.button("✨ Auto-Generate Random Key"):
            st.session_state["otp_key"] = generate_otp_key(clean_len or 10)
            
        otp_key = st.text_input("OTP Key (Length >= Text Length):", st.session_state.get("otp_key", generate_otp_key(clean_len or 10)))
        
    with col2:
        st.subheader("Output & Telemetry")
        try:
            t0 = time.perf_counter()
            if mode == "Encrypt":
                result = otp_encrypt(text_input, otp_key)
            else:
                result = otp_decrypt(text_input, otp_key)
            t_elapsed = (time.perf_counter() - t0) * 1000
            
            st.text_area("Result Output:", result, height=120)
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Execution Time", f"{t_elapsed:.4f} ms")
            m2.metric("Text Length", f"{len(result)} chars")
            m3.metric("Security Level", "Unbreakable")
        except Exception as e:
            st.error(f"Error: {e}")

# ==========================================
# 7. RAIL FENCE CIPHER
# ==========================================
elif cipher_choice == "7. Rail Fence Cipher":
    st.header("7. Rail Fence Cipher")
    st.write("Transposition cipher that writes message characters in a diagonal zig-zag pattern across depth rails and reads them row by row.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input & Configuration")
        mode = st.radio("Select Mode:", ["Encrypt", "Decrypt"], horizontal=True)
        text_input = st.text_area("Input Text:", "DEFENDTHEEASTWALL", height=120)
        rails = st.slider("Number of Rails (Depth):", 2, 10, 3)
        
    with col2:
        st.subheader("Output & Telemetry")
        try:
            t0 = time.perf_counter()
            if mode == "Encrypt":
                result = rail_fence_encrypt(text_input, rails)
            else:
                result = rail_fence_decrypt(text_input, rails)
            t_elapsed = (time.perf_counter() - t0) * 1000
            
            st.text_area("Result Output:", result, height=120)
            
            m1, m2 = st.columns(2)
            m1.metric("Execution Time", f"{t_elapsed:.4f} ms")
            m2.metric("Text Length", f"{len(result)} chars")
        except Exception as e:
            st.error(f"Error: {e}")

    # Visual Working Section
    st.subheader("🌊 Rail Fence Zig-Zag Working Visualizer")
    clean_text = sanitize_text(text_input)
    if clean_text:
        n = len(clean_text)
        fence = [["." for _ in range(n)] for _ in range(rails)]
        r, direction = 0, 1
        for i in range(n):
            fence[r][i] = clean_text[i]
            r += direction
            if r == 0 or r == rails - 1:
                direction = -direction
                
        df_fence = pd.DataFrame(fence, index=[f"Rail {i+1}" for i in range(rails)], columns=[f"P{i+1}" for i in range(n)])
        st.write("**Diagonal Wave Matrix Grid:**")
        st.dataframe(df_fence)
        
        row_readout = ["".join([ch for ch in row if ch != "."]) for row in fence]
        st.write("**Row-by-Row Ciphertext Construction:**")
        for idx, r_str in enumerate(row_readout):
            st.code(f"Rail {idx+1} readout ➔ '{r_str}'")

# ==========================================
# 8. COLUMNAR TRANSPOSITION
# ==========================================
elif cipher_choice == "8. Columnar Transposition Cipher":
    st.header("8. Columnar Transposition Cipher")
    st.write("Transposition cipher arranging text into a grid of columns defined by a keyword and reading out columns in alphabetical key order.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input & Configuration")
        mode = st.radio("Select Mode:", ["Encrypt", "Decrypt"], horizontal=True)
        text_input = st.text_area("Input Text:", "MEETMEAFTERTHEPARTY", height=120)
        col_key = st.text_input("Column Keyword:", "HACK")
        
    with col2:
        st.subheader("Output & Telemetry")
        try:
            t0 = time.perf_counter()
            if mode == "Encrypt":
                result = columnar_encrypt(text_input, col_key)
            else:
                result = columnar_decrypt(text_input, col_key)
            t_elapsed = (time.perf_counter() - t0) * 1000
            
            st.text_area("Result Output:", result, height=120)
            
            m1, m2 = st.columns(2)
            m1.metric("Execution Time", f"{t_elapsed:.4f} ms")
            m2.metric("Text Length", f"{len(result)} chars")
        except Exception as e:
            st.error(f"Error: {e}")

    # Visual Working Section
    st.subheader("📊 Columnar Transposition Grid Working Visualizer")
    clean_text = sanitize_text(text_input)
    clean_key = sanitize_key_alphanumeric(col_key)
    
    if clean_text and clean_key:
        num_cols = len(clean_key)
        import math
        num_rows = math.ceil(len(clean_text) / num_cols)
        padded_text = clean_text.ljust(num_rows * num_cols, 'X')
        
        # Grid construction
        matrix = [list(padded_text[i:i+num_cols]) for i in range(0, len(padded_text), num_cols)]
        
        # Sort order
        key_order = sorted(range(len(clean_key)), key=lambda k: (clean_key[k], k))
        rank_order = [0] * num_cols
        for rank, col_idx in enumerate(key_order):
            rank_order[col_idx] = rank + 1
            
        col_headers = [f"'{clean_key[i]}' (Order {rank_order[i]})" for i in range(num_cols)]
        df_grid = pd.DataFrame(matrix, columns=col_headers, index=[f"Row {r+1}" for r in range(num_rows)])
        
        st.write("**Transposition Grid Matrix (Padded with 'X'):**")
        st.dataframe(df_grid)
        
        st.write("**Column Read-out Sequence in Alphabetical Rank Order:**")
        col_readouts = []
        for rank, col_idx in enumerate(key_order):
            col_str = "".join([matrix[r][col_idx] for r in range(num_rows)])
            col_readouts.append(col_str)
            st.code(f"Rank {rank+1} (Col '{clean_key[col_idx]}'): '{col_str}'")

# ==========================================
# 9. BENCHMARK COMPARATOR
# ==========================================
elif cipher_choice == "9. Compare Algorithms (Benchmark)":
    st.header("9. Algorithm Performance & Security Comparison")
    st.write("Live performance benchmark measuring encryption/decryption latency and key space complexity.")
    
    sample_text = st.text_input("Sample Text for Benchmark:", "NETWORKSECURITYPROJECT2026")
    
    if st.button("▶ Run Live Performance Benchmark"):
        results = benchmark_ciphers(sample_text)
        df_results = pd.DataFrame(results)
        
        st.dataframe(df_results, width=900)
        
        st.subheader("Execution Latency (ms)")
        st.bar_chart(df_results.set_index("name")["time_ms"])

# ==========================================
# 10. FILE ENCRYPTION
# ==========================================
elif cipher_choice == "10. File Encryption & Decryption":
    st.header("10. Text File Encryption & Decryption Module")
    
    uploaded_file = st.file_uploader("Upload Text File (.txt)", type=["txt"])
    
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        st.text_area("File Content Preview:", content, height=150)
        
        col1, col2 = st.columns(2)
        with col1:
            cipher_file = st.selectbox("Select Cipher Algorithm:", ["Caesar Cipher", "Vigenère Cipher", "Rail Fence Cipher"])
            file_action = st.radio("Action:", ["Encrypt", "Decrypt"], horizontal=True)
            
        with col2:
            if cipher_file == "Caesar Cipher":
                file_key = st.number_input("Shift Key:", value=5)
                res = caesar_encrypt(content, file_key) if file_action == "Encrypt" else caesar_decrypt(content, file_key)
            elif cipher_file == "Vigenère Cipher":
                file_key = st.text_input("Key Phrase:", "FILEKEY")
                res = vigenere_encrypt(content, file_key) if file_action == "Encrypt" else vigenere_decrypt(content, file_key)
            else:
                file_key = st.slider("Rails:", 2, 10, 3)
                res = rail_fence_encrypt(content, file_key) if file_action == "Encrypt" else rail_fence_decrypt(content, file_key)
                
            st.text_area("Processed Output Preview:", res, height=150)
            
            st.download_button(
                label=f"💾 Download {file_action}ed File",
                data=res,
                file_name=f"processed_{uploaded_file.name}",
                mime="text/plain"
            )

# ==========================================
# 11. FREQUENCY ANALYSIS
# ==========================================
elif cipher_choice == "11. Text Frequency Analysis":
    st.header("11. Text Character Frequency Analysis")
    st.write("Calculates distribution of letter frequencies for cryptanalysis.")
    
    freq_input = st.text_area("Enter Text to Analyze:", "NETWORK SECURITY PROJECT CRYPTOGRAPHY TOOLKIT", height=150)
    
    if freq_input:
        freqs = calculate_letter_frequency(freq_input)
        freq_df = pd.DataFrame(list(freqs.items()), columns=["Letter", "Frequency (%)"])
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.dataframe(freq_df)
        with col2:
            st.bar_chart(freq_df.set_index("Letter"))

# ==========================================
# 12. CRYPTOGRAPHY CONCEPT GUIDE
# ==========================================
elif cipher_choice == "12. Cryptography Concept Guide":
    st.header("12. Classical Cryptography Concepts & Mathematical Formulas")
    
    st.markdown("""
    ### 1. Caesar Cipher
    - **Formula**: $E(x) = (x + k) \pmod{26}$, $D(x) = (x - k + 26) \pmod{26}$
    - **Key Space**: 25 possible keys. Vulnerable to brute-force frequency analysis.

    ### 2. Monoalphabetic Cipher
    - **Formula**: $\pi: \mathcal{A} \to \mathcal{A}'$ (1-to-1 permutation table)
    - **Key Space**: $26! \approx 4.03 \times 10^{26}$ keys.

    ### 3. Playfair Cipher
    - **Grid**: $5 \times 5$ matrix combining keyword and remaining alphabets (I/J merged).
    - **Rules**: Digraph pairs in same row shift right; same column shift down; rectangle corners swap.

    ### 4. Hill Cipher
    - **Formula**: $C = [K] \cdot [P] \pmod{26}$
    - **Decryption Matrix**: $P = [K]^{-1} \cdot [C] \pmod{26}$. Requires $\gcd(\det(K), 26) = 1$.

    ### 5. Vigenère Cipher
    - **Formula**: $C_i = (P_i + K_{i \pmod L}) \pmod{26}$
    - **Key Space**: $26^L$ (where $L$ is key length).

    ### 6. One-Time Pad (OTP)
    - **Formula**: $C_i = (P_i + K_i) \pmod{26}$
    - **Security**: Perfect Secrecy (Shannon Theorem) provided key is random and never reused.

    ### 7. Rail Fence Cipher
    - **Mechanism**: Transposition cipher placing letters in diagonal wave rails across depth $R$.

    ### 8. Columnar Transposition Cipher
    - **Mechanism**: Arranges plaintext into grid of $K$ columns and reads columns in sorted keyword order.
    """)
