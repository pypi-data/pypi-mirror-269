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
    """
    A class that provides various encryption and decryption methods using different cryptographic algorithms.
    """

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
    
    # Rest of the code...
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
    

    def playfair_encrypt(self, plaintext, key):
        key = key.replace(" ", "").upper()
        matrix = self.create_playfair_matrix(key)
        plaintext = plaintext.upper().replace(" ", "")
        plaintext = self.prepare_playfair_text(plaintext)
        ciphertext = ""
        for i in range(0, len(plaintext), 2):
            pair = plaintext[i:i+2]
            encrypted_pair = self.playfair_encrypt_pair(pair, matrix)
            ciphertext += encrypted_pair
        return ciphertext

    def playfair_decrypt(self, ciphertext, key):
        key = key.replace(" ", "").upper()
        matrix = self.create_playfair_matrix(key)
        ciphertext = ciphertext.upper().replace(" ", "")
        plaintext = ""
        for i in range(0, len(ciphertext), 2):
            pair = ciphertext[i:i+2]
            decrypted_pair = self.playfair_decrypt_pair(pair, matrix)
            plaintext += decrypted_pair
        return plaintext

    def create_playfair_matrix(self, key):
        result = []
        for c in key:
            if c not in result:
                if c == 'J':
                    result.append('I')
                else:
                    result.append(c)
        for i in range(65, 91):
            if chr(i) not in result:
                if i == 73 and chr(74) not in result:
                    result.append("I")
                elif i != 73 and i != 74:
                    result.append(chr(i))
        matrix = [[0] * 5 for _ in range(5)]
        k = 0
        for i in range(5):
            for j in range(5):
                matrix[i][j] = result[k]
                k += 1
        return matrix

    def prepare_playfair_text(self, text):
        result = ""
        i = 0
        while i < len(text):
            result += text[i]
            if i + 1 < len(text):
                if text[i] == text[i + 1]:
                    result += 'X'
            i += 1
        if len(result) % 2 != 0:
            result += 'X'
        return result

    def playfair_encrypt_pair(self, pair, matrix):
        char1, char2 = pair[0], pair[1]
        row1, col1 = self.get_playfair_char_position(char1, matrix)
        row2, col2 = self.get_playfair_char_position(char2, matrix)
        if row1 == row2:
            encrypted_char1 = matrix[row1][(col1 + 1) % 5]
            encrypted_char2 = matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            encrypted_char1 = matrix[(row1 + 1) % 5][col1]
            encrypted_char2 = matrix[(row2 + 1) % 5][col2]
        else:
            encrypted_char1 = matrix[row1][col2]
            encrypted_char2 = matrix[row2][col1]
        return encrypted_char1 + encrypted_char2

    def playfair_decrypt_pair(self, pair, matrix):
        char1, char2 = pair[0], pair[1]
        row1, col1 = self.get_playfair_char_position(char1, matrix)
        row2, col2 = self.get_playfair_char_position(char2, matrix)
        if row1 == row2:
            decrypted_char1 = matrix[row1][(col1 - 1) % 5]
            decrypted_char2 = matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            decrypted_char1 = matrix[(row1 - 1) % 5][col1]
            decrypted_char2 = matrix[(row2 - 1) % 5][col2]
        else:
            decrypted_char1 = matrix[row1][col2]
            decrypted_char2 = matrix[row2][col1]
        return decrypted_char1 + decrypted_char2

    def get_playfair_char_position(self, char, matrix):
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == char:
                    return i, j
        return -1, -1

    def RC4key_scheduling(self, key):
        sched = [i for i in range(0, 256)]
        
        i = 0
        for j in range(0, 256):
            i = (i + sched[j] + key[j % len(key)]) % 256
            
            tmp = sched[j]
            sched[j] = sched[i]
            sched[i] = tmp
            
        return sched
        

    def RC4stream_generation(self, sched):
        stream = []
        i = 0
        j = 0
        while True:
            i = (1 + i) % 256
            j = (sched[i] + j) % 256
            
            tmp = sched[j]
            sched[j] = sched[i]
            sched[i] = tmp
            
            yield sched[(sched[i] + sched[j]) % 256]        

    def RC4encrypt(self, text, key):
        text = [ord(char) for char in text]
        key = [ord(char) for char in key]
        
        sched = self.RC4key_scheduling(key)
        key_stream = self.RC4stream_generation(sched)
        
        ciphertext = ''
        for char in text:
            enc = str(hex(char ^ next(key_stream))).upper()
            ciphertext += (enc)
            
        return ciphertext
        

    def RC4decrypt(self, ciphertext, key):
        ciphertext = ciphertext.split('0X')[1:]
        ciphertext = [int('0x' + c.lower(), 0) for c in ciphertext]
        key = [ord(char) for char in key]
        
        sched = self.RC4key_scheduling(key)
        key_stream = self.RC4stream_generation(sched)
        
        plaintext = ''
        for char in ciphertext:
            dec = str(chr(char ^ next(key_stream)))
            plaintext += dec
        
        return plaintext

    # RC4 encryption method
    def rc4_encrypt(self, plaintext, key):
        return self.RC4encrypt(plaintext, key)

    # RC4 decryption method
    def rc4_decrypt(self, ciphertext, key):
        return self.RC4decrypt(ciphertext, key)

    
    
    
    
    # Write a help function to display the available methods and their descriptions

    def help(self):
        print("Available methods and their descriptions:")
        print("\n")
        print("1. desEncrypt3(data, key): Encrypts the data using the DES3 algorithm with the given key.")
        print("2. desDecrypt3(data, key): Decrypts the data using the DES3 algorithm with the given key.")
        print("3. desEncrypt(data, key): Encrypts the data using the DES algorithm with the given key.")
        print("4. desDecrypt(data, key): Decrypts the data using the DES algorithm with the given key.")
        print("5. desPaddedEncrypt(data, key): Encrypts the padded data using the DES algorithm with the given key.")
        print("6. desPaddedDecrypt(data, key): Decrypts the padded data using the DES algorithm with the given key.")
        print("7. aesEncrypt(data, key): Encrypts the data using the AES algorithm with the given key.")
        print("8. aesDecrypt(data, key): Decrypts the data using the AES algorithm with the given key.")
        print("9. aesPaddedEncrypt(data, key): Encrypts the padded data using the AES algorithm with the given key.")
        print("10. aesPaddedDecrypt(data, key): Decrypts the padded data using the AES algorithm with the given key.")
        print("11. rsaEncrypt(data, key): Encrypts the data using the RSA algorithm with the given key.")
        print("12. rsaDecrypt(data, key): Decrypts the data using the RSA algorithm with the given key.")
        print("13. rsaKeyGen(): Generates an RSA key pair.")
        print("14. elgamalKeyGen(): Generates an ElGamal key pair.")
        print("15. elgamalEncrypt(data, key): Encrypts the data using the ElGamal algorithm with the given key.")
        print("16. elgamalDecrypt(data, key): Decrypts the data using the ElGamal algorithm with the given key.")
        print("17. deffieHellmanKeyGen(): Generates a Deffie-Hellman key pair.")
        print("18. deffieHellmanEncrypt(data, key): Encrypts the data using the Deffie-Hellman algorithm with the given key.")
        print("19. deffieHellmanDecrypt(data, key): Decrypts the data using the Deffie-Hellman algorithm with the given key.")
        print("20. socketDeffieHellmanKeyGen(): Generates a Deffie-Hellman key pair for socket communication.")
        print("21. socketDeffieHellmanEncryptServer(data, key, port): Encrypts the data using the Deffie-Hellman algorithm for server.")
        print("22. socketDeffieHellmanDecryptClient(data, key, port): Decrypts the data using the Deffie-Hellman algorithm for client.")
        print("23. socketDeffieHellmanDecryptServer(data, key, port): Decrypts the data using the Deffie-Hellman algorithm for server.")
        print("24. socketDeffieHellmanEncryptClient(data, key, port): Encrypts the data using the Deffie-Hellman algorithm for client.")
        print("25. sha256(data): Generates the SHA-256 hash of the data.")
        print("26. sha512(data): Generates the SHA-512 hash of the data.")
        print("27. sha1(data): Generates the SHA-1 hash of the data.")
        print("28. md5(data): Generates the MD5 hash of the data.")
        print("29. sha224(data): Generates the SHA-224 hash of the data.")
        print("30. caesar_encrypt(text, shift): Encrypts the text using the Caesar cipher with the given shift value.")
        print("31. caesar_decrypt(text, shift): Decrypts the text using the Caesar cipher with the given shift value.")
        print("32. vigenere_encrypt(plaintext, key): Encrypts the plaintext using the Vigenere cipher with the given key.")
        print("33. vigenere_decrypt(ciphertext, key): Decrypts the ciphertext using the Vigenere cipher with the given key.")
        print("34. railfence_encrypt(lst, numrails): Encrypts the list using the Rail Fence cipher with the given number of rails.")
        print("35. Railencode(text, n): Encrypts the text using the Rail Fence cipher with the given number of rails.")
        print("36. raildecode(text, n): Decrypts the text using the Rail Fence cipher with the given number of rails.")
        print("37. columnar_transposition_encrypt(text, key): Encrypts the text using the Columnar Transposition cipher with the given key.")
        print("38. columnar_transposition_decrypt(text, key): Decrypts the text using the Columnar Transposition cipher with the given key.")
        print("39. playfair_encrypt(plaintext, key): Encrypts the plaintext using the Playfair cipher with the given key.")
        print("40. playfair_decrypt(ciphertext, key): Decrypts the ciphertext using the Playfair cipher with the given key.")
        print("41. RC4key_scheduling (key): Generates the key scheduling for the RC4 algorithm with the given key.")
        print("42. RC4stream_generation(sched): Generates the key stream for the RC4 algorithm with the given key scheduling.")
        print("43. RC4encrypt(text, key): Encrypts the text using the RC4 algorithm with the given key.")
        print("44. RC4decrypt(ciphertext, key): Decrypts the ciphertext using the RC4 algorithm with the given key.")
        print("45. rc4_encrypt(plaintext, key): Encrypts the plaintext using the RC4 algorithm with the given key.")
        print("46. rc4_decrypt(ciphertext, key): Decrypts the ciphertext using the RC4 algorithm with the given key.")