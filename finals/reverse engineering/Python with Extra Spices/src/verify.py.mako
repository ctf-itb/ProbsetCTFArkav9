<%!
    import math
    with open("flag.txt") as f:
        flag = f.read().strip()
    chunks = []
    for i in range(math.ceil(len(flag)/4)):
        n = 0
        for j, c in enumerate(flag[i*4:(i+1)*4]):
            n += ord(c) << (j * 8)
        chunks.append(n)
%>
def verify(flag):
    chunks = []
    for i in range(${len(chunks)}):
        n = 0
        for j, c in enumerate(flag[i*4:(i+1)*4]):
            n += ord(c) << (j * 8)
        chunks.append(n)
    return all([
        len(flag) == ${len(flag)},
    %for i in range(1, len(chunks)):
        chunks[${i - 1}] * chunks[${i}] % 2**32 == ${chunks[i - 1] * chunks[i] % 2**32},
    %endfor
    ])
