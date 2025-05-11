#include <stdio.h>
#include <string.h>

typedef unsigned long ULONG;

/* 初始化函数 */
void rc4_init(unsigned char *s, unsigned char *key, unsigned long Len) {
    int i = 0, j = 0;
    char k[256] = {0};
    unsigned char tmp = 0;
    for (i = 0; i < 256; i++) {
        s[i] = i;
        k[i] = key[i % Len];
    }
    for (i = 0; i < 256; i++) {
        j = (j + s[i] + k[i]) % 256;
        tmp = s[i];
        s[i] = s[j]; // 交换 s[i] 和 s[j]
        s[j] = tmp;
    }
}

/* 加解密 */
void rc4_crypt(unsigned char *s, unsigned char *Data, unsigned long Len) {
    int i = 0, j = 0, t = 0;
    unsigned long k = 0;
    unsigned char tmp;
    for (k = 0; k < Len; k++) {
        i = (i + 1) % 256;
        j = (j + s[i]) % 256;
        tmp = s[i];
        s[i] = s[j]; // 交换 s[x] 和 s[y]
        s[j] = tmp;
        t = (s[i] + s[j]) % 256;
        Data[k] ^= s[t];
    }
}

void print_string_as_hex(const char *str) {
    size_t len = strlen(str);
    size_t i;
    for (i = 0; i < len; i++) {
        // 以十六进制形式输出每个字符，并确保输出两位
        printf("%02x", (unsigned char)str[i]);
        if (i < len - 1) {
            printf(" ");
        }
    }
    printf("\n");
}

int main() {
    unsigned char s[256] = {0}, s2[256] = {0}; // S-box
    char key[256] = {"Boom"}; // 密钥
    char pData[] = {0x53, 0x13, 0xb8, 0xd6, 0xb9, 0xb7, 0x26, 0x99, 0x73, 0x03, 0xa4, 0xf7, 0x49, 0xef, 0x43, 0x18, 0xcf, 0xd7, 0x28, 0xca}; // 密文
    char arr[512] = {0}; // 假设这里存储预期结果，这里初始化为 0
    unsigned long len = sizeof(pData) / sizeof(pData[0]); // 正确计算密文数据长度
    int i;

    printf("请输入flag：");
    fgets(arr, sizeof(arr), stdin);
    // 去除 fgets 读取的换行符
    size_t arr_len = strlen(arr);
    if (arr_len > 0 && arr[arr_len - 1] == '\n') {
        arr[arr_len - 1] = '\0';
    }

    rc4_init(s, (unsigned char *)key, strlen(key)); // 已经完成了初始化
    for (i = 0; i < 256; i++) {
        s2[i] = s[i];
    }
    

   rc4_crypt(s, (unsigned char *)pData, len); // 加密
//  printf("%s",pData);
 	if(strcmp(arr,pData)==0){
		printf("YES");
	}
	else{
		printf("NO");
	}
	getchar(); 


    return 0;
}    
