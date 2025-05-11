#include <stdio.h>
#include <string.h>

typedef unsigned long ULONG;

/* ��ʼ������ */
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
        s[i] = s[j]; // ���� s[i] �� s[j]
        s[j] = tmp;
    }
}

/* �ӽ��� */
void rc4_crypt(unsigned char *s, unsigned char *Data, unsigned long Len) {
    int i = 0, j = 0, t = 0;
    unsigned long k = 0;
    unsigned char tmp;
    for (k = 0; k < Len; k++) {
        i = (i + 1) % 256;
        j = (j + s[i]) % 256;
        tmp = s[i];
        s[i] = s[j]; // ���� s[x] �� s[y]
        s[j] = tmp;
        t = (s[i] + s[j]) % 256;
        Data[k] ^= s[t];
    }
}

void print_string_as_hex(const char *str) {
    size_t len = strlen(str);
    size_t i;
    for (i = 0; i < len; i++) {
        // ��ʮ��������ʽ���ÿ���ַ�����ȷ�������λ
        printf("%02x", (unsigned char)str[i]);
        if (i < len - 1) {
            printf(" ");
        }
    }
    printf("\n");
}

int main() {
    unsigned char s[256] = {0}, s2[256] = {0}; // S-box
    char key[256] = {"Boom"}; // ��Կ
    char pData[] = {0x53, 0x13, 0xb8, 0xd6, 0xb9, 0xb7, 0x26, 0x99, 0x73, 0x03, 0xa4, 0xf7, 0x49, 0xef, 0x43, 0x18, 0xcf, 0xd7, 0x28, 0xca}; // ����
    char arr[512] = {0}; // ��������洢Ԥ�ڽ���������ʼ��Ϊ 0
    unsigned long len = sizeof(pData) / sizeof(pData[0]); // ��ȷ�����������ݳ���
    int i;

    printf("������flag��");
    fgets(arr, sizeof(arr), stdin);
    // ȥ�� fgets ��ȡ�Ļ��з�
    size_t arr_len = strlen(arr);
    if (arr_len > 0 && arr[arr_len - 1] == '\n') {
        arr[arr_len - 1] = '\0';
    }

    rc4_init(s, (unsigned char *)key, strlen(key)); // �Ѿ�����˳�ʼ��
    for (i = 0; i < 256; i++) {
        s2[i] = s[i];
    }
    

   rc4_crypt(s, (unsigned char *)pData, len); // ����
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
