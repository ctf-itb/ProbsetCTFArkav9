FLAG := $(shell cat src/flag.txt)
OUTPUT := dist/dist.zip

.PHONY: all
all: src/chall $(OUTPUT) challenge.yml

src/chall: src/chall.cc
	@echo "[+] Compiling..."
	@cd src
	@g++ -O2 -fstack-protector-strong -fcf-protection=full -Wl,-z,relro,-z,now,-z,noexecstack -o chall chall.cc

$(OUTPUT): src/chall src/chall.cc src/Dockerfile src/docker-compose.yml 
	@echo "[+] Packing..."
	@cd src
	@7z a dist.zip chall chall.cc docker-compose.yml Dockerfile
	@cd ..
	@mkdir -p dist
	@mv src/dist.zip $(OUTPUT)
    

define CHALLENGE
name: "KV"
category: binary exploitation
description: |- 
    Just a simple key-value store with some fancy features because it's 2025

    Author: **msfir**

value: 1000
type: dynamic
extra:
    initial: 1000
    decay: 30
    minimum: 100

connection_info: nc 20.195.43.216 8003

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

