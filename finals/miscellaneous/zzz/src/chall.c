#define _GNU_SOURCE

#include <fcntl.h>
#include <grp.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/resource.h>
#include <sys/stat.h>
#include <sys/wait.h>
#include <unistd.h>

extern char **environ;

#define MAX_SOURCE_SIZE (5 * 1024) // 5KB
#define FORBIDDEN_COUNT 5
const char *FORBIDDEN[FORBIDDEN_COUNT] = {"@import", "@cInclude", "@cImport", "@embedFile", "asm"};

void set_limits()
{
    struct rlimit limit;
    limit.rlim_cur = 3;
    limit.rlim_max = 3;
    if (setrlimit(RLIMIT_CPU, &limit) < 0)
    {
        perror("setrlimit CPU");
    }

    limit.rlim_cur = 10 * 1024 * 1024;
    limit.rlim_max = 10 * 1024 * 1024;
    if (setrlimit(RLIMIT_AS, &limit) < 0)
    {
        perror("setrlimit AS");
    }
}

const char *contains_forbidden(const char *source)
{
    for (int i = 0; i < FORBIDDEN_COUNT; i++)
    {
        if (strstr(source, FORBIDDEN[i]) != NULL)
            return FORBIDDEN[i];
    }
    return NULL;
}

int main()
{
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);

    char source[MAX_SOURCE_SIZE] = {0};
    char line[1024];
    size_t len = 0;

    printf("Enter source code (write EOF to stop):\n");

    while (fgets(line, sizeof(line), stdin))
    {
        if (strcmp(line, "EOF\n") == 0)
            break;
        if (len + strlen(line) >= MAX_SOURCE_SIZE)
        {
            fprintf(stderr, "Your code is too large, what did you even write lol\n");
            return 1;
        }
        strcat(source, line);
        len += strlen(line);
    }

    const char *s = contains_forbidden(source);
    if (s)
    {
        fprintf(stderr, "`%s` is banned, brah\n", s);
        return 1;
    }

    char temp_dir_template[] = "/tmp/chalXXXXXX";
    char *temp_dir = mkdtemp(temp_dir_template);
    if (!temp_dir)
    {
        perror("mkdtemp");
        return 1;
    }
    if (chmod(temp_dir, 0750) < 0)
    {
        perror("chmod");
        return 1;
    }
    char cleanup_cmd[512];
    snprintf(cleanup_cmd, sizeof(cleanup_cmd), "rm -rf %s", temp_dir);

    char src_path[256];
    char bin_path[256];
    snprintf(src_path, sizeof(src_path), "%s/sol.zig", temp_dir);
    snprintf(bin_path, sizeof(bin_path), "%s/sol", temp_dir);

    FILE *fp = fopen(src_path, "w");
    if (!fp)
    {
        perror("fopen");
        return 1;
    }
    fputs(source, fp);
    fclose(fp);

    pid_t compile_pid = fork();
    if (compile_pid == 0)
    {
        chdir(temp_dir);
        printf("Compiling...\n");
        char *compile_cmd[] = {"zig", "build-exe", "-O", "ReleaseSmall", src_path, NULL};
        execvp(compile_cmd[0], compile_cmd);
        perror("execvp");
        exit(1);
    }

    int status;
    waitpid(compile_pid, &status, 0);
    if (!WIFEXITED(status) || WEXITSTATUS(status) != 0)
    {
        fprintf(stderr, "Compilation failed.\n");
        system(cleanup_cmd);
        return 1;
    }

    int fd = open(bin_path, O_RDONLY);
    if (fd < 0)
    {
        perror("open binary");
        return 1;
    }

    system(cleanup_cmd);

    alarm(30);
    set_limits();

    if (setgroups(0, NULL) < 0)
    {
        perror("setgroups");
        return 1;
    }
    if (setregid(65534, 65534) < 0)
    {
        perror("setregid");
        return 1;
    }
    if (setreuid(65534, 65534) < 0)
    {
        perror("setreuid");
        return 1;
    }

    printf("Running...\n");
    char *const args[] = {bin_path, NULL};
    fexecve(fd, args, environ);

    return 0;
}
