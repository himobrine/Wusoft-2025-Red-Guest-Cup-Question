#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>

void init() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void vuln() {
    char buf[100];
    printf("Input: ");
    read(0,buf,0x20);
    (*(void (*)())buf)();
}

int main() {
    init();
    vuln();
    return 0;
}

