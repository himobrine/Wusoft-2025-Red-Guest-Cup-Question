#include <stdio.h>
#include <stdlib.h>
#include <seccomp.h>
#include <unistd.h>
#include <fcntl.h>

// 初始化沙箱规则
void init_sandbox() {
    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL); // 默认禁止所有系统调用
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(read), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(write), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(open), 0);
    seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit), 0);
    seccomp_load(ctx);
    seccomp_release(ctx);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void vuln() {
    char buf[100];
    printf("Input: ");
    gets(buf); // 触发栈溢出
}

int main() {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    init_sandbox(); // 启用沙箱
    vuln();
    return 0;
}

