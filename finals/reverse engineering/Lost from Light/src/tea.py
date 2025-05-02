import struct


def encrypt_block(v, k, delta, rounds):
    v0, v1 = struct.unpack("<2L", v)
    k0, k1, k2, k3 = struct.unpack("<4L", k)
    s = 0
    for _ in range(rounds):
        s = (s + delta) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
    return struct.pack("<2L", v0, v1)


def decrypt_block(v, k, delta, rounds):
    v0, v1 = struct.unpack("<2L", v)
    k0, k1, k2, k3 = struct.unpack("<4L", k)
    s = (delta * rounds) & 0xFFFFFFFF
    for _ in range(rounds):
        v1 = (v1 - (((v0 << 4) + k2) ^ (v0 + s) ^ ((v0 >> 5) + k3))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + k0) ^ (v1 + s) ^ ((v1 >> 5) + k1))) & 0xFFFFFFFF
        s = (s - delta) & 0xFFFFFFFF
    return struct.pack("<2L", v0, v1)


def null_pad(data: bytes, block_size=8) -> bytes:
    if len(data) % block_size == 0:
        return data
    pad_len = block_size - (len(data) % block_size)
    return data + b"\x00" * pad_len


def null_unpad(data: bytes) -> bytes:
    return data.rstrip(b"\x00")


def encrypt(data: bytes, key: bytes, delta=0x9E3779B9, rounds=32) -> bytes:
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes")
    data = null_pad(data)
    result = bytearray()
    for i in range(0, len(data), 8):
        block = data[i : i + 8]
        encrypted = encrypt_block(block, key, delta, rounds)
        result.extend(encrypted)
    return bytes(result)


def decrypt(data: bytes, key: bytes, delta=0x9E3779B9, rounds=32) -> bytes:
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes")
    if len(data) % 8 != 0:
        raise ValueError("Ciphertext must be a multiple of 8 bytes")
    result = bytearray()
    for i in range(0, len(data), 8):
        block = data[i : i + 8]
        decrypted = decrypt_block(block, key, delta, rounds)
        result.extend(decrypted)
    return null_unpad(bytes(result))
