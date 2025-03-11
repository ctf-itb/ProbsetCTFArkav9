from pwn import context, asm
import base64
import ctypes
import mmap

context.arch = "AMD64"

codes = asm("""
    push    rcx
    push    rdx
    push    rsi
    mov     rax, rsi
    test    rsi, 1
    jnz     check_mod_4
    add     rax, 1
    check_mod_4:
    mov     r8, rax
    mov     rax, rdi
    xor     rdx, rdx
    mov     rcx, 4
    div     rcx

    cmp     rdx, 0
    je      case_mod_0
    cmp     rdx, 1
    je      case_mod_1
    cmp     rdx, 2
    je      case_mod_2
    imul    rdi, 101
    jmp     multiply_with_i
    case_mod_0:
    imul    rdi, 27
    jmp     multiply_with_i
    case_mod_1:
    imul    rdi, 129
    jmp     multiply_with_i
    case_mod_2:
    imul    rdi, 3
    multiply_with_i:
    imul    rdi, r8
    and     rdi, 0xFF
    mov     rax, rdi
    pop     rsi
    pop     rdx
    pop     rcx
    ret
""")

print(f"Base64 code : {base64.b64encode(codes)}")

buf = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)
buf.write(codes)

ftype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)
fpointer = ctypes.c_void_p.from_buffer(buf)
f = ftype(ctypes.addressof(fpointer))

def process_byte(b, i):

    if (i % 2 == 0) :
        i += 1

    if b % 4 == 0:
        return (b * 27 * i) % 256
    elif b % 4 == 1:
        return (b * 129 * i) % 256
    elif b % 4 == 2:
        return (b * 3 * i) % 256
    else:
        return (b * 101 * i) % 256
    
def reverse_process_byte(y, i):

    if i % 2 == 0:
        i_mod = i + 1
    else:
        i_mod = i
    
    multipliers = [27, 129, 3, 101]
    
    for r in range(4):
        k = multipliers[r]
        multiplier = k * i_mod
        inv = pow(multiplier, -1, 256)
        candidate = (y * inv) % 256
        
        if candidate % 4 == r:
            return candidate

for i in range(256) :
    for j in range(51) :
        assert f(i, j) == process_byte(i, j)
    
FLAG = b"ARKAV{its_just_python_riiiiggghhhhhhtttttt????????}"

expected_output = bytearray()
for i, c in enumerate(FLAG) :
    expected_output.append(process_byte(c, i))

print(expected_output.hex())

check_input = bytearray()
for i, c in enumerate(expected_output) :
    check_input.append(reverse_process_byte(c, i))

assert bytes(check_input) == FLAG