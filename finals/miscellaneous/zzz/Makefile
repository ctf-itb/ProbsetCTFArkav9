FLAG := $(shell cat src/flag.txt)
OUTPUT := dist/dist.zip

.PHONY: all
all: src/chall $(OUTPUT) challenge.yml

src/chall: src/chall.c
	@echo "[+] Compiling..."
	@cd src
	@gcc -o chall chall.c

$(OUTPUT): src/chall src/chall.c src/Dockerfile src/docker-compose.yml 
	@echo "[+] Packing..."
	@cd src
	@7z a dist.zip chall chall.c docker-compose.yml Dockerfile
	@cd ..
	@mkdir -p dist
	@mv src/dist.zip $@

define CHALLENGE
name: "zzz"
category: miscellaneous
description: |- 
    Diliat-liat kayaknya Zig lagi naik daun nih.
    Momen yang pas buat bikin jail-nya :D

    Author: **msfir**

value: 1000
type: dynamic
extra:
    initial: 1000
    decay: 25
    minimum: 100

connection_info: nc hostname 12000

flags:
    - $(FLAG)

files:
    - $(OUTPUT)

state: hidden
version: "0.1"
endef

export CHALLENGE

.ONESHELL:
challenge.yml: src/flag.txt
	@echo "[+] Generating challenge.yml..."
	@echo "$$CHALLENGE" > challenge.yml

.PHONY: clean
clean:
	@rm -rf $(OUTPUT) src/chall challenge.yml
	@echo "[+] Cleaned build artifacts"

.PHONY: rebuild
rebuild: clean all

