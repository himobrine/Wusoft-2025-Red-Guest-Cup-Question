import os
import base64
import random
from shutil import which

# 0. 检查依赖工具（mksquashfs）
assert which("mksquashfs") is not None, "请先安装 squashfs-tools（Linux: apt-get install squashfs-tools, macOS: brew install squashfs）"

# 1. 定义文件结构
os.makedirs("rootfs/etc", exist_ok=True)

# 2. 生成加密密码（XOR密钥0x37）
real_password = b"5b70573748c5161676b30882bf29a295fdfe6657"
encrypted_pass = bytes([c ^ 0x37 for c in real_password])  # 加密结果: b'\x94\x93\x90\x95\x9D\xBF\xBF\xBF'

# 3. 创建干扰配置文件
fake_configs = [
    # 门锁版本信息
    "LOCK_VERSION=SmartLock Pro V2025.04.24",
    "FIRMWARE_DATE=2025-04-24",
    "HARDWARE_ID=AGS-Q20",

    # 开锁方式配置
    "UNLOCK_METHODS=password|fingerprint|nfc",
    "FINGERPRINT_MAX=10",
    "NFC_ENABLED=10",

    # 报警和安全机制
    "LOW_BATTERY_ALERT=15%",
    "INTRUSION_ALERT_ENABLED=1",
    "STRANGER_TIMEOUT=30s",

    # 系统调试信息
    "DEBUG_MODE=0",
    "LOG_LEVEL=info",
    "SERIAL_NUMBER=ABCD-1234-EF56",

    # 虚假密码字段
    "BACKUP_PASS=ac94718d9774c6bc37e337e4bd45b226abb8360e",
    "DEFAULT_PIN=030598",
    "ENCRYPTED_TEST=AQIDBAUGBwg=",

    # 真正的密码配置（藏在中间）
    f"ENCRYPTED_PASS={base64.b64encode(encrypted_pass).decode()}",# 关键行

    # 兼容性信息
    "BLE_SUPPORT=1",
    "WIFI_COMPATIBLE=2.4GHz/5GHz",
    "ZIGBEE_VERSION=5.0",

    # 随机填充数据
    f"RANDOM_DATA={os.urandom(8).hex()}"
]
random.shuffle(fake_configs)  # 打乱顺序

with open("rootfs/etc/config", "w") as f:
    f.write("\n".join(fake_configs))

# 4. 生成其他干扰文件
with open("rootfs/README.txt", "w") as f:
    f.write("This is a firmware for SmartLock Pro\nDO NOT MODIFY!")

# 5. 打包为squashfs文件系统（关键步骤）
os.system("mksquashfs rootfs rootfs.squashfs -noappend")

# 6. 构造最终固件
with open("doorlock.bin", "wb") as f:
    # 固件头
    f.write(b"SMARTLOCK_FW\x00" + b"\x00"*0x200)
    
    # 文件系统
    assert os.path.exists("rootfs.squashfs"), "squashfs生成失败！"
    f.write(open("rootfs.squashfs", "rb").read())
    
    # 在文件末尾隐藏XOR密钥提示
    f.write(b"\x37\x37\x37\x37\x37\x37\x37\x37")  # 密钥0x37
    f.write(b"XOR_KEY_HINT=END_OF_FILE")          # 提示

print("[+] 固件生成成功: doorlock.bin")