FLAG := $(shell cat src/flag.txt)
OUTPUT := dist/dist.zip

.PHONY: all
all: $(OUTPUT) src/chall challenge.yml

$(OUTPUT): src/chall.py.mako src/obfuscator.py
	@echo "[+] Building with test flag..."
	@cd src
	@mako-render --var flag="FLAG" --output-file chall.py chall.py.mako
	@python obfuscator.py chall.py chall.py --seed=arkavidia9.0
	@cython --embed --directive language_level=3 -o chall.c chall.py
	@gcc -O0 -ggdb -o chall -I /usr/include/python3.12 chall.c -lpython3.12
	@rm -f chall.py chall.c
	@patchelf --set-rpath . chall
	@7z a dist.zip chall /lib/python3.12/config-3.12-x86_64-linux-gnu/libpython3.12.so
	@7z rn dist.zip libpython3.12.so libpython3.12.so.1.0
	@cd ..
	@rm -rf dist
	@mkdir -p dist
	@mv src/dist.zip $@

src/chall: $(OUTPUT) src/chall.py.mako src/obfuscator.py src/flag.txt
	@echo "[+] Building with real flag..."
	@cd src
	@mako-render --var flag="FLAG: $(FLAG)" --output-file chall.py chall.py.mako
	@python obfuscator.py chall.py chall.py --seed=arkavidia9.0
	@cython --embed --directive language_level=3 -o chall.c chall.py
	@gcc -O0 -ggdb -o chall -I /usr/include/python3.12 chall.c -lpython3.12
	@rm -f chall.py chall.c

define CHALLENGE
name: "Flag Seeker"
category: reverse engineering
description: |- 
    "The only thing that you absolutely have to know is the location of the flag." – Albert Einstein (probably)

    Author: **msfir**

value: 1000
type: dynamic
extra:
    initial: 1000
    decay: 30
    minimum: 100

connection_info: nc 20.195.43.216 8700

flags:
    - $(FLAG)

files:
    - $(OUTPUT)

state: hidden
version: "0.1"
endef

export CHALLENGE

.ONESHELL:
challenge.yml: Makefile src/flag.txt
	@echo "[+] Generating challenge.yml..."
	@echo "$$CHALLENGE" > challenge.yml

.PHONY: clean
clean:
	@rm -rf $(OUTPUT) src/chall challenge.yml
	@echo "[+] Cleaned build artifacts"

.PHONY: rebuild
rebuild: clean all

