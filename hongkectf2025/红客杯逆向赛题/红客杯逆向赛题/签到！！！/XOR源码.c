#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// ���ܺ���������飨������flag���㣩
int arr[] = {
   0x6c, 0x66, 0x6b, 0x6d, 0x71, 0x5d, 0x6f, 0x66, 0x69, 0x65, 0x67, 0x6f, 0x55, 0x7e, 0x65, 0x55, 0x42, 0x65, 0x64, 0x6d, 0x55, 0x61, 0x6f, 0x77  // ����һ��Ԫ��
};

int __cdecl main(int argc, const char **argv, const char **envp)
{
    char Str[44]; // [rsp+20h] [rbp-30h] BYREF
    int i; // [rsp+4Ch] [rbp-4h]

    puts("please input your flag!");
    scanf("%s", Str);
    


    // ��֤ÿ���ַ�
    for (i = 0; i <= 22; ++i)  // ��Ϊ22��ѭ��
    {
        if (arr[i] != (Str[i] ^ 0xA))
        {
            printf("flag error!");
            exit(0);
        }
    }
    
    printf("you are right!");
    return 0;
}
