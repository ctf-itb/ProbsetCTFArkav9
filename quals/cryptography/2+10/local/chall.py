import random
import sys

from tqdm import tqdm

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad as itb

FLAG = b'ARKAV{****************}'

key = random.randbytes(16)
rnd = random.randrange(2**12, 2**13)

def encrypt(key: bytes, pt: bytes) -> bytes:
    pt = pad(pt, AES.block_size)

    iv = random.randbytes(16)
    for i in tqdm(range(len(key)), dynamic_ncols=True, file=sys.stdout):
        # we encrypt this multiple times to make it extra secure!
        for _ in range(key[i] * rnd):
            cipher = AES.new(key, AES.MODE_CBC, iv)
            ct = cipher.encrypt(pt)

    return iv + ct

def decrypt(key: bytes, iv: bytes, ct: bytes) -> bytes:
    for i in tqdm(range(len(key)), dynamic_ncols=True, file=sys.stdout):
        for _ in range(key[i] * rnd):
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = cipher.decrypt(ct)

    return itb(pt, AES.block_size)

enc = encrypt(key, FLAG)

iv = enc[:16]
ct = enc[16:]

print(f'iv = {iv}')
print(f'ct = {ct}')
print(f'rnd = {rnd}')
print(f'leak = {key[:8].hex()}')
