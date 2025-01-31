from Crypto.Util.number import bytes_to_long, getPrime
from Crypto.Random.random import randint

FLAG = b"ARKAV{EZZZZ_f3rm47_t0_g3t_5t4rt3d_VROOM_VROOM!!!!!!}"

p, q = getPrime(512), getPrime(512)
n = p*q

g, r1, r2 = randint(2, n), randint(2, n), randint(2, n)

g1 = pow(g, r1 * (p - 1), n)
g2 = pow(g, r2 * (q - 1), n)

s1, s2 = randint(2, n), randint(2, n)

m = bytes_to_long(FLAG)
c1 = (m * pow(g1, s1, n)) % n
c2 = (m * pow(g2, s2, n)) % n

print(f"{n = }")
print(f"{g1 = }")
print(f"{g2 = }")
print(f"{c1 = }")
print(f"{c2 = }")