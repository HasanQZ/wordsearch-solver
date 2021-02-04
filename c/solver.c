#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define arrsize 1048

void slice_str(int x, int y, char str[], char output[]) {
    int q = 0;
    for (int i = x; i < y; i++) {
        output[q] = str[i];
        q++;
    }
}

int chunk(char str[], int n, char output[arrsize][arrsize]) {
    int x=0;
    int i;
    for (i = 0; i < (strlen(str) / n) + 1; i++) {
        char z[arrsize];
        slice_str(x, x+n, str, z);
        strcpy(output[i], z);
        printf("%s\n", output[i]);
        x += n;
    }
    return i;
}

void strcoords(char string[], char substr[]) {
    char* s = strstr(string, substr);

    if (!s)
        return;

    int chunkn = strlen(substr);
    char chunks[arrsize][arrsize];
    int x = chunk(string, substr, chunks);


}


int main(void) {
    char x[arrsize][arrsize];
    // chunk("abcdefghijklm", 3, x);
    strcoords("abcdefg", "cde");
}