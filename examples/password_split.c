#include <stdio.h>
#include <string.h>

#define SECRET "p@ssw0rd"
#define PASSWORD_SIZE 20+1
#define SPLIT_STRING_SIZE 1


void sub_string(char string[], char sub_str[], int position, int length) {
    int i;

    for (i = 0; i < length; sub_str[i] = string[position + i], i++);
    sub_str[i] = '\0';
}


int length(char *string) {
    int i ;

    for (i = 0; string[i] != '\0'; i ++);

    return i;
}


int authenticate(char password[PASSWORD_SIZE]) {
    int i;
    char secret[] = SECRET;
    int secret_length = length(secret);
    int password_length = length(password);
    char secret_split_string[SPLIT_STRING_SIZE + 1];
    char password_split_string[SPLIT_STRING_SIZE + 1];

    if (secret_length != password_length) {
        return 1;
    }

    for (i = 0; i < secret_length; i = i + SPLIT_STRING_SIZE) {
        sub_string(secret, secret_split_string, i, SPLIT_STRING_SIZE);
        sub_string(password, password_split_string, i, SPLIT_STRING_SIZE);

        if (strcmp(secret_split_string, password_split_string) != 0) {
            return 1;
        }
    }

    return 0;
}


int main(int argc, char* argv[]) {
    char password[PASSWORD_SIZE];

    printf("Enter password: ");
    scanf("%s", password);

    if (authenticate(password) == 0) {
        printf("Welcome!\n");
    } else {
        printf("Try again!\n");
    }

    return 0;
}
