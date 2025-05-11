import base64

def extract_key_from_bmp(bmp_path):
    with open(bmp_path, 'rb') as f:
        d = bytearray(f.read())

    # 读取BMP文件头信息
    pixel_offset = int.from_bytes(d[10:14], 'little')

    # 提取LSB中的二进制数据（前256位）
    secret_bits = []
    for i in range(pixel_offset, len(d)):
        if len(secret_bits) >= 256:
            break
        secret_bits.append(d[i] & 0x01)  # 取最低位

    # 将二进制位转换为字节
    key_bytes = []
    for i in range(0, 256, 8):
        byte_bits = secret_bits[i:i + 8]
        byte_value = int(''.join(map(str, byte_bits)), 2)
        key_bytes.append(byte_value)

    return bytes(key_bytes)


def decrypt_flag(encrypted_b85_path, key):
    with open(encrypted_b85_path, 'rb') as f:
        encrypted_data = base64.b85decode(f.read())

    # 异或解密
    decrypted = bytes([encrypted_data[i] ^ key[i % len(key)]
                       for i in range(len(encrypted_data))])
    return decrypted.decode()


# 主流程
if __name__ == "__main__":
    # 1. 从secret.bmp提取密钥c
    c = extract_key_from_bmp("secret.bmp")

    # 2. 解密encrypted.b85
    flag = decrypt_flag("encrypted.b85", c)
    print("Flag:", flag)