from cipher import Cipher

class Autokey(Cipher):
    def __init__(self, text, key):
        '''
        Initializes an Autokey cipher object
        Parameters: text (inherited from superclass Cipher), key (str)
        Side effects: initializes an Autokey cipher obejct with the text to be encoded/decoded, and the key to encode/decode it with
        '''
        super().__init__(text)
        self.key = key

    def check_valid_key(self):
        '''
        Check if the key is valid: a string with letters only (no spaces, punctuation, or special characters)
        Parameters: none
        Side effects: none
        Returns: True (valid) or False (invalid)
        '''
        if len(self.key) > 0 and self.key.isalpha():
            return True
        return False

    def set_valid_key(self):
        '''
        Prompts user to enter a valid key
        Parameters: none
        Side effects: updates key to a new value
        Returns: none
        '''
        while self.check_valid_key() == False:
            new_key = input("Invalid key. Please enter a string with characters only: ")
            self.key = new_key

    def extend_key(self):
        '''
        Parameters: none
        Side effects: extends the key to match the length of the text
        - appends the message to the end of the key+message until its length > len(text)
        Returns: extended_key
        '''
        key = self.key.lower()
        text = ''.join(filter(str.isalpha, self.get_text())).lower()
        extended_key = key + text
        while len(extended_key) < len(self.get_text()):
            extended_key += text
        return extended_key

    def encrypt(self):
        '''
        Encrypt a plaintext via Autokey cipher
        Parameters: none
        Side effects: 
        - sets a valid plaintext and key
        - extends the key to match the length of the plaintext
        Returns: encrypted ciphertext (str)
        '''
        self.set_valid_text()
        self.set_valid_key()
        full_key = self.extend_key()
        ciphertext = ''
        j = 0
        for i in range(len(self.get_text())):
            char = self.get_text()[i]
            key = full_key[j]
            if char in self.alphabet_upper:
                ciphertext += self.alphabet_upper[(self.alphabet_upper.index(char) + self.alphabet_lower.index(key)) % 26]
                j += 1
            elif char in self.alphabet_lower:
                ciphertext += self.alphabet_lower[(self.alphabet_lower.index(char) + self.alphabet_lower.index(key)) % 26]
                j += 1
            else:
                ciphertext += char
        return ciphertext

    def decrypt(self):
        '''
        Decrypt a ciphertext via Autokey cipher
        Parameters: none
        Side effects:
        - sets a valid ciphertext and key
        - extends the key to match the length of the ciphertext
        Returns: decrypted plaintext (str)
        '''
        self.set_valid_text()
        self.set_valid_key()
        full_key = self.key.lower()
        plaintext = ''
        j = 0
        for i in range(len(self.get_text())):
            char = self.get_text()[i]
            key = full_key[j]
            if char in self.alphabet_upper:
                plaintext += self.alphabet_upper[(self.alphabet_upper.index(char) - self.alphabet_lower.index(key)) % 26]
                full_key += self.alphabet_upper[(self.alphabet_upper.index(char) - self.alphabet_lower.index(key)) % 26].lower()
                j += 1
            elif char in self.alphabet_lower:
                plaintext += self.alphabet_lower[(self.alphabet_lower.index(char) - self.alphabet_lower.index(key) + 26) % 26]
                full_key += self.alphabet_lower[(self.alphabet_lower.index(char) - self.alphabet_lower.index(key) + 26) % 26]
                j += 1
            else:
                plaintext += char
        return plaintext
    
    def __str__(self):
        '''
        Overload string method to print info
        Parameters: none
        Side effects: prints info about Autokey cipher
        Returns: none
        '''
        description = "  The autokey cipher (aka. the autoclave cipher) is a symmetric, polyalphabetic substitution cipher similar to the Vigenère cipher, but with an additional twist: it incorporates the message (the plaintext) into the key. Most commonly, the key is generated by adding a short primer key to the front of the message, which is then used to encode the message.\n"
        description += "  In this way, it addresses one of the weaknesses of the Vigenère cipher--the periodic repetition of the keyword and increases the security of the cipher. Decryption methods like the Kasiski examination or index of coincidence analysis will not work on the ciphertext, unlike for similar ciphers that use a single repeated key.\n"
        description += "  A crucial weakness of the cipher, however, is that the plaintext is part of the key. That means that the key will likely contain common words at various points. The key can be attacked by using a dictionary of common words, bigrams, trigrams etc. and by attempting the decryption of the message by moving that word through the key until potentially-readable text appears.\n"
        description += "  For more detailed information, checkout these online resources! https://en.wikipedia.org/wiki/Autokey_cipher"
        return description

if __name__ == "__main__":
    e = Autokey("One believes things because one has been conditioned to believe them.", "OhBraveNewWorldThatHasSuchPeopleInIt") # from 'Brave New World' by Aldous Huxley & 'The Tempest' by Shakespeare
    print(f'Test - encryption\nPlain text: {e.get_text()}\nCipher text: {e.encrypt()}')
    
    d = Autokey("Ple kpe dgu G dto zlx fs xvre, hbikr gsauhi hee mx bukx, lms swqelh yl wayp mfx rzi zmlpsy: mc ymix eg yegr lvi udgug vw szdtyqam lhoz of oqf ldqa.", "Patriarchy") # from 'Woman at Point Zero' by Nawal El Saadawi
    print(f'Test - decryption\nPlain text: {d.get_text()}\nCipher text: {d.decrypt()}')
