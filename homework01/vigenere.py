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
    for i, value in enumerate(plaintext):
        if value.isupper():
            keyword = keyword.upper()
        else:
            keyword = keyword.lower()
    key_ord = [ord(i) for i in keyword]
    plaintext_ord = [ord(i) for i in plaintext]
    for i, value in enumerate(plaintext):
        if value.isalpha():
            if value.isupper():
                ciphertext += chr(((plaintext_ord[i] + key_ord[i % key_lenght]) % 26) + ord('A'))
            elif value.islower():
                ciphertext += chr(((plaintext_ord[i] - 12 + key_ord[i % key_lenght]) % 26) + ord('a'))
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
    for i, value in enumerate(ciphertext):
        if value.isupper():
            keyword = keyword.upper()
        elif value.islower():
            keyword = keyword.lower()
    key_ord = [ord(i) for i in keyword]
    ciphertext_ord = [ord(i) for i in ciphertext]
    for i, value in enumerate(ciphertext):
        if value.isalpha():
            if value.isupper():
                plaintext += chr(((ciphertext_ord[i] - key_ord[i % key_lenght]) % 26) + ord('A'))
            elif value.islower():
                plaintext += chr(((ciphertext_ord[i] - key_ord[i % key_lenght]) % 26) + ord('a'))
        else:
            plaintext += ciphertext[i]
    return plaintext
