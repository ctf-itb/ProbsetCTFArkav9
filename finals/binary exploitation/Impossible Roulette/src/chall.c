// /opt/wasi-sdk/bin/clang -o chall chall.c

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef int (*func_ptr)(int, int, int);

int add_fn(int a, int b, int c)
{
    return a + b + c;
}
int mul_fn(int a, int b, int c)
{
    return a * b * c;
}
int xor_fn(int a, int b, int c)
{
    return a ^ b ^ c;
}

int secret(int a, int b, int c)
{
    if (b * c == 0)
    {
        FILE *file = fopen("flag.txt", "r");
        char buf[0x100] = {0};
        fread(buf, 1, 0x100, file);
        printf("Congratulations! Here is your flag: %s\n", buf);
    }
    return a;
}

func_ptr funcs[] = {add_fn, mul_fn, xor_fn, secret};
int round_results[100];

int read_int(const char *prompt)
{
    printf("%s", prompt);
    char buf[24];
    fgets(buf, 18, stdin);
    return atoi(buf);
}

void init()
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
    srand(time(NULL));
}

void play()
{
    for (int i = 0; i < 100; i++)
    {
        func_ptr chosen_func = funcs[rand() % 4];
        int x = chosen_func(rand(), 1 + rand(), 2 + rand()) % 5;
        printf("Round %d\n", i + 1);
        int index = read_int("> ");
        if (index < 100)
        {
            round_results[index] = x;
        }
    }
}

void check()
{
    for (int i = 0; i < 100; i++)
    {
        if (round_results[i] != rand() % 5)
        {
            printf("You lose :(\n");
            exit(0);
        }
    }
    printf("You win :)\n");
}

int main()
{
    init();
    play();
    check();
    return 0;
}
