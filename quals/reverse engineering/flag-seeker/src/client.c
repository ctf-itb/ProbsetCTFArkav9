#define _GNU_SOURCE
#include <arpa/inet.h>
#include <fcntl.h>
#include <libssh2.h>
#include <poll.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <termios.h>
#include <unistd.h>

static struct termios original_termios;
static LIBSSH2_CHANNEL *channel = NULL;

void restore_terminal()
{
    tcsetattr(STDIN_FILENO, TCSANOW, &original_termios);
}

void set_raw_mode()
{
    struct termios raw;
    tcgetattr(STDIN_FILENO, &original_termios);
    atexit(restore_terminal);

    raw = original_termios;
    raw.c_lflag &= ~(ECHO | ICANON | IEXTEN | ISIG);
    raw.c_iflag &= ~(BRKINT | ICRNL | INPCK | ISTRIP | IXON);
    raw.c_cflag |= (CS8);
    raw.c_oflag &= ~(OPOST);
    raw.c_cc[VMIN] = 1;
    raw.c_cc[VTIME] = 0;

    tcsetattr(STDIN_FILENO, TCSANOW, &raw);
}

void resize_terminal(int signo)
{
    if (channel)
    {
        struct winsize ws;
        if (ioctl(STDOUT_FILENO, TIOCGWINSZ, &ws) == 0)
        {
            libssh2_channel_request_pty_size(channel, ws.ws_col, ws.ws_row);
        }
    }
}

void handle_sigsegv(int signo)
{
    (void)signo;
    _exit(1);
}

int main(int argc, char *argv[])
{
    struct sigaction sa;
    sa.sa_handler = handle_sigsegv;
    sigemptyset(&sa.sa_mask);
    sa.sa_flags = 0;
    sigaction(SIGSEGV, &sa, NULL);

    const char *username = "4TAdcJskoyJ9ZVYlYDr5cCsY3ueyNljDAaCxl0slmARpclxRPNle6EG1GUAjsnl9Siy0ktk";
    const char *password = "8niRFzMctZvc9okrQ0cUFecn0bXM6";

    int sock = socket(AF_INET, SOCK_STREAM, 0);
    struct sockaddr_in sin = {.sin_family = AF_INET, .sin_port = htons(8700)};
    inet_pton(AF_INET, "20.195.43.216", &sin.sin_addr);

    if (connect(sock, (struct sockaddr *)&sin, sizeof(sin)) != 0)
    {
        perror("Failed to connect");
        return EXIT_FAILURE;
    }

    LIBSSH2_SESSION *session = libssh2_session_init();
    libssh2_session_handshake(session, sock);
    libssh2_userauth_password(session, username, password);

    if (!libssh2_userauth_authenticated(session))
    {
        fprintf(stderr, "Authentication failed\n");
        return EXIT_FAILURE;
    }

    channel = libssh2_channel_open_session(session);
    struct winsize ws;
    ioctl(STDOUT_FILENO, TIOCGWINSZ, &ws);
    libssh2_channel_request_pty(channel, "xterm");
    libssh2_channel_request_pty_size(channel, ws.ws_col, ws.ws_row);
    libssh2_channel_shell(channel);

    set_raw_mode();
    signal(SIGWINCH, resize_terminal);

    struct pollfd fds[2] = {{STDIN_FILENO, POLLIN, 0}, {sock, POLLIN, 0}};

    char buffer[4096];
    while (1)
    {
        poll(fds, 2, -1);

        if (fds[0].revents & POLLIN)
        {
            int n = read(STDIN_FILENO, buffer, sizeof(buffer));
            if (n > 0)
                libssh2_channel_write(channel, buffer, n);
        }

        if (fds[1].revents & POLLIN)
        {
            int n = libssh2_channel_read(channel, buffer, sizeof(buffer));
            if (n > 0)
                write(STDOUT_FILENO, buffer, n);
        }

        if (libssh2_channel_eof(channel))
            break;
    }

    restore_terminal();
    libssh2_channel_close(channel);
    libssh2_session_disconnect(session, "Bye");
    libssh2_session_free(session);
    close(sock);

    return EXIT_SUCCESS;
}
