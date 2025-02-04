use nix::{
    fcntl::{fcntl, FcntlArg, OFlag},
    libc,
    poll::{poll, PollFd, PollFlags, PollTimeout},
    sys::{
        signal,
        termios::{self, ControlFlags, InputFlags, LocalFlags, OutputFlags, SetArg},
    },
    unistd,
};
use std::env;
use std::os::{fd::BorrowedFd, unix::io::AsRawFd};
use std::process;
use std::{
    io::{self, stdin, stdout, Read, Write},
    os::fd::AsFd,
};

struct TermSize {
    width: u32,
    height: u32,
}

static mut CURRENT_SIZE: TermSize = TermSize {
    width: 0,
    height: 0,
};

extern "C" fn handle_sigwinch(_: libc::c_int) {
    unsafe {
        let mut size = libc::winsize {
            ws_row: 0,
            ws_col: 0,
            ws_xpixel: 0,
            ws_ypixel: 0,
        };
        libc::ioctl(stdin().as_raw_fd(), libc::TIOCGWINSZ, &mut size);
        CURRENT_SIZE = TermSize {
            width: size.ws_col as u32,
            height: size.ws_row as u32,
        };
    }
}

fn set_raw_mode<Fd: AsFd>(fd: fn() -> Fd) -> nix::Result<termios::Termios> {
    let original = termios::tcgetattr(fd())?;

    let mut raw = original.clone();
    raw.input_flags -= InputFlags::BRKINT
        | InputFlags::ICRNL
        | InputFlags::INPCK
        | InputFlags::ISTRIP
        | InputFlags::IXON;
    raw.output_flags -= OutputFlags::OPOST;
    raw.control_flags |= ControlFlags::CS8;
    raw.local_flags -=
        LocalFlags::ECHO | LocalFlags::ICANON | LocalFlags::IEXTEN | LocalFlags::ISIG;
    raw.control_chars[termios::SpecialCharacterIndices::VMIN as usize] = 1;
    raw.control_chars[termios::SpecialCharacterIndices::VTIME as usize] = 0;

    termios::tcsetattr(fd(), SetArg::TCSANOW, &raw)?;
    Ok(original)
}

fn get_terminal_size<Fd: AsRawFd>(fd: fn() -> Fd) -> nix::Result<(u32, u32, u32, u32)> {
    let mut size = libc::winsize {
        ws_row: 0,
        ws_col: 0,
        ws_xpixel: 0,
        ws_ypixel: 0,
    };

    unsafe {
        libc::ioctl(fd().as_raw_fd(), libc::TIOCGWINSZ, &mut size);
    }

    Ok((
        size.ws_col as u32,
        size.ws_row as u32,
        size.ws_xpixel as u32,
        size.ws_ypixel as u32,
    ))
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let args: Vec<_> = env::args().collect();
    if args.len() < 3 {
        eprintln!("Usage: {} <host> <port>", args[0]);
        process::exit(1);
    }
    // Set up signal handler
    let sa = signal::SigAction::new(
        signal::SigHandler::Handler(handle_sigwinch),
        signal::SaFlags::SA_RESTART,
        signal::SigSet::empty(),
    );
    unsafe {
        signal::sigaction(signal::Signal::SIGWINCH, &sa)?;
    }

    // SSH connection setup
    let tcp = std::net::TcpStream::connect(format!("{}:{}", args[1], args[2]))?;
    let tcp_fd = tcp.as_raw_fd();
    let mut sess = ssh2::Session::new()?;
    sess.set_tcp_stream(tcp);
    sess.handshake()?;

    sess.userauth_password(
        "4TAdcJskoyJ9ZVYlYDr5cCsY3ueyNljDAaCxl0slmARpclxRPNle6EG1GUAjsnl9Siy0ktk",
        "8niRFzMctZvc9okrQ0cUFecn0bXM6",
    )?;
    if !sess.authenticated() {
        eprintln!("Authentication failed");
        process::exit(1);
    }

    // Create channel
    let mut channel = sess.channel_session()?;
    let (width, height, pxw, pxh) = get_terminal_size(stdin)?;
    channel.request_pty("xterm", None, Some((width, height, pxw, pxh)))?;
    channel.shell()?;

    // Save original terminal settings
    let original_termios = set_raw_mode(stdin)?;
    sess.set_blocking(false);

    // Set non-blocking mode for stdin
    let flags = fcntl(stdin().as_raw_fd(), FcntlArg::F_GETFL)?;
    let new_flags = OFlag::from_bits_truncate(flags) | OFlag::O_NONBLOCK;
    fcntl(stdin().as_raw_fd(), FcntlArg::F_SETFL(new_flags))?;

    // Main I/O loop
    let mut buffer = [0u8; 4096];

    // Setup poll
    let mut fds = [
        PollFd::new(
            unsafe { BorrowedFd::borrow_raw(stdin().as_raw_fd()) },
            PollFlags::POLLIN,
        ),
        PollFd::new(unsafe { BorrowedFd::borrow_raw(tcp_fd) }, PollFlags::POLLIN),
    ];

    'outer: loop {
        // Handle window resize
        unsafe {
            if CURRENT_SIZE.width != 0 || CURRENT_SIZE.height != 0 {
                let _ =
                    channel.request_pty_size(CURRENT_SIZE.width, CURRENT_SIZE.height, None, None);
                CURRENT_SIZE = TermSize {
                    width: 0,
                    height: 0,
                };
            }
        }

        match poll(&mut fds, PollTimeout::NONE) {
            Ok(_) => {}
            Err(nix::Error::EINTR) => continue,
            Err(e) => return Err(e.into()),
        }

        // Handle stdin
        if fds[0]
            .revents()
            .map_or(false, |e| e.contains(PollFlags::POLLIN))
        {
            match unistd::read(stdin().as_raw_fd(), &mut buffer) {
                Ok(0) => break,
                Ok(n) => channel.write_all(&buffer[..n])?,
                Err(nix::Error::EAGAIN) => {}
                Err(e) => return Err(e.into()),
            }
        }

        // Handle channel output
        if fds[1]
            .revents()
            .map_or(false, |e| e.contains(PollFlags::POLLIN))
        {
            loop {
                match channel.read(&mut buffer) {
                    Ok(0) => break 'outer,
                    Ok(n) => {
                        unistd::write(stdout(), &buffer[..n])?;
                    }
                    Err(e) if e.kind() == io::ErrorKind::WouldBlock => break,
                    Err(e) => return Err(e.into()),
                }
            }
        }
    }

    // Cleanup
    termios::tcsetattr(stdin(), SetArg::TCSANOW, &original_termios)?;
    channel.close()?;
    Ok(())
}
