#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

struct note {
    char *content;
    size_t size;
};

struct note *notes[10]; // 修改为指针数组

void init() {
    setvbuf(stdin, 0, _IONBF, 0);
    setvbuf(stdout, 0, _IONBF, 0);
    memset(notes, 0, sizeof(notes)); // 初始化指针数组
}

void add_note() {
    int idx;
    size_t size;
    printf("index: ");
    scanf("%d", &idx);
    if (idx < 0 || idx >= 10 || notes[idx]) {
        puts("invalid index!");
        return;
    }
    printf("size: ");
    scanf("%zu", &size);
    if (size > 0x100) {
        puts("too large!");
        return;
    }
    notes[idx] = malloc(sizeof(struct note));
    notes[idx]->content = malloc(size);
    printf("content: ");
    read(0, notes[idx]->content, size);
    notes[idx]->size = size;
}

void delete_note() {
    int idx;
    printf("index: ");
    scanf("%d", &idx);
    if (idx < 0 || idx >= 10 || !notes[idx]) {
        puts("invalid index!");
        return;
    }
    free(notes[idx]->content);
    free(notes[idx]);
}

void edit_note() {
    int idx;
    printf("index: ");
    scanf("%d", &idx);
    if (idx < 0 || idx >= 10 || !notes[idx]) {
        puts("invalid index!");
        return;
    }
    printf("new content: ");
    read(0, notes[idx]->content, notes[idx]->size + 0x10);
}

void show_note() {
    int idx;
    printf("index: ");
    scanf("%d", &idx);
    if (idx < 0 || idx >= 10 || !notes[idx]) {
        puts("invalid index!");
        return;
    }
    printf("Content: %s\n", notes[idx]->content);
}

int main() {
    init();
    while (1) {
        printf("1. add\n2. delete\n3. edit\n4. show\n5. exit\n>");
        int choice;
        scanf("%d", &choice);
        switch (choice) {
            case 1: add_note(); break;
            case 2: delete_note(); break;
            case 3: edit_note(); break;
            case 4: show_note(); break;
            case 5: return 0;
            default: puts("invalid choice!");
        }
    }
    return 0;
}

