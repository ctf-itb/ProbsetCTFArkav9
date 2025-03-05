FLAG := $(shell cat src/flag.txt)
OUTPUT := dist/dist.zip

.PHONY: all
all: $(OUTPUT) challenge.yml

$(OUTPUT): src/wibufication.exs src/flag.txt
	@echo "[+] Compiling..."
	@cd src
	@elixirc wibufication.exs
	@echo "[+] Encoding flag..."
	@elixir -e "Wibufication.main()" $$(cat flag.txt) > flag.txt.enc
	@echo "[+] Packing..."
	@7z a dist.zip Elixir.Wibufication.beam flag.txt.enc
	@rm Elixir.Wibufication.beam flag.txt.enc
	@cd ..
	@mkdir -p dist
	@mv src/dist.zip $@
	

define CHALLENGE
name: "Wibu"
category: reverse engineering
description: |- 
	Katanya di ITB banyak wibunya.

	Author: **msfir**

value: 1000
type: dynamic
extra:
	initial: 1000
	decay: 15
	minimum: 100

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
	@rm -rf $(OUTPUT) challenge.yml
	@echo "[+] Cleaned build artifacts"

.PHONY: rebuild
rebuild: clean all

