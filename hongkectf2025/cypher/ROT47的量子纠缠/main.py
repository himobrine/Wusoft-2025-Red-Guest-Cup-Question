from secret import flag

key = 0x1A
def encrypt(text: str) -> str:
    result = []
    for char in text:
        ascii_val = ord(char)
        if 33 <= ascii_val <= 126:
            result.append(chr(33 + ((ascii_val - 33 + 47) % 94)))
        else:
            result.append(char)
    encrypted_bytes = [ord(c) ^ key for c in result]
    return ''.join(f"{b:02X}" for b in encrypted_bytes)

e = encrypt(flag)
print(e)

"""
52592326272456287C2F2E782F7C7D7829457C78457F2F2E7B72792F7D7C727E7B2F7A782979792F72787F29722C2F54
"""