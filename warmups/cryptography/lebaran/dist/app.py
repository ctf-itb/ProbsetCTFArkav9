flag = "ARKAV{REDACTED}"
key = "REDACTED"

assert len(key) == 16

def xor(message: str, key: str) -> bytes:
    key = key * (len(message) // len(key)) + key[: len(message) % len(key)]
    return "".join(chr(ord(a) ^ ord(b)) for a, b in zip(message, key)).encode()


enc_flag = xor(flag, key)
print(f"Here is the encrypted flag: {enc_flag}")

while True:
    inp = input("Enter a message: ")
    res = xor(inp, key)
    if res == enc_flag:
        print("Correct!")
        break
    else:
        print(res)
