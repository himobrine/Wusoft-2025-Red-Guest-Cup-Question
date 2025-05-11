import base64
import hashlib
import random
from datetime import datetime

class ChronoXorCipher:
    def __init__(self, seed_salt="chrono_salt"):
        self.seed_salt = seed_salt.encode()

    def _generate_key(self, target_time):
        time_str = target_time.strftime("%Y-%m-%d %H:%M:%S")
        seed = hashlib.sha256(time_str.encode() + self.seed_salt).digest()
        random.seed(seed)
        return bytes(random.getrandbits(8) for _ in range(256))  # 生成256字节循环密钥

    def encrypt(self, plaintext, target_time):
        key = self._generate_key(target_time)
        encrypted_bytes = bytes([p ^ key[i % len(key)] for i, p in enumerate(plaintext.encode())])
        return base64.b64encode(encrypted_bytes).decode()  # 标准Base64编码

    def decrypt(self, encrypted, target_time):
        key = self._generate_key(target_time)

        # 修复Base64填充
        restored = encrypted.strip()
        missing_padding = len(restored) % 4
        if missing_padding:
            restored += '=' * (4 - missing_padding)

        try:
            decoded = base64.b64decode(restored)
            return bytes([c ^ key[i % len(key)] for i, c in enumerate(decoded)]).decode()
        except (binascii.Error, UnicodeDecodeError) as e:
            raise ValueError("解密失败: 请检查密钥一致性或输入数据完整性") from e


# 使用示例
if __name__ == "__main__":
    cipher = ChronoXorCipher()
    target_time = datetime(1949,10,1,15)

    encrypted = 'dx3Sbk0PQ3MUrC5Q/csYdMrwKDilAalcYfkT8cIGPd4YKrLLWEUXXiidq+XqFMww'
    decrypted = cipher.decrypt(encrypted, target_time)
    print(f"解密结果: {decrypted}")

    corrupted = encrypted.rstrip("=")
    restored = cipher.decrypt(corrupted, target_time)
    print(f"修复后解密: {restored}")

