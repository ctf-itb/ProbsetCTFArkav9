import ctypes
import mmap
import base64

buf = mmap.mmap(-1, mmap.PAGESIZE, prot=mmap.PROT_READ | mmap.PROT_WRITE | mmap.PROT_EXEC)

ftype = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)
fpointer = ctypes.c_void_p.from_buffer(buf)
f = ftype(ctypes.addressof(fpointer))

buf.write(base64.b64decode("UVJWSInwSPfGAQAAAHUESIPAAUmJwEiJ+Egx0kjHwQQAAABI9/FIg/oAdBJIg/oBdBJIg/oCdBVIa/9l6xNIa/8b6w1Iaf+BAAAA6wRIa/8DSQ+v+EiB5/8AAABIifheWlnD"))

flag = input("Input flag here: ").strip().encode()

if bytes(list(map(lambda x : f(x[1], x[0]), list(enumerate(flag))))).hex() == "c1f6c5430aa35fa45753aa87d30c353089fc68111217baefc1c1933177770808f8f8e8e8acac24249c9cc9c97f7f3535ebeb67" :
    print("Correct!")
else :
    print("Wrong!")