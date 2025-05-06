# How to Solve
Since Zig is a compiled and low level language, 
you can abuse builtin functions related to pointer 
to call execve syscall. One thing you have to consider 
is that the remote uses Alpine, and Alpine uses BusyBox. 
Therefore, you have to call `execve("/bin/sh", {"/bin/sh", NULL}, NULL)` 
instead of `execve("/bin/sh", NULL, NULL)`.
