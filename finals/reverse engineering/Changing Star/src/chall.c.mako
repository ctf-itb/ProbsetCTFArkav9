#define _GNU_SOURCE
#include <link.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/ptrace.h>
#include <sys/user.h>
#include <sys/prctl.h>
#include <sys/wait.h>
#include <unistd.h>
#include <zlib.h>

#define N_STAGE ${n_stage}

const int compressed_size = ${compressed_size};
const int uncompressed_size = ${uncompressed_size};
const unsigned char next_stage[] = { ${next_stage} };

extern void _init;

void print_wrong()
{
    putchar(':');
    putchar('(');
    putchar('\n');
    _exit(1);
}

void print_correct()
{
    putchar(':');
    putchar(')');
    putchar('\n');
}

void handler(int)
{
    print_wrong();
}

void ptrace_read_n_bytes(pid_t pid, void *remote_addr, void *buf, size_t n)
{
    size_t i = 0;
    long word;
    unsigned char *dst = buf;
    uintptr_t src = (uintptr_t)remote_addr;

    while (i < n)
    {
        uintptr_t aligned_addr = src + i - ((src + i) % sizeof(long));
        word = ptrace(PTRACE_PEEKDATA, pid, (void *)aligned_addr, NULL);

        size_t offset = (src + i) % sizeof(long);
        size_t bytes_to_copy = sizeof(long) - offset;
        if (i + bytes_to_copy > n)
        {
            bytes_to_copy = n - i;
        }

        memcpy(dst + i, ((unsigned char *)&word) + offset, bytes_to_copy);
        i += bytes_to_copy;
    }
}

void get_input(void *dst, size_t len) {
    int count = 0;
    char *buf = dst;
    while (count < len)
    {
        int n = read(0, buf+count, len-count);
        if (n > 0)
        {
            count += n;
            if (buf[count - 1] == '\n')
            {
                buf[count - 1] = '\0';
                return;
            }
        } 
        else
        {
            break;
        }
    }
}

__attribute__((section(".main"))) int main()
{
    struct user_regs_struct regs = {0};
    int flag[N_STAGE] = {0};
    int count = -1;

    get_input(flag, sizeof(flag));

loop:
    signal(SIGSEGV, SIG_DFL);
    signal(SIGILL, SIG_DFL);

    count++;
    pid_t child_pid = fork();
    if (child_pid == 0)
    {
        if (uncompressed_size > 0)
        {
            Bytef *buffer = mmap(NULL, uncompressed_size, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
            uLong uncompressed_len = uncompressed_size;
            uncompress(buffer, &uncompressed_len, (Bytef *)next_stage, compressed_size);
            for (int i = 0; i < (uncompressed_size + sizeof(int) - 1) / sizeof(int); i++)
            {
                ((int *)buffer)[i] ^= flag[count];
            }
            mprotect(&_init, (size_t)(&main) - (size_t)&_init + uncompressed_size, PROT_EXEC | PROT_READ | PROT_WRITE);
            memcpy((void *)&main, buffer, uncompressed_size);

            register size_t r11 __asm__("r11") = uncompressed_len;
            register size_t r12 __asm__("r12") = (size_t)buffer;
        }

    next:
        __asm__ volatile("ud2");
        exit(0);
    }
    else
    {
        signal(SIGSEGV, handler);
        signal(SIGILL, handler);

        int status;

        if (ptrace(PTRACE_ATTACH, child_pid, NULL, NULL) < 0)
        {
            kill(child_pid, SIGKILL);
            print_wrong();
        }

        waitpid(child_pid, &status, 0);
        if (!WIFSTOPPED(status) || WSTOPSIG(status) != SIGSTOP)
        {
            print_wrong();
        }

        if (regs.rip == 0)
        {
            ptrace(PTRACE_GETREGS, child_pid, NULL, &regs);
        }

        ptrace(PTRACE_SETREGS, child_pid, NULL, &regs);
        ptrace(PTRACE_CONT, child_pid, NULL, NULL);

        waitpid(child_pid, &status, 0);
        if (WIFSTOPPED(status))
        {
            struct user_regs_struct tmp_regs;
            ptrace(PTRACE_GETREGS, child_pid, NULL, &tmp_regs);

            if (tmp_regs.rip == (unsigned long long)&&next)
            {
                tmp_regs.rip += 2;
                ptrace(PTRACE_SETREGS, child_pid, NULL, &tmp_regs);
                if (count < N_STAGE)
                {
                    size_t main_base = ((size_t)&main) & ~0xfff;
                    size_t rodata_base = ((size_t)&uncompressed_size) & ~0xfff;

                    size_t main_total = main_base - rodata_base;
                    size_t rodata_total = tmp_regs.r11 - main_total + (size_t)&main - main_base;

                    mprotect((void *)main_base, (size_t)&main - main_base + tmp_regs.r11,
                             PROT_READ | PROT_WRITE | PROT_EXEC);
                    ptrace_read_n_bytes(child_pid, (void *)tmp_regs.r12, &main, tmp_regs.r11);
                    mprotect((void *)main_base, main_total, PROT_READ | PROT_EXEC);
                    mprotect((void *)rodata_base, rodata_total, PROT_READ);

                    ptrace(PTRACE_DETACH, child_pid, NULL, NULL);
                    goto loop;
                }
                else
                {
                    print_correct();
                    ptrace(PTRACE_DETACH, child_pid, NULL, NULL);
                }
            }
            else
            {
                ptrace(PTRACE_DETACH, child_pid, NULL, NULL);
                print_wrong();
            }
        }
    }

    return 0;
}
