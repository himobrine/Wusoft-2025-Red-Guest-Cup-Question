import base64

encrypted = base64.b64decode("AlUABwIABAADD1QCBgEGAQABVQQHDw8FVVEFDlYFDgJRU1FSAQECAA==")
key = 0x37
plaintext = bytes([c ^ key for c in encrypted])
print("Flag:", f"wrhklm{{{plaintext.decode()}}}")
