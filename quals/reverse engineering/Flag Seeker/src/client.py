#!/usr/bin/env python3
import os
import select
import signal
import socket
import sys
import termios
import time
import tty

# Save original terminal settings so we can restore them later.
orig_settings = termios.tcgetattr(sys.stdin.fileno())


def restore_terminal():
    termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, orig_settings)


def get_terminal_size():
    """Get current terminal size (rows, columns)."""
    try:
        size = os.get_terminal_size(sys.stdout.fileno())
        return size.lines, size.columns
    except OSError:
        return 24, 80


def sigwinch_handler(signum, frame):
    """
    Handle terminal resize (SIGWINCH).
    Obtain new terminal dimensions and send an escape sequence to the server.
    The sequence is formatted as: ESC [8;{rows};{cols}
    (matching the challenge's handling, which expects to split on ';')
    """
    rows, cols = get_terminal_size()
    # Construct the resize sequence. Note: no trailing "t" so that when the server splits
    # the sequence (e.g. b"\x1b[8;80;200"), int conversion works.
    resize_seq = f"\x1b[8;{rows};{cols}t"
    try:
        client_socket.send(resize_seq.encode())
    except Exception:
        pass


def sigint_handler(signum, frame):
    restore_terminal()
    sys.exit(0)


def main():
    global client_socket
    # Register signal handlers.
    signal.signal(signal.SIGWINCH, sigwinch_handler)
    signal.signal(signal.SIGINT, sigint_handler)

    # Put terminal into raw mode.
    tty.setraw(sys.stdin.fileno())

    # Connect to the server on port 1337.
    host = "20.195.43.216"
    port = 8700
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
    except Exception as e:
        restore_terminal()
        print("Failed to connect:", e)
        sys.exit(1)
    client_socket.setblocking(False)

    time.sleep(0.2)
    signal.raise_signal(signal.SIGWINCH)

    try:
        while True:
            # Wait for input from either stdin or the server.
            rlist, _, _ = select.select([sys.stdin, client_socket], [], [])
            for ready in rlist:
                if ready == sys.stdin:
                    # Read raw bytes from stdin.
                    data = os.read(sys.stdin.fileno(), 1024)
                    if not data:
                        continue
                    # Relay the data to the server.
                    client_socket.send(data)
                elif ready == client_socket:
                    try:
                        data = client_socket.recv(4096)
                        if not data:
                            # Connection closed by server.
                            restore_terminal()
                            sys.exit(0)
                        # Write the server’s response to stdout.
                        os.write(sys.stdout.fileno(), data)
                    except BlockingIOError:
                        continue
    except Exception as e:
        restore_terminal()
        print("Error:", e)
    finally:
        restore_terminal()
        client_socket.close()


if __name__ == "__main__":
    main()
