from sage.all import *
import random

# This is the source code of oLLLama 9.0 music streaming platform
def fill(num, length):
    notes = Integer(num).bits()
    return notes + [0] * (length - len(notes))

with open("song.txt", "rb") as secret:
    song_list = secret.read().strip()

now_playing = song_list[:11]
next_queue = song_list[10:]

song1 = int.from_bytes(now_playing, "big")
song2 = int.from_bytes(next_queue, "big")

albums = 69
artist1 = song1.bit_length()
artist2 = song2.bit_length()
artists = max(artist1, artist2)
assert albums < artists

p = random_prime(2**512)
q = random_prime(2**512)
N = p*q

F = GF(p)
G = GF(q)
x = random_matrix(F, 1, albums)
y = random_matrix(G, 1, albums)

A1 = random_matrix(ZZ, albums, artists, x=0, y=2)
A2 = random_matrix(ZZ, albums, artists, x=0, y=2)

shuffle1 = randint(0, albums-1)
shuffle2 = randint(0, albums-1)
A1[shuffle1] = vector(ZZ, fill(song1, artists))
A2[shuffle2] = vector(ZZ, fill(song2, artists))

h1 = x*A1
h2 = y*A2
queue1 = 9*p**2*q**2 + p*q**2 - 2*p*q
queue2 = 2*p*q + 3*p

with open("output.txt", "w") as f:
    f.write(f"{N}\n")
    f.write(f"{queue1}\n")
    f.write(f"{queue2}\n")
    f.write(f"{list(h1[0])}\n")
    f.write(f"{list(h2[0])}\n")
