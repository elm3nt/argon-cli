#include <stdio.h>
#include <string.h>

int main(int argc, char* argv[]) {
    char password[20];
    char secret[9] = "p@$$w0rd";

    printf("Enter password: ");
    scanf("%s", password);

    if (strcmp(secret, password) == 0) {
        printf("Welcome!\n");
    } else {
        printf("Try again!\n");
    }

    return 0;
}
