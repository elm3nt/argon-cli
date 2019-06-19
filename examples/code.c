#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
    int activation_code = 2019;

    if (argc != 2) {
        printf("Usage: code_password <activation code>\n");

        return -1;
    }

    int code = atoi(argv[1]);

    if (code == activation_code) {
        printf("Welcome!\n");
    } else {
        printf("Try again!\n");
    }

    return 0;
}