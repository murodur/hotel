import codes


def encryption(text):
    decrypted_text = ""
    for symbol in text:
        decrypted_text += codes.encryption_code[symbol]
    return decrypted_text


def decryption(text):

    encrypted_text = ""

    symbols = [text[i:i+6] for i in range(0, len(text), 6)]

    for symbol in symbols:
        encrypted_text += decode(symbol)
    return encrypted_text


def decode(symbol):
    for key, value in codes.encryption_code.items():
        if value == symbol:
            return key
