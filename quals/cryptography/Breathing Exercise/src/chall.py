from sage.all import EllipticCurve, GF, proof
from Crypto.Random import random
import json
import signal

proof.all(False)

FLAG = open('flag.txt', 'r').read()

N = 224
p = 0xffffffffffffffffffffffffffffffff000000000000000000000001

class RNG:
    def __init__(self, seed, P, Q):
        self.seed = seed
        self.P = P
        self.Q = Q

    def next(self):
        t = self.seed
        s = (t * self.P).x()
        self.seed = s
        r = (s * self.Q).x()

        return (int(r)) >> 16
        
send = lambda x : print(json.dumps(x))
recv = lambda : json.loads(input())

def main() :
    oxygen = 50
    a1 = random.randint(2**(N - 1), p)
    b1 = random.randint(2**(N - 1), p)
    a2 = random.randint(2**(N - 1), p)
    F = GF(p)
    E1 = EllipticCurve(F, [a1, b1])
    
    G = E1.gens()[0]

    print("We're gonna do a breathing exercise okay! When i breathe you breathe!")
    send({"msg" : "Send b2 and a point on E2!", "a1" : a1, "b1" : b1, "a2" : a2, "Gx" : int(G.x()), "Gy" : int(G.y())})
    response = recv()

    b2 = response['b2']
    E2 = EllipticCurve(F, [a2, b2])

    Q = E2([response['x'], response['y']])

    assert 0 < response['x'] < p and 0 < response['y'] < p
    assert Q.order() == E2.order()

    rand = RNG(random.getrandbits(N), G, Q)

    while 0 < oxygen < 100 :
        volume = rand.next()
        response = recv()
        
        if response['volume'] > volume :
            send({"msg" : "you're breathing too heavily", "volume" : volume})
            oxygen -= 10
        elif response['volume'] < volume :
            send({"msg" : "you're breathing too lightly", "volume" : volume})
            oxygen -= 10
        elif response['volume'] == volume :
            send({"msg" : "Great, do more", "volume" : volume})
            oxygen += 3

    if oxygen <= 0 :
        print("You fainted")
        exit(1)
    elif oxygen >= 100 :
        print("That was relaxing right?")
        print(f"You earned this {FLAG}")

if __name__ == "__main__" :
    signal.alarm(60)
    try :
        main()
    except Exception as e :
        print("Whoops, maybe next time")