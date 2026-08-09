# -*- coding: utf-8 -*-
"""
test_ciphers.py - Automated Unit Verification for all 8 ciphers
"""

import unittest
from ciphers_lib import (
    caesar_encrypt, caesar_decrypt,
    monoalphabetic_encrypt, monoalphabetic_decrypt, generate_monoalphabetic_key,
    playfair_encrypt, playfair_decrypt,
    hill_encrypt, hill_decrypt,
    vigenere_encrypt, vigenere_decrypt,
    otp_encrypt, otp_decrypt, generate_otp_key,
    rail_fence_encrypt, rail_fence_decrypt,
    columnar_encrypt, columnar_decrypt
)

class TestClassicalCiphers(unittest.TestCase):

    def test_caesar(self):
        pt = "NETWORKSECURITY"
        shift = 5
        ct = caesar_encrypt(pt, shift)
        dec = caesar_decrypt(ct, shift)
        self.assertEqual(pt, dec)

    def test_monoalphabetic(self):
        pt = "HELLOWORLD"
        key = generate_monoalphabetic_key()
        ct = monoalphabetic_encrypt(pt, key)
        dec = monoalphabetic_decrypt(ct, key)
        self.assertEqual(pt, dec)

    def test_playfair(self):
        pt = "INSTRUMENT"
        key = "MONARCHY"
        ct = playfair_encrypt(pt, key)
        dec = playfair_decrypt(ct, key)
        self.assertTrue("INSTRUMENT" in dec or "INSTRUMEN" in dec)

    def test_hill(self):
        pt = "HELP"
        key_matrix = [[7, 8], [11, 11]]
        ct = hill_encrypt(pt, key_matrix)
        dec = hill_decrypt(ct, key_matrix)
        self.assertEqual(pt, dec)

    def test_vigenere(self):
        pt = "ATTACKATDAWN"
        key = "LEMON"
        ct = vigenere_encrypt(pt, key)
        dec = vigenere_decrypt(ct, key)
        self.assertEqual(pt, dec)

    def test_otp(self):
        pt = "TOPSECRET"
        key = generate_otp_key(len(pt))
        ct = otp_encrypt(pt, key)
        dec = otp_decrypt(ct, key)
        self.assertEqual(pt, dec)

    def test_rail_fence(self):
        pt = "DEFENDTHEEASTWALL"
        rails = 3
        ct = rail_fence_encrypt(pt, rails)
        dec = rail_fence_decrypt(ct, rails)
        self.assertEqual(pt, dec)

    def test_columnar(self):
        pt = "MEETMEAFTERTHEPARTY"
        key = "HACK"
        ct = columnar_encrypt(pt, key)
        dec = columnar_decrypt(ct, key)
        self.assertTrue(dec.startswith(pt))

    def test_columnar_numeric_key(self):
        pt = "MEETMEAFTERTHEPARTY"
        key = "1243"
        ct = columnar_encrypt(pt, key)
        dec = columnar_decrypt(ct, key)
        self.assertTrue(dec.startswith(pt))

if __name__ == '__main__':
    unittest.main()
