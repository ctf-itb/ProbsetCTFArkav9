#!/usr/bin/env python3

from pathlib import Path
from shutil import copy
from subprocess import check_output
from tempfile import TemporaryDirectory
from zlib import compress

from mako.template import Template
from pwn import ELF, unpack, xor
from tqdm import trange


def to_c_array(data):
    return ", ".join(f"0x{b:02x}" for b in data)


FLAG = Path("flag.txt").read_bytes().strip()
N_STAGE = (len(FLAG) + 3) // 4

template = Template(filename="chall.c.mako")

with TemporaryDirectory() as tmpdir:
    next_stage = ""
    uncompressed_size = 0
    compressed_size = 0

    src = Path(tmpdir) / f"stage{N_STAGE}.c"
    out = Path(tmpdir) / f"stage{N_STAGE}"

    src.write_text(
        str(
            template.render(
                uncompressed_size=uncompressed_size,
                compressed_size=compressed_size,
                next_stage=next_stage,
                n_stage=N_STAGE,
            )
        )
    )
    check_output(["gcc", "-static", "-w", "-o", out, src, "-lz"])

    for n in trange(N_STAGE, desc="Compiling"):
        i = N_STAGE - n - 1

        elf = ELF(out, False)
        cur_size = unpack(elf.read(elf.sym["compressed_size"], 4), 32)
        total_size = elf.sym["next_stage"] - elf.sym["main"] + cur_size

        pt = elf.read(elf.sym["main"], total_size)
        key = FLAG[i * 4 : (i + 1) * 4].ljust(4, b"\0")

        uncompressed = xor(pt, key)
        uncompressed_size = len(uncompressed)
        compressed = compress(uncompressed)
        compressed_size = len(compressed)
        next_stage = to_c_array(compressed)

        src = Path(tmpdir) / f"stage{i}.c"
        out = Path(tmpdir) / f"stage{i}"

        src.write_text(
            str(
                template.render(
                    uncompressed_size=uncompressed_size,
                    compressed_size=compressed_size,
                    next_stage=next_stage,
                    n_stage=N_STAGE,
                )
            )
        )
        if i > 0:
            check_output(["gcc", "-static", "-w", "-o", out, src, "-lz"])
        else:
            check_output(["gcc", "-static", "-s", "-w", "-o", out, src, "-lz"])

    copy(out, "chall")
