CC = gcc

all: code password password_split code_password

code: code.c
	${CC} code.c -o code

password: password.c
	${CC} password.c -o password

password_split: password_split.c
	${CC} password_split.c -o password_split

code_password: code_password.c
	${CC} code_password.c -o code_password

clean:
	rm code password code_password
