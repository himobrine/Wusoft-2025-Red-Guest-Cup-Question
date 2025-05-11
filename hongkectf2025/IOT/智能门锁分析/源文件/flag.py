import os
import hmac
import hashlib

def generate_flag(challenge_id):
    secret_key = os.urandom(32)
    nonce = os.urandom(16)

    # 构造flag内容
    payload = hmac.new(
        secret_key,
        msg=f"{challenge_id}-{nonce}".encode(),
        digestmod=hashlib.sha256
    ).hexdigest()[:40]

    flag = f"wrhklm{{{payload}}}"

    flag_hash = hashlib.sha3_256(flag.encode()).hexdigest()
    return flag, flag_hash

flag, verification_hash = generate_flag("web_001")
print("Flag:", flag)
# print("Verification Hash:", verification_hash)