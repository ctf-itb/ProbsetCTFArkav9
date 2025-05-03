FLAG := $(shell cat src/flag.txt)
OUTPUT := dist/chall

.PHONY: all
all: $(OUTPUT) challenge.yml

$(OUTPUT): src/gen.py src/chall.c.mako src/flag.txt
	@echo "[+] Compiling..."
	@cd src
	@python3 gen.py
	@cd ..
	@mkdir -p dist
	@mv src/chall $(OUTPUT)


define CHALLENGE
name: "Changing Star"
category: reverse engineering
description: |-
    In silent skies where silver weeps,
    A star once woke from ancient sleeps.
    Neither light nor dark her flame confined,
    But both entwined in fate aligned.

    A whisper born from shattered lore,
    She walks where none have walked before.
    The wind forgets the steps she takes,
    Yet echoes bloom in her mistakes.

    Star of Change— she bends the night,
    Unfolding dawn in shadow’s light.
    With every breath, a world remade,
    A blade of truth through lies’ parade.

    Star of Ruin— cold and pure,
    The storm she brings is fate's own cure.
    To break, to burn, to start anew,
    The seed must die before it grew.

    No crown she wears, no throne she seeks,
    Her voice is silence when it speaks.
    And in that hush, the heavens fall—
    For she, the star, will end it all.

    Or birth the dawn from ash and flame...
    No one remains, yet all is named.

    **NP: read Shadow Slave, it's PEAK**

    Author: **msfir**

value: 1000
type: dynamic
extra:
    initial: 1000
    decay: 9
    minimum: 100

flags:
    - $(FLAG)

files:
    - $(OUTPUT)

state: visible
version: "0.1"
endef

export CHALLENGE

.ONESHELL:
challenge.yml: src/flag.txt Makefile
	@echo "[+] Generating challenge.yml..."
	@echo "$$CHALLENGE" > challenge.yml

.PHONY: clean
clean:
	@rm -rf $(OUTPUT) challenge.yml
	@echo "[+] Cleaned build artifacts"

.PHONY: rebuild
rebuild: clean all

