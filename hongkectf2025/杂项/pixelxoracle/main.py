import os
import base64
from secret import flag

def b(data, key):
    data_bytes = data.encode() if isinstance(data, str) else data
    key_bytes = key.encode() if isinstance(key, str) else key
    return bytes([data_bytes[i] ^ key_bytes[i % len(key_bytes)]
                for i in range(len(data_bytes))])

def a(image_path, secret_data, output_path):
    with open(image_path, 'rb') as f:
        d = bytearray(f.read())

    pixel_offset = int.from_bytes(d[10:14], 'little')
    width = int.from_bytes(d[18:22], 'little')
    height = int.from_bytes(d[22:26], 'little')

    secret_bits = ''.join(format(b, '08b') for b in secret_data)
    secret_bits += '0' * (8 - (len(secret_bits) % 8))

    bit_index = 0
    for i in range(pixel_offset, len(d)):
        if bit_index >= len(secret_bits):
            break
        d[i] = (d[i] & 0xFE) | int(secret_bits[bit_index])
        bit_index += 1

    with open(output_path, 'wb') as f:
        f.write(d)


def main():
    c = os.urandom(32)
    encrypted = b(flag, c)
    base85_data = base64.b85encode(encrypted)
    with open("encrypted.b85", "wb") as f:
        f.write(base85_data)
    a("no_brain.bmp", c, "secret.bmp")

if __name__ == "__main__":
    main()