from Crypto.Random import random
from Variety1 import Variety1
from Variety2 import Variety2
from param import p
import signal
import json

with open('flag.txt', 'r') as f :
    FLAG = f.read()

class RNG:
    def __init__(self, seed, P, Q):
        self.seed = seed
        self.P = P
        self.Q = Q

    def next(self):
        t = self.seed
        s = (t * self.P).x
        self.seed = s
        r = (s * self.Q).x
        return (int(r)) >> 12
        
send = lambda x : print(json.dumps(x))
recv = lambda : json.loads(input())

def main() :
    aura = 5000
    a2 = random.randint(1, p)
    b2 = random.randint(1, p)
    a1 = random.randint(1, p)

    E2 = Variety2(a2, b2)
    G2 = E2.random_element()

    print("Mr. can you see the future?")
    send({"msg" : "Send b1 and a point on E1!", "a1" : a1, "a2" : a2, "b2" : b2, "Gx" : G2.x, "Gy" : G2.y})
    response = recv()

    b1 = response['b1']
    x1, y1 = response['x'], response['y']

    E1 = Variety1(a1, b1)
    G1 = E1(x1, y1)
    
    if (195306067165045895827288868805553560 * G1).list() == [1, 0] :
        print("I don't like that point 🤔")
        exit()

    rand = RNG(random.randint(1, p), G1, G2)

    while 0 < aura < 12000 :
        future = rand.next()
        response = recv()
        
        if response['future'] != future :
            send({"msg" : "Sir, that is not my future, you are a scam artist", "future" : future})
            aura -= 1000
        elif response['future'] == future :
            send({"msg" : "Great, do more", "future" : future})
            aura += 400

    if aura <= 0 :
        print("You fainted")
        exit(1)
    elif aura >= 12000 :
        print("You are a certified dukun!")
        print(f"You earned this {FLAG}")

if __name__ == "__main__" :
    signal.alarm(30)
    try :
        main()
    except Exception as e :
        print(e)