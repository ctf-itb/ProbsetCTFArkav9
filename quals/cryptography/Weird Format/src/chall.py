from Crypto.Util.number import bytes_to_long, getPrime
from Crypto.Random.random import randint
import signal

with open("flag.txt", "r") as f :
    FLAG = f.read().encode()

p, q = getPrime(384), getPrime(384)
n = p*q

g, r1, r2 = randint(2, n), randint(2, n), randint(2, n)
g1 = pow(g, r1 * (p - 1), n)
g2 = pow(g, r2 * (q - 1), n)

def encrypt(m) :
    assert (0 <= m < n)
    s1, s2 = randint(2, n), randint(2, n)
    c1 = (m * pow(g1, s1, n)) % n
    c2 = (m * pow(g2, s2, n)) % n
    return c1, c2

def encrypt_service() :
    m = int(input("Plaintext: "))
    assert (0 <= m < n)
    c1, c2 = encrypt(m)
    print(f"Encrypted: {(c1, c2)}")

options = ["Encrypt", "Decrypt", "Exit"]
def menu() :
    [print(f"{i + 1}. {opt}") for i, opt in enumerate(options)]

def main() :
    print(f"Encrypted Flag: {encrypt(bytes_to_long(FLAG))}")

    while True :
        menu()
        choice = int(input(">> "))
        if choice == 1 :
            encrypt_service()
        elif choice == 2 :
            print("Do it yourself :D")
        elif choice == 3:
            print("Kay Bye")
            exit()
        else :
            raise IndexError()

if __name__ == "__main__" :
    signal.alarm(60)
    try :
        main()
    except :
        print("Uh Oh")
        exit()