#!/usr/bin/env python3

from hashlib import md5
from pathlib import Path
from subprocess import check_output

from mako.template import Template


def to_c_array(data):
    return ",".join(f"0x{b:02x}" for b in data)


FLAG = Path("flag.txt").read_bytes()
assert len(FLAG) == 56, "flag must be 56 characters long"
flag_hash = md5(FLAG).digest()

template = Template(filename="chall.cpp.mako")
dwarfs = check_output(["python3", "gen_dwarf.py"]).decode().strip()

src = Path("chall.cpp")
src.write_text(str(template.render(flag_hash=to_c_array(flag_hash), dwarfs=dwarfs)))

check_output(
    [
        "g++",
        "-mavx2",
        "-masm=intel",
        "-std=c++17",
        "-fstack-protector",
        "-fno-pie",
        "-no-pie",
        "-Wl,-z,relro,-z,now",
        # "-O3",
        "-o",
        "chall",
        src.as_posix(),
    ]
)

src.unlink()
