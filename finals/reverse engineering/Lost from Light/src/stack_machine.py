#!/usr/bin/env python3

import math
import struct


class StackMachine:
    def __init__(self, address_size=8, mem_size=0x100000):
        self._address_size = address_size
        self._stack: list[int] = []
        self._mem = bytearray(mem_size)

    def const(self, val):
        self._stack.append(val)
        return self

    def plus(self):
        self.__assert_elements(2)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(b + a)
        return self

    def minus(self):
        self.__assert_elements(2)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(b - a)
        return self

    def div(self):
        self.__assert_elements(2)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(b // a)
        return self

    def mod(self):
        self.__assert_elements(2)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(b % a)
        return self

    def mul(self):
        self.__assert_elements(2)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(b * a)
        return self

    def shl(self):
        self.__assert_elements(2)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(b << a)
        return self

    def shr(self):
        self.__assert_elements(2)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(b >> a)
        return self

    def xor(self):
        self.__assert_elements(2)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(b ^ a)
        return self

    def neg(self):
        self.__assert_elements(1)
        self._stack.append(-self._stack.pop())
        return self

    def abs(self):
        self.__assert_elements(1)
        self._stack.append(abs(self._stack.pop()))
        return self

    def bnot(self):
        self.__assert_elements(1)
        self._stack.append(~self._stack.pop())
        return self

    def band(self):
        self.__assert_elements(2)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(b & a)
        return self

    def bor(self):
        self.__assert_elements(2)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(b | a)
        return self

    def eq(self):
        self.__assert_elements(2)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(b == a)
        return self

    def neq(self):
        self.__assert_elements(2)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.append(b != a)
        return self

    def dup(self):
        self.__assert_elements(1)
        self._stack.append(self._stack[-1])
        return self

    def drop(self):
        self.__assert_elements(1)
        self._stack.pop()
        return self

    def pick(self, index):
        if index >= len(self._stack):
            raise ValueError("index out of bound")
        self._stack.append(self._stack[-1 - index])
        return self

    def over(self):
        self.__assert_elements(2)
        self._stack.append(self._stack[-2])
        return self

    def swap(self):
        self.__assert_elements(2)
        a = self._stack.pop()
        b = self._stack.pop()
        self._stack.extend([a, b])
        return self

    def rot(self):
        self.__assert_elements(3)
        a = self._stack.pop()
        b = self._stack.pop()
        c = self._stack.pop()
        self._stack.extend([a, c, b])
        return self

    def deref(self):
        addr = self._stack.pop()
        if 0 <= addr < len(self._mem):
            vb = self._mem[addr : addr + self._address_size]
            self._stack.append(struct.unpack("<Q", vb)[0])
            return self
        else:
            max = f"{len(self._mem):x}"
            min = "0" * len(max)
            raise ValueError(f"address out of bound (0x{min}-0x{max})")

    def deref_size(self, size):
        if size not in (1, 2, 4, 8):
            raise ValueError("size must be one of (1, 2, 4, 8)")
        addr = self._stack.pop()
        if not (0 <= addr < len(self._mem)):
            max = f"{len(self._mem):x}"
            min = "0" * len(max)
            raise ValueError(f"address out of bound (0x{min}-0x{max})")
        vb = self._mem[addr : addr + size]
        if size == 1:
            self._stack.append(struct.unpack("<B", vb)[0])
        elif size == 2:
            self._stack.append(struct.unpack("<H", vb)[0])
        elif size == 4:
            self._stack.append(struct.unpack("<I", vb)[0])
        elif size == 8:
            self._stack.append(struct.unpack("<Q", vb)[0])
        return self

    def store(self, address: int, value: bytes | bytearray):
        self._mem[address : address + len(value)] = value

    def __assert_elements(self, n):
        if len(self._stack) < n:
            raise RuntimeError(f"stack must have at least {n} elements")

    def debug(self):
        print(self._stack[::-1])
        return self


if __name__ == "__main__":
    # StackMachine().const(1000).const(29).const(17).dup().debug()
    # StackMachine().const(1000).const(29).const(17).drop().debug()
    # StackMachine().const(1000).const(29).const(17).pick(2).debug()
    # StackMachine().const(1000).const(29).const(17).over().debug()
    # StackMachine().const(1000).const(29).const(17).swap().debug()
    # StackMachine().const(1000).const(29).const(17).debug().rot().debug()

    def perform_round(machine: StackMachine, delta=0x9E3779B9):
        # initial state: [sum, v1, v0, k3, k2, k1, k0, ...]
        # end state: [new_sum, new_v1, new_v0, k3, k2, k1, k0, ...]
        (
            machine.const(delta)  # [delta, sum, v1, v0, k3, k2, k1, k0]
            .plus()  # [new_sum, v1, v0, k3, k2, k1, k0]
            .const(0xFFFFFFFF)
            .band()
            .rot()  # [v1, v0, new_sum, k3, k2, k1, k0]
            .over()  # [v0, v1, v0, new_sum, k3, k2, k1, k0]
            .over()  # [v1, v0, v1, v0, new_sum, k3, k2, k1, k0]
            .const(4)
            .shl()  # [v1<<4, v0, v1, v0, new_sum, k3, k2, k1, k0]
            .pick(8)  # [k0, v1<<4, v0, v1, v0, new_sum, k3, k2, k1, k0]
            .plus()  # [k0+(v1<<4), v0, v1, v0, new_sum, k3, k2, k1, k0]
            .pick(2)  # [v1, k0+(v1<<4), v0, v1, v0, new_sum, k3, k2, k1, k0]
            .pick(5)  # [new_sum, v1, k0+(v1<<4), v0, v1, v0, new_sum, k3, k2, k1, k0]
            .plus()  # [v1+new_sum, k0+(v1<<4), v0, v1, v0, new_sum, k3, k2, k1, k0]
            .pick(3)  # [v1, v1+new_sum, k0+(v1<<4), v0, v1, v0, new_sum, k3, k2, k1, k0]
            .const(5)
            .shr()  # [v1>>5, v1+new_sum, k0+(v1<<4), v0, v1, v0, new_sum, k3, k2, k1, k0]
            .pick(9)
            .plus()  # [k1+(v1>>5), v1+new_sum, k0+(v1<<4), v0, v1, v0, new_sum, k3, k2, k1, k0]
            .xor()
            .xor()  # [k1+(v1>>5)^v1+new_sum^k0+(v1<<4), v0, v1, v0, new_sum, k3, k2, k1, k0]
            .plus()  # [new_v0, v1, v0, new_sum, k3, k2, k1, k0]
            .const(0xFFFFFFFF)
            .band()
            .rot()  # [v1, v0, new_v0, new_sum, k3, k2, k1, k0]
            .rot()  # [v0, new_v0, v1, new_sum, k3, k2, k1, k0]
            .drop()  # [new_v0, v1, new_sum, k3, k2, k1, k0]
            .swap()  # [v1, new_v0, new_sum, k3, k2, k1, k0]
            .over()  # [new_v0, v1, new_v0, new_sum, k3, k2, k1, k0]
            .const(4)
            .shl()  # [new_v0<<4, v1, new_v0, new_sum, k3, k2, k1, k0]
            .pick(5)  # [k2, new_v0<<4, v1, new_v0, new_sum, k3, k2, k1, k0]
            .plus()  # [k2+(new_v0<<4), v1, new_v0, new_sum, k3, k2, k1, k0]
            .pick(2)  # [new_v0, k2+(new_v0<<4), v1, new_v0, new_sum, k3, k2, k1, k0]
            .pick(4)  # [new_sum, new_v0, k2+(new_v0<<4), v1, new_v0, new_sum, k3, k2, k1, k0]
            .plus()  # [new_sum+new_v0, k2+(new_v0<<4), v1, new_v0, new_sum, k3, k2, k1, k0]
            .pick(
                3
            )  # [new_v0, new_sum+new_v0, k2+(new_v0<<4), v1, new_v0, new_sum, k3, k2, k1, k0]
            .const(5)
            .shr()  # [new_v0>>5, new_sum+new_v0, k2+(new_v0<<4), v1, new_v0, new_sum, k3, k2, k1, k0]
            .pick(
                6
            )  # [k3, new_v0>>5, new_sum+new_v0, k2+(new_v0<<4), v1, new_v0, new_sum, k3, k2, k1, k0]
            .plus()  # [k3+(new_v0>>5), new_sum+new_v0, k2+(new_v0<<4), v1, new_v0, new_sum, k3, k2, k1, k0]
            .xor()
            .xor()  # [k3+(new_v0>>5)^new_sum+new_v0^k2+(new_v0<<4), v1, new_v0, new_sum, k3, k2, k1, k0]
            .plus()  # [new_v1, new_v0, new_sum, k3, k2, k1, k0]
            .const(0xFFFFFFFF)
            .band()
            .rot()  # [new_v0, new_sum, new_v1, k3, k2, k1, k0]
            .rot()  # [new_sum, new_v1, new_v0, k3, k2, k1, k0]
        )

    def tea_encrypt_block(
        machine: StackMachine, block_addr: int, key_addr: int, delta=0x9E3779B9, rounds=32
    ):
        (
            machine.const(key_addr)
            .deref_size(4)
            .const(key_addr + 4)
            .deref_size(4)
            .const(key_addr + 8)
            .deref_size(4)
            .const(key_addr + 12)
            .deref_size(4)
            .const(block_addr)
            .deref_size(4)
            .const(block_addr + 4)
            .deref_size(4)
            .const(0)
        )
        # state: [sum, v1, v0, k3, k2, k1, k0, ...]
        for _ in range(rounds):
            perform_round(machine, delta=delta)
        # state: [new_sum, new_v1, new_v0, k3, k2, k1, k0, ...]
        (
            machine.drop()  # [new_v1, new_v0, k3, k2, k1, k0]
            .rot()  # [new_v0, k3, new_v1, k2 ,k1, k0]
            .rot()  # [k3, new_v1, new_v0, k2 ,k1, k0]
            .drop()  # [new_v1, new_v0, k2 ,k1, k0]
            .rot()  # [new_v0, k2, new_v1, k1, k0]
            .rot()  # [k2, new_v1, new_v0, k1, k0]
            .drop()  # [new_v1, new_v0, k1, k0]
            .rot()  # [new_v0, k1, new_v1, k0]
            .rot()  # [k1, new_v1, new_v0, k0]
            .drop()  # [new_v1, new_v0, k0]
            .rot()  # [new_v0, k0, new_v1]
            .rot()  # [k0, new_v1, new_v0]
            .drop()  # [new_v1, new_v0]
        )

    def tea_encrypt(
        plaintext: bytes | bytearray, key: bytes | bytearray, delta=0x9E3779B9, rounds=32
    ):
        machine = StackMachine()
        machine.store(0, key[:0x10])
        machine.store(0x10, plaintext)
        block_size = 8
        num_blocks = math.ceil(len(plaintext) / block_size)
        for i in range(num_blocks):
            tea_encrypt_block(machine, 0x10 + i * block_size, 0, delta=delta, rounds=rounds)
        return machine

    machine = tea_encrypt(
        b"ARKAV{this_chall_is_as_treacherous_as_lost_from_light!!}",
        bytes.fromhex("dc9e3ac003ca259f20f6a5ad6ecfbce8"),
        delta=0x13371337,
        rounds=8,
    )
    machine.debug()
    (
        machine.const(0x69D6E2E0)
        .eq()
        .swap()
        .const(0xD44D2E26)
        .eq()
        .band()
        .swap()
        .const(0x1B0E2315)
        .eq()
        .band()
        .swap()
        .const(0x72DA7209)
        .eq()
        .band()
        .swap()
        .const(0xD5E2C222)
        .eq()
        .band()
        .swap()
        .const(0x5791AC4C)
        .eq()
        .band()
        .swap()
        .const(0xCF35086B)
        .eq()
        .band()
        .swap()
        .const(0xABFF26E3)
        .eq()
        .band()
        .swap()
        .const(0x1CB2B476)
        .eq()
        .band()
        .swap()
        .const(0xFF56BFE9)
        .eq()
        .band()
        .swap()
        .const(0x2F89FA84)
        .eq()
        .band()
        .swap()
        .const(0x731262C)
        .eq()
        .band()
        .swap()
        .const(0xDF72C75)
        .eq()
        .band()
        .swap()
        .const(0xBE6121B7)
        .eq()
        .band()
    )
    machine.debug()
