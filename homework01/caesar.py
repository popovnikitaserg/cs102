def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in plaintext:
        if i.isalpha() and i.islower():
            new_i = ord(i) + shift
            if new_i > 122:
                new_i -= 26
            ciphertext += chr(new_i)
        elif i.isalpha() and i.isupper():
            new_i = ord(i) + shift
            if new_i > 90:
                new_i -= 26
            ciphertext += chr(new_i)
        else:
            ciphertext += i
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i in ciphertext:
        if i.isalpha() and i.islower():
            new_i = ord(i) - shift
            if new_i < 97:
                new_i += 26
            plaintext += chr(new_i)
        elif i.isalpha() and i.isupper():
            new_i = ord(i) - shift
            if new_i < 65:
                new_i += 26
            plaintext += chr(new_i)
        else:
            plaintext += i
    return plaintext