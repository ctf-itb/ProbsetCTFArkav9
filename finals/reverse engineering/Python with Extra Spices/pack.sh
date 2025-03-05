#!/bin/bash

pushd src
mako-render verify.py.mako >verify.py
mako-render chall.py.mako >chall.py
nuitka --onefile chall.py
rm -rf chall.build chall.dist chall.onefile-build chall.py verify.py
popd

mv src/chall.bin dist

cat <<EOF >challenge.yml
name: "Python with Extra Spices"
# This is used to group challenges in the CTFd UI.
# choose one: binary exploitation, reverse engineering, web exploitation, cryptography, forensics, miscellaneous.
category: reverse engineering
description: |- 
    Recently, I learned how to create functions using FunctionType and CodeType 
    as one of the methods to obfuscate my Python code. I thought it was still 
    easy for seasoned reversing players. So, I compiled my code using Nuitka 
    😁. I wonder how hard it is now 🤔?

    Author: **msfir**

# Don't change this
value: 1000
type: dynamic
extra:
    initial: 1000
    decay: 15
    minimum: 100

flags:
    # A static case sensitive flag
    - $(cat src/flag.txt)

# Provide paths to files from the same directory that this file is in
files:
    - dist/chall.bin

# If provided, the field can take one of two values: hidden, visible.
state: hidden

# Specifies what version of the challenge specification was used.
version: "0.1"
EOF
