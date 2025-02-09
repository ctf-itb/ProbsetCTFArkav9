from sage.all import *
from Crypto.Util.number import getPrime, getRandomNBitInteger
from random import randint
from ast import literal_eval
from cysignals.signals import AlarmInterrupt
import signal

FLAG = open('flag.txt').read().strip()

n = getPrime(128)

R = PolynomialRing(Zmod(n), 'x')
X = R.gens()[0]

fc = [randint(1, 2**64) for _ in range(32)]
f = sum([fc[i]*X**i for i in range(32)])

def main():
    print("Do you know your sage?")
    
    print(f"We have the generator: {f.list()}")
    print(f"And the prime: {n}")
    
    s = input("Give me your constants, a large one please: ")
    arr = literal_eval(s)
    
    if len(arr) < 48:
        raise Exception("Invalid array length")
    
    is_int = all([type(i) == int and int(i) != 0 for i in arr])
    if not is_int:
        raise Exception("Invalid member type")
    
    mod = sum([arr[i]*X**i for i in range(len(arr))])
    print("Welp, good luck!")
    
    for _ in range(24):
        secret = getRandomNBitInteger(100)
        out = power_mod(f, secret, mod)
        print(f"Challenge: {out.list()}")

        guess = int(input("Your guess: "))
        if guess != secret:
            print("Nope!")
            return

    print(f"Here's your flag: {FLAG}")
    
if __name__ == "__main__":
    try:
        signal.alarm(32) 
        main()
    except AlarmInterrupt as e: print("\nToo slow!\n")
    except Exception as e: print(e)