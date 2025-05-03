FLAG := $(shell cat src/flag.txt)
OUTPUT := dist/chall

.PHONY: all
all: $(OUTPUT) challenge.yml

$(OUTPUT): src/gen_chall.py src/chall.cpp.mako src/gen_dwarf.py src/md5_simd.cpp src/flag.txt
	@echo "[+] Compiling..."
	@cd src
	@python3 gen_chall.py
	@cd ..
	@mkdir -p dist
	@mv src/chall $(OUTPUT)


define CHALLENGE
name: "Lost from Light"
category: reverse engineering
description: |-
	**SPOILER ALERT**

	There was a king who ruled over a dying land. The king was valiant and wise.
	Refusing to embrace despair, he thought of an audacious plan, gathered his
	companions, and braved the endless desert to enter the Tomb of Ariel, where
	the Great River flowed endlessly from the future into the past. Thus, the 
	valiant king became a guide who guarded his people in their nightmares.

    They built a city at the edge of dawn and gathered an army to vanquish that 
	which was defiled. However, in the end, the army was destroyed, the city was 
	lost, and the valiant king himself succumbed to madness.

    Consumed by wrath and resentment, he turned into a mindless beast and roamed 
	the Great River for countless years. Nothing could withstand his hunger and 
	fury... until, one day, the mad king met a treacherous shadow.

    "But what do you even know?" said the shadow. "Do you think you're so special? 
	I know fury, too. I know hunger, too. I know madness, too! Oh... and I've 
	killed plenty of creatures more powerful than me, too. Who are you to dare 
	stare me down, beast?"

    "I am Lost from Light, who was born from the shadows. I am the rightful heir 
	of death and the bastard son of fate. Wherever I go, ruin follows. If you had 
	any sense, you would have run away as soon as you saw me."

    And, true to his word, treacherous Lost from Light battled the mad king, 
	eventually becoming his doom.

    That was how the king who had outlived his land died.


    **NP: read Shadow Slave it's PEAK**

    Author: **msfir**

value: 1000
type: dynamic
extra:
    initial: 1000
    decay: 10
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
challenge.yml: src/flag.txt Makefile
	@echo "[+] Generating challenge.yml..."
	@echo "$$CHALLENGE" > challenge.yml

.PHONY: clean
clean:
	@rm -rf $(OUTPUT) challenge.yml
	@echo "[+] Cleaned build artifacts"

.PHONY: rebuild
rebuild: clean all

