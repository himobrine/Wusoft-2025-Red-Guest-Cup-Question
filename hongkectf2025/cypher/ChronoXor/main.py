import base64
import hashlib
import random
from datetime import datetime
from secret import flag

class ChronoXorCipher:
    def __init__(self, seed_salt="chrono_salt"):
        self.seed_salt = seed_salt.encode()

    def _generate_key(self, target_time):
        time_str = target_time.strftime("%Y-%m-%d %H:%M:%S")
        seed = hashlib.sha256(time_str.encode() + self.seed_salt).digest()
        random.seed(seed)
        return bytes(random.getrandbits(8) for _ in range(256))

    def encrypt(self, plaintext, target_time):
        key = self._generate_key(target_time)
        encrypted_bytes = bytes([p ^ key[i % len(key)] for i, p in enumerate(plaintext.encode())])
        return base64.b64encode(encrypted_bytes).decode()  # 标准Base64编码

if __name__ == "__main__":
    cipher = ChronoXorCipher()
    target_time = datetime(1949,10,1,15)

    encrypted = cipher.encrypt(flag, target_time)
    print(f"加密结果: {encrypted}")

