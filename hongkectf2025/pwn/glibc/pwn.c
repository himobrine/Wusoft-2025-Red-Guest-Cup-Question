#include <stdio.h>
#include <string.h>

void vuln() {
    char buffer[64];
    printf("Input: ");
    gets(buffer); // 明显栈溢出漏洞
}

int main() {
    setbuf(stdout, NULL);
    setbuf(stdin, NULL);
    puts("Welcome to ret2libc challenge!");
    vuln();
    puts("Bye!");
    return 0;
}
