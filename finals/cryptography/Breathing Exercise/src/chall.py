from sage.all import EllipticCurve, GF
from Crypto.Random import random
from bn350 import p, G, N
import json
import signal
import os

FLAG = open('flag.txt', 'r').read()

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
        return int(r) >> 16
    
send = lambda x : print(json.dumps(x))
recv = lambda : json.loads(input())

def main() :
    oxygen = 50
    b2 = random.randint(2**(N - 1), p)
    F = GF(p)
    E2 = EllipticCurve(F, [0, b2])

    print("We're gonna do a breathing exercise okay! When i breathe you breathe!")
    send({"msg" : "Send your Point!", "b" : b2})
    response = recv()

    Q = E2([response['x'], response['y']])

    assert 0 < response['x'] < p and 0 < response['y'] < p
    assert Q.order() == E2.order()

    rand = RNG(random.getrandbits(N), G, Q)

    while 0 < oxygen < 100 :
        volume = rand.next()
        response = recv()
        
        if response['volume'] > volume :
            oxygen -= 10
            send({"msg" : "you're breathing too heavily", "volume" : volume, "oxygen" : oxygen})
        elif response['volume'] < volume :
            oxygen -= 10
            send({"msg" : "you're breathing too lightly", "volume" : volume, "oxygen" : oxygen})
        elif response['volume'] == volume :
            oxygen += 3
            send({"msg" : "Great, do more", "volume" : volume, "oxygen" : oxygen})

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