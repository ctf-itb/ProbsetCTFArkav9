#!/usr/bin/env python3

import io
import math
import struct

DW_OP = {
    "addr": 3,
    "deref": 6,
    "const1u": 8,
    "const1s": 9,
    "const2u": 10,
    "const2s": 11,
    "const4u": 12,
    "const4s": 13,
    "const8u": 14,
    "const8s": 15,
    "constu": 16,
    "consts": 17,
    "dup": 18,
    "drop": 19,
    "over": 20,
    "pick": 21,
    "swap": 22,
    "rot": 23,
    "xderef": 24,
    "abs": 25,
    "and": 26,
    "div": 27,
    "minus": 28,
    "mod": 29,
    "mul": 30,
    "neg": 31,
    "not": 32,
    "or": 33,
    "plus": 34,
    "plus_uconst": 35,
    "shl": 36,
    "shr": 37,
    "shra": 38,
    "xor": 39,
    "bra": 40,
    "eq": 41,
    "ge": 42,
    "gt": 43,
    "le": 44,
    "lt": 45,
    "ne": 46,
    "skip": 47,
    "lit0": 48,
    "lit1": 49,
    "lit2": 50,
    "lit3": 51,
    "lit4": 52,
    "lit5": 53,
    "lit6": 54,
    "lit7": 55,
    "lit8": 56,
    "lit9": 57,
    "lit10": 58,
    "lit11": 59,
    "lit12": 60,
    "lit13": 61,
    "lit14": 62,
    "lit15": 63,
    "lit16": 64,
    "lit17": 65,
    "lit18": 66,
    "lit19": 67,
    "lit20": 68,
    "lit21": 69,
    "lit22": 70,
    "lit23": 71,
    "lit24": 72,
    "lit25": 73,
    "lit26": 74,
    "lit27": 75,
    "lit28": 76,
    "lit29": 77,
    "lit30": 78,
    "lit31": 79,
    "reg0": 80,
    "reg1": 81,
    "reg2": 82,
    "reg3": 83,
    "reg4": 84,
    "reg5": 85,
    "reg6": 86,
    "reg7": 87,
    "reg8": 88,
    "reg9": 89,
    "reg10": 90,
    "reg11": 91,
    "reg12": 92,
    "reg13": 93,
    "reg14": 94,
    "reg15": 95,
    "reg16": 96,
    "reg17": 97,
    "reg18": 98,
    "reg19": 99,
    "reg20": 100,
    "reg21": 101,
    "reg22": 102,
    "reg23": 103,
    "reg24": 104,
    "reg25": 105,
    "reg26": 106,
    "reg27": 107,
    "reg28": 108,
    "reg29": 109,
    "reg30": 110,
    "reg31": 111,
    "breg0": 112,
    "breg1": 113,
    "breg2": 114,
    "breg3": 115,
    "breg4": 116,
    "breg5": 117,
    "breg6": 118,
    "breg7": 119,
    "breg8": 120,
    "breg9": 121,
    "breg10": 122,
    "breg11": 123,
    "breg12": 124,
    "breg13": 125,
    "breg14": 126,
    "breg15": 127,
    "breg16": 128,
    "breg17": 129,
    "breg18": 130,
    "breg19": 131,
    "breg20": 132,
    "breg21": 133,
    "breg22": 134,
    "breg23": 135,
    "breg24": 136,
    "breg25": 137,
    "breg26": 138,
    "breg27": 139,
    "breg28": 140,
    "breg29": 141,
    "breg30": 142,
    "breg31": 143,
    "regx": 144,
    "fbreg": 145,
    "bregx": 146,
    "piece": 147,
    "deref_size": 148,
    "xderef_size": 149,
}


def encode_uleb128(value: int) -> bytes:
    """Encodes an integer as an unsigned LEB128 byte sequence."""
    if value < 0:
        raise ValueError("ULEB128 cannot encode negative numbers.")
    result = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        if value != 0:
            byte |= 0x80
        result.append(byte)
        if value == 0:
            break
    return bytes(result)


def encode_sleb128(value: int) -> bytes:
    """Encodes an integer as a signed LEB128 byte sequence."""
    result = bytearray()
    while True:
        byte = value & 0x7F
        value >>= 7
        more = True
        if (value == 0 and (byte & 0x40) == 0) or (value == -1 and (byte & 0x40) != 0):
            more = False

        if more:
            byte |= 0x80

        result.append(byte)

        if not more:
            break
    return bytes(result)


class DwarfExpressionBuilder:
    """Builds a DWARF expression incrementally."""

    def __init__(self, address_size=8):
        self._buffer = io.BytesIO()
        self.address_size = address_size

    def get_bytes(self) -> bytes:
        """Returns the accumulated bytecode for the expression."""
        return self._buffer.getvalue()

    def _write_op(self, op_name: str):
        """Writes a simple opcode with no operands."""
        if op_name not in DW_OP:
            raise ValueError(f"Unknown DWARF operation: {op_name}")
        self._buffer.write(struct.pack("B", DW_OP[op_name]))

    def lit(self, value: int):
        if 0 <= value <= 31:
            self._write_op(f"lit{value}")
        else:
            self.constu(value)
        return self

    def addr(self, address: int):
        self._write_op("addr")
        pack_format = "<I" if self.address_size == 4 else "<Q"
        self._buffer.write(struct.pack(pack_format, address))
        return self

    def const1u(self, value: int):
        self._write_op("const1u")
        self._buffer.write(struct.pack("<B", value & 0xFF))
        return self

    def const1s(self, value: int):
        self._write_op("const1s")
        self._buffer.write(struct.pack("<b", value))
        return self

    def const2u(self, value: int):
        self._write_op("const2u")
        self._buffer.write(struct.pack("<H", value & 0xFFFF))
        return self

    def const2s(self, value: int):
        self._write_op("const2s")
        self._buffer.write(struct.pack("<h", value))
        return self

    def const4u(self, value: int):
        self._write_op("const4u")
        self._buffer.write(struct.pack("<I", value & 0xFFFFFFFF))
        return self

    def const4s(self, value: int):
        self._write_op("const4s")
        self._buffer.write(struct.pack("<i", value))
        return self

    def const8u(self, value: int):
        self._write_op("const8u")
        self._buffer.write(struct.pack("<Q", value & 0xFFFFFFFFFFFFFFFF))
        return self

    def const8s(self, value: int):
        self._write_op("const8s")
        self._buffer.write(struct.pack("<q", value))
        return self

    def constu(self, value: int):
        self._write_op("constu")
        self._buffer.write(encode_uleb128(value))
        return self

    def consts(self, value: int):
        self._write_op("consts")
        self._buffer.write(encode_sleb128(value))
        return self

    def fbreg(self, offset: int):
        self._write_op("fbreg")
        self._buffer.write(encode_sleb128(offset))
        return self

    def breg(self, reg_num: int, offset: int):
        if 0 <= reg_num <= 31:
            self._buffer.write(struct.pack("B", DW_OP["breg0"] + reg_num))
        else:
            self._write_op("bregx")
            self._buffer.write(encode_uleb128(reg_num))
        self._buffer.write(encode_sleb128(offset))
        return self

    def reg(self, reg_num: int):
        if 0 <= reg_num <= 31:
            self._buffer.write(struct.pack("B", DW_OP["reg0"] + reg_num))
        else:
            self._write_op("regx")
            self._buffer.write(encode_uleb128(reg_num))
        return self

    def deref(self):
        self._write_op("deref")
        return self

    def dup(self):
        self._write_op("dup")
        return self

    def drop(self):
        self._write_op("drop")
        return self

    def over(self):
        self._write_op("over")
        return self

    def swap(self):
        self._write_op("swap")
        return self

    def rot(self):
        self._write_op("rot")
        return self

    def abs(self):
        self._write_op("abs")
        return self

    def band(self):
        self._write_op("and")
        return self

    def div(self):
        self._write_op("div")
        return self

    def minus(self):
        self._write_op("minus")
        return self

    def mod(self):
        self._write_op("mod")
        return self

    def mul(self):
        self._write_op("mul")
        return self

    def neg(self):
        self._write_op("neg")
        return self

    def bnot(self):
        self._write_op("not")
        return self

    def bor(self):
        self._write_op("or")
        return self

    def plus(self):
        self._write_op("plus")
        return self

    def shl(self):
        self._write_op("shl")
        return self

    def shr(self):
        self._write_op("shr")
        return self

    def shra(self):
        self._write_op("shra")
        return self

    def xor(self):
        self._write_op("xor")
        return self

    def eq(self):
        self._write_op("eq")
        return self

    def ge(self):
        self._write_op("ge")
        return self

    def gt(self):
        self._write_op("gt")
        return self

    def le(self):
        self._write_op("le")
        return self

    def lt(self):
        self._write_op("lt")
        return self

    def ne(self):
        self._write_op("ne")
        return self

    def nop(self):
        self._write_op("nop")
        return self

    def push_object_address(self):
        self._write_op("push_object_address")
        return self

    def call_frame_cfa(self):
        self._write_op("call_frame_cfa")
        return self

    def stack_value(self):
        self._write_op("stack_value")
        return self

    def plus_uconst(self, value: int):
        self._write_op("plus_uconst")
        self._buffer.write(encode_uleb128(value))
        return self

    def skip(self, offset: int):
        self._write_op("skip")
        self._buffer.write(struct.pack("<h", offset))
        return self

    def bra(self, offset: int):
        self._write_op("bra")
        self._buffer.write(struct.pack("<h", offset))
        return self

    def piece(self, size: int):
        self._write_op("piece")
        self._buffer.write(encode_uleb128(size))
        return self

    def deref_size(self, size: int):
        self._write_op("deref_size")
        self._buffer.write(struct.pack("<B", size))
        return self

    def pick(self, index: int):
        self._write_op("pick")
        self._buffer.write(struct.pack("<B", index))
        return self


if __name__ == "__main__":
    KEY_ADDR = 0x40D010
    PLAINTEXT_ADDR = 0x40D280
    PLAINTEXT_SIZE = 56
    BLOCK_SIZE = 8
    NUM_BLOCKS = math.ceil(PLAINTEXT_SIZE / BLOCK_SIZE)
    NUM_ROUNDS = 8
    DELTA = 0x13371337

    builder = DwarfExpressionBuilder()

    for i in range(NUM_BLOCKS):
        block_addr = PLAINTEXT_ADDR + i * BLOCK_SIZE
        (
            builder.addr(KEY_ADDR)
            .deref_size(4)
            .addr(KEY_ADDR + 4)
            .deref_size(4)
            .addr(KEY_ADDR + 8)
            .deref_size(4)
            .addr(KEY_ADDR + 12)
            .deref_size(4)
            .addr(block_addr)
            .deref_size(4)
            .addr(block_addr + 4)
            .deref_size(4)
            .lit(0)
        )
        for _ in range(NUM_ROUNDS):
            (
                builder.const4u(DELTA)
                .plus()
                .const4u(0xFFFFFFFF)
                .band()
                .rot()
                .over()
                .over()
                .lit(4)
                .shl()
                .const4u(0xFFFFFFFF)
                .band()
                .pick(8)
                .plus()
                .const4u(0xFFFFFFFF)
                .band()
                .pick(2)
                .pick(5)
                .plus()
                .const4u(0xFFFFFFFF)
                .band()
                .pick(3)
                .lit(5)
                .shr()
                .const4u(0xFFFFFFFF)
                .band()
                .pick(9)
                .plus()
                .const4u(0xFFFFFFFF)
                .band()
                .xor()
                .const4u(0xFFFFFFFF)
                .band()
                .xor()
                .const4u(0xFFFFFFFF)
                .band()
                .plus()
                .const4u(0xFFFFFFFF)
                .band()
                .rot()
                .rot()
                .drop()
                .swap()
                .over()
                .lit(4)
                .shl()
                .const4u(0xFFFFFFFF)
                .band()
                .pick(5)
                .plus()
                .const4u(0xFFFFFFFF)
                .band()
                .pick(2)
                .pick(4)
                .plus()
                .const4u(0xFFFFFFFF)
                .band()
                .pick(3)
                .lit(5)
                .shr()
                .const4u(0xFFFFFFFF)
                .band()
                .pick(6)
                .plus()
                .const4u(0xFFFFFFFF)
                .band()
                .xor()
                .const4u(0xFFFFFFFF)
                .band()
                .xor()
                .const4u(0xFFFFFFFF)
                .band()
                .plus()
                .const4u(0xFFFFFFFF)
                .band()
                .rot()
                .rot()
            )
        builder.drop().rot().rot().drop().rot().rot().drop().rot().rot().drop().rot().rot().drop()
    (
        builder.const4u(0x69D6E2E0)
        .eq()
        .swap()
        .const4u(0xD44D2E26)
        .eq()
        .band()
        .swap()
        .const4u(0x1B0E2315)
        .eq()
        .band()
        .swap()
        .const4u(0x72DA7209)
        .eq()
        .band()
        .swap()
        .const4u(0xD5E2C222)
        .eq()
        .band()
        .swap()
        .const4u(0x5791AC4C)
        .eq()
        .band()
        .swap()
        .const4u(0xCF35086B)
        .eq()
        .band()
        .swap()
        .const4u(0xABFF26E3)
        .eq()
        .band()
        .swap()
        .const4u(0x1CB2B476)
        .eq()
        .band()
        .swap()
        .const4u(0xFF56BFE9)
        .eq()
        .band()
        .swap()
        .const4u(0x2F89FA84)
        .eq()
        .band()
        .swap()
        .const4u(0x731262C)
        .eq()
        .band()
        .swap()
        .const4u(0xDF72C75)
        .eq()
        .band()
        .swap()
        .const4u(0xBE6121B7)
        .eq()
        .band()
        .bra(12)
        .addr(0x4012AF)
        .skip(9)
        .addr(0x401246)
    )
    result = builder.get_bytes()
    print(",".join(map(hex, [*encode_uleb128(len(result)), *result])))
