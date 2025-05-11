def rot47_decrypt(text: str) -> str:
    result = []
    for char in text:
        ascii_val = ord(char)
        if 33 <= ascii_val <= 126:
            result.append(chr(33 + ((ascii_val - 33 - 47) % 94)))
        else:
            result.append(char)
    return ''.join(result)

key = 0x1A
def xor_encrypt(text):
    encrypted_bytes = [ord(c) ^ key for c in text]
    return ''.join(f"{b:02X}" for b in encrypted_bytes)

plaintext = "52592326272456287C2F2E782F7C7D7829457C78457F2F2E7B72792F7D7C727E7B2F7A782979792F72787F29722C2F54"
m = rot47_decrypt(bytes([b ^ key for b in bytes.fromhex(plaintext)]).decode('utf-8', errors='replace'))
print(m)