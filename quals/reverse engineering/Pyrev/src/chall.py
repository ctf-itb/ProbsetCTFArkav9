lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII, llllllllllllIll, llllllllllllIlI = map, bytes, input, enumerate, print, list

from mmap import PAGESIZE as IlIIlIIlllIIll, PROT_EXEC as lIIllIlIIIIlll, PROT_WRITE as lIIllIIIIIIIII, mmap as lllIIlIIIlIlll, PROT_READ as llllIllIIlIllI
from ctypes import c_int as llIIIIIIlIIlIl, CFUNCTYPE as lIlIlllIIIlIII, addressof as lIIllIlIIIIIlI
from ctypes import c_void_p as IIIlIIlllIlIll
from base64 import b64decode as lIllIIlIlIIIIl
IlllIlIIlIllllIIlI = lllIIlIIIlIlll(-1, IlIIlIIlllIIll, prot=llllIllIIlIllI | lIIllIIIIIIIII | lIIllIlIIIIlll)
lIIllllIllIIlllIll = lIlIlllIIIlIII(llIIIIIIlIIlIl, llIIIIIIlIIlIl)
lllllIllIIlIIIIIlI = IIIlIIlllIlIll.from_buffer(IlllIlIIlIllllIIlI)
llIllllIlllllIIIIl = lIIllllIllIIlllIll(lIIllIlIIIIIlI(lllllIllIIlIIIIIlI))
IlllIlIIlIllllIIlI.write(lIllIIlIlIIIIl('UVJWSInwSPfGAQAAAHUESIPAAUmJwEiJ+Egx0kjHwQQAAABI9/FIg/oAdBJIg/oBdBJIg/oCdBVIa/9l6xNIa/8b6w1Iaf+BAAAA6wRIa/8DSQ+v+EiB5/8AAABIifheWlnD'))
IlllIllIllIllIllIl = lllllllllllllIl('Input flag here: ').strip().encode()
if llllllllllllllI(llllllllllllIlI(lllllllllllllll(lambda lIlIlIIlIIIlIlIIlI: llIllllIlllllIIIIl(lIlIlIIlIIIlIlIIlI[1], lIlIlIIlIIIlIlIIlI[0]), llllllllllllIlI(lllllllllllllII(IlllIllIllIllIllIl))))).hex() == 'c1f6c5430aa35fa45753aa87d30c353089fc68111217baefc1c1933177770808f8f8e8e8acac24249c9cc9c97f7f3535ebeb67':
    llllllllllllIll('Correct!')
else:
    llllllllllllIll('Wrong!')