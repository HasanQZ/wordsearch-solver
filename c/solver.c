#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void strcoords(char string[], char substr[]) {
    char* s = strstr(string, substr);
    printf("%s\n", s);
}


int main(void) {
    strcoords("abcdefghi", "abc");
}