def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    key_lenght = len(keyword)
    for i in range(len(plaintext)):
        if plaintext[i].isupper():
            keyword = keyword.upper()
            key_ord = [ord(i) for i in keyword]
        else:
            keyword = keyword.lower()
            key_ord = [ord(i) for i in keyword]
    plaintext_ord = [ord(i) for i in plaintext]
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            if plaintext[i].isupper():
                ciphertext += chr(((plaintext_ord[i] + key_ord[i % key_lenght]) % 26) + 65)
            elif plaintext[i].islower():
                ciphertext += chr(((plaintext_ord[i] - 12 + key_ord[i % key_lenght]) % 26) + 97)
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""
    key_lenght = len(keyword)
    for i in range(len(ciphertext)):
        if ciphertext[i].isupper():
            keyword = keyword.upper()
            key_ord = [ord(i) for i in keyword]
        elif ciphertext[i].islower():
            keyword = keyword.lower()
            key_ord = [ord(i) for i in keyword]
    ciphertext_ord = [ord(i) for i in ciphertext]
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            if ciphertext[i].isupper():
                plaintext += chr(((ciphertext_ord[i] - key_ord[i % key_lenght]) % 26) + 65)
            elif ciphertext[i].islower():
                plaintext += chr(((ciphertext_ord[i] - key_ord[i % key_lenght]) % 26) + 97)
        else:
            plaintext += ciphertext[i]
    return plaintext
