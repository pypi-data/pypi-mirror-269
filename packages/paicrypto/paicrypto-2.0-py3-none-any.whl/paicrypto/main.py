import hashlib
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import getPrime, inverse
from Crypto.Cipher import DES3
import socket
import time
import math


# python3 pydoc.py  -p 8000
# Server ready at http://localhost:8000/
# Server commands: [b]rowser, [q]uit


class paicrypto:

    def checkSize(self, keylen ,datalen, standardKeyLen, standardDataLen):
        if keylen != standardKeyLen:
            raise ValueError("Key length must be 8 bytes")
            return False
        if datalen % standardDataLen != 0:
            raise ValueError("Data length must be multiple of 8 bytes")
            return False
        
        return True

    def desEncrypt3(self, data, key):
        keylen = len(key)
        datalen = len(data)
        if not self.checkSize(keylen, datalen, 24, 8):
            return False
    
        cipher = DES3.new(key.encode(), DES3.MODE_ECB)
        cipherText = cipher.encrypt(data.encode())
        return cipherText
    
    def desDecrypt3(self, data, key):
        keylen = len(key)
        datalen = len(data)
        if not self.checkSize(keylen, datalen, 24, 8):
            return False
    
        cipher = DES3.new(key.encode(), DES3.MODE_ECB)
        plainText = cipher.decrypt(data)
        return plainText
    
    

    def desEncrypt(self, data, key):
        keylen = len(key)
        datalen = len(data)
        if not self.checkSize(keylen, datalen, 8, 8):
            return False
    
        cipher = DES.new(key.encode(), DES.MODE_ECB)
        cipherText = cipher.encrypt(data.encode())
        return  cipherText
    
    def desDecrypt(self, data, key):
        keylen = len(key)
        datalen = len(data)
        if not self.checkSize(keylen, datalen, 8, 8):
            return False
    
        cipher = DES.new(key.encode(), DES.MODE_ECB)
        plainText = cipher.decrypt(data)
        return  plainText
    
    def desPaddedEncrypt(self, data, key):
        if len(data) % 8 != 0:
            data = pad(data.encode(), 8)
        keylen = len(key)
        datalen = len(data)
        if not self.checkSize(keylen, datalen, 8, 8):
            return False
        
        cipher = DES.new(key.encode(), DES.MODE_ECB)
        cipherText = cipher.encrypt(data)
        return cipherText
    
    def desPaddedDecrypt(self, data, key):
        keylen = len(key)
        datalen = len(data)
        if not self.checkSize(keylen, datalen, 8, 8):
            return False
        
        cipher = DES.new(key.encode(), DES.MODE_ECB)
        plainText = cipher.decrypt(data)
        return unpad(plainText, DES.block_size).decode()
    

    def aesEncrypt(self, data, key):
        keylen = len(key)
        datalen = len(data)
        if not self.checkSize(keylen, datalen, 16, 16):
            return False
        
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        cipherText = cipher.encrypt(data.encode())
        return cipherText
    
    def aesDecrypt(self, data, key):
        keylen = len(key)
        datalen = len(data)
        if not self.checkSize(keylen, datalen, 16, 16):
            return False
        
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        plainText = cipher.decrypt(data)
        return plainText.decode()
    
    def aesPaddedEncrypt(self, data, key):
        if len(data) % 16 != 0:
            data = pad(data.encode(), 16)
        keylen = len(key)
        datalen = len(data)
        if not self.checkSize(keylen, datalen, 16, 16):
            return False
        
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        cipherText = cipher.encrypt(data)
        return cipherText
    
    def aesPaddedDecrypt(self, data, key):
        keylen = len(key)
        datalen = len(data)
        if not self.checkSize(keylen, datalen, 16, 16):
            return False
        
        cipher = AES.new(key.encode(), AES.MODE_ECB)
        plainText = cipher.decrypt(data)
        return unpad(plainText, AES.block_size).decode()
    
    def rsaEncrypt(self, data, key):
        cipher = PKCS1_OAEP.new(key)
        cipherText = cipher.encrypt(data.encode())
        return cipherText
    
    def rsaDecrypt(self, data, key):
        cipher = PKCS1_OAEP.new(key)
        plainText = cipher.decrypt(data)
        return plainText.decode()
    
    def rsaKeyGen(self):
        key = RSA.generate(2048)
        return key
    
    def elgamalKeyGen(self):
        p = getPrime(128)
        g = getPrime(128)
        x = getPrime(128)
        y = pow(g, x, p)
        return (p, g, x, y)
    
    def elgamalEncrypt(self, data, key):
        p, g, x, y = key
        k = getPrime(128)
        a = pow(g, k, p)
        b = (pow(y, k, p) * data) % p
        return (a, b)
    
    def elgamalDecrypt(self, data, key):
        p, g, x, y = key
        a, b = data
        s = pow(a, x, p)
        plainText = (b * inverse(s, p)) % p
        return plainText
    
    def deffieHellmanKeyGen(self):
        p = getPrime(128)
        g = getPrime(128)
        x = getPrime(128)
        y = pow(g, x, p)
        return (p, g, x, y)
    
    def deffieHellmanEncrypt(self, data, key):
        p, g, x, y = key
        k = getPrime(128)
        a = pow(g, k, p)
        b = (pow(y, k, p) * data) % p
        return (a, b)
    
    def deffieHellmanDecrypt(self, data, key):
        p, g, x, y = key
        a, b = data
        s = pow(a, x, p)
        plainText = (b * inverse(s, p)) % p
        return plainText
    
    #Deffiehellman with socket
    def socketDeffieHellmanKeyGen(self):
        p = getPrime(128)
        g = getPrime(128)
        x = getPrime(128)
        y = pow(g, x, p)
        return (p, g, x, y)
    
    def socketDeffieHellmanEncryptServer(self, data, key,port):
        s = socket.socket()
        s.bind(('', port))
        s.listen(5)
        c, addr = s.accept()
        p, g, x, y = key
        k = getPrime(128)
        a = pow(g, k, p)
        c.send(str(a).encode())
        b = int(c.recv(1024).decode())
        c.close()
        s.close()
        return (a, b)
    
    def socketDeffieHellmanDecryptClient(self, data, key, port):
        s = socket.socket()
        s.connect(('localhost', port))
        p, g, x, y = key
        a, b = data
        s.send(str(a).encode())
        b = int(s.recv(1024).decode())
        s.close()
        return (a, b)
    
    def socketDeffieHellmanDecryptServer(self, data, key, port):
        s = socket.socket()
        s.bind(('', port))
        s.listen(5)
        c, addr = s.accept()
        p, g, x, y = key
        a, b = data
        s.send(str(b).encode())
        b = int(s.recv(1024).decode())
        c.close()
        s.close()
        return b
    
    def socketDeffieHellmanEncryptClient(self, data, key, port):
        s = socket.socket()
        s.connect(('localhost', port))
        p, g, x, y = key
        k = getPrime(128)
        a = pow(g, k, p)
        s.send(str(a).encode())
        b = int(s.recv(1024).decode())
        s.close()
        return (a, b)
    

    
    
    
    
    def sha256(self, data):
        return hashlib.sha256(data.encode()).hexdigest()
    
    def sha512(self, data):
        return hashlib.sha512(data.encode()).hexdigest()
    
    def sha1(self, data):
        return hashlib.sha1(data.encode()).hexdigest()
    
    def md5(self, data):
        return hashlib.md5(data.encode()).hexdigest()
    
    def sha224(self, data):
        return hashlib.sha224(data.encode()).hexdigest()
    
    def caesar_encrypt(self, text, shift):
        result = ""
        for char in text:
            if char.isalpha():
                # For uppercase letters
                if char.isupper():
                    result += chr((ord(char) + shift - 65) % 26 + 65)
                # For lowercase letters
                elif char.islower():
                    result += chr((ord(char) + shift - 97) % 26 + 97)
            elif char.isdigit():
                # For digits
                result += str((int(char) + shift) % 10)
            else:
                # For non-alphanumeric characters
                result += char
        return result
    
    def caesar_decrypt(self, text, shift):
        result = ""

        for char in text:
            if char.isalpha():
                # For uppercase letters
                if char.isupper():
                    result += chr((ord(char) - shift - 65) % 26 + 65)
                # For lowercase letters
                elif char.islower():
                    result += chr((ord(char) - shift - 97) % 26 + 97)
            elif char.isdigit():
                # For digits
                result += str((int(char) - shift) % 10)
            else:
                # For non-alphanumeric characters
                result += char

        return result 

    def vigenere_encrypt(self,plaintext, key):
        if not key.isalpha():
            raise ValueError("Key must contain only alphabetic characters")
            return False
        
        encrypted_text = ""
        key = key.upper()
        key_index = 0

        for char in plaintext:
            if char.isalpha():
                # Convert character to uppercase
                char = char.upper()
                # Get the corresponding shift value from the key
                shift = ord(key[key_index]) - 65
                # Encrypt the character
                if char.isupper():
                    encrypted_text += chr((ord(char) + shift - 65) % 26 + 65)
                elif char.islower():
                    encrypted_text += chr((ord(char) + shift - 97) % 26 + 97)
                # Move to the next letter in the key
                key_index = (key_index + 1) % len(key)
            else:
                # Non-alphabetic characters remain unchanged
                encrypted_text += char

        return encrypted_text

    def vigenere_decrypt(self,ciphertext, key):
        if not key.isalpha():
            raise ValueError("Key must contain only alphabetic characters")
            return False
        decrypted_text = ""
        key = key.upper()
        key_index = 0

        for char in ciphertext:
            if char.isalpha():
                # Convert character to uppercase
                char = char.upper()
                # Get the corresponding shift value from the key
                shift = ord(key[key_index]) - 65
                # Decrypt the character
                if char.isupper():
                    decrypted_text += chr((ord(char) - shift - 65) % 26 + 65)
                elif char.islower():
                    decrypted_text += chr((ord(char) - shift - 97) % 26 + 97)
                # Move to the next letter in the key
                key_index = (key_index + 1) % len(key)
            else:
                # Non-alphabetic characters remain unchanged
                decrypted_text += char

        return decrypted_text
    

    def railfence_encrypt(self,lst, numrails):
        fence = [[None] * len(lst) for _ in range(numrails)]
        rails = list(range(numrails - 1)) + list(range(numrails - 1, 0, -1))
        for n, x in enumerate(lst):
            fence[rails[n % len(rails)]][n] = x

        if 0:  # debug
            for rail in fence:
                print(''.join('.' if c is None else str(c) for c in rail))

        return [c for rail in fence for c in rail if c is not None]
    
    def Railencode(self,text, n):
        return ''.join(self.railfence_encrypt(text, n))
    
    def raildecode(self,text, n):
        rng = list(range(len(text)))
        pos = self.railfence_encrypt(rng, n)
        return ''.join(text[pos.index(n)] for n in rng)
    

    def columnar_transposition_encrypt(self,text, key):
        cipher = ""
        k_indx = 0
        msg_len = float(len(text))
        msg_lst = list(text)
        key_lst = sorted(list(key))
        col = len(key)
        row = int(math.ceil(msg_len / col))
        fill_null = int((row * col) - msg_len)
        msg_lst.extend('_' * fill_null)
        matrix = [msg_lst[i: i + col] for i in range(0, len(msg_lst), col)]
        for _ in range(col):
            curr_idx = key.index(key_lst[k_indx])
            cipher += ''.join([row[curr_idx] for row in matrix])
            k_indx += 1
        return cipher
    def columnar_transposition_decrypt(self, text, key):
        msg = ""
        k_indx = 0
        msg_indx = 0
        msg_len = float(len(text))
        msg_lst = list(text)
        col = len(key)
        row = int(math.ceil(msg_len / col))
        key_lst = sorted(list(key))
        dec_cipher = []
        for _ in range(row):
            dec_cipher += [[None] * col]
        for _ in range(col):
            curr_idx = key.index(key_lst[k_indx])
            for j in range(row):
                dec_cipher[j][curr_idx] = msg_lst[msg_indx]
                msg_indx += 1
            k_indx += 1
        try:
            msg = ''.join(sum(dec_cipher, []))
        except TypeError:
            raise TypeError("This program cannot", "handle repeating words.")
        null_count = msg.count('_')
        if null_count > 0:
            return msg[:-null_count]
        return msg



