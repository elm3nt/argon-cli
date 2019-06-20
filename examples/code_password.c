#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char* argv[]) {
    char password[20];
    int activation_code = 2019;
    char secret[9] = "p@$$w0rd";

    if (argc != 2) {
        printf("Usage: code_password <activation code>\n");

        return -1;
    }

    int code = atoi(argv[1]);

    printf("Enter password: ");
    scanf("%s", password);

    if (code == activation_code) {
        if (strcmp(secret, password) == 0) {
            printf("Welcome!\n");
        } else {
            printf("Try again!\n");
        }
    } else {
        printf("Try again!\n");
    }

    return 0;
}
