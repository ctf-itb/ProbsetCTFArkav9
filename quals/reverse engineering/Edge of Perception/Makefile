FLAG := $(shell cat src/flag.txt)

.PHONY: all
all: dist/chall src/chall challenge.yml

dist/chall: src/chall.py.mako src/obfuscator.py
	@echo "[+] Building with test flag..."
	@cd src && \
	mako-render --var flag="Flag" --output-file chall.py chall.py.mako && \
	python obfuscator.py chall.py chall.py && \
	cython --embed --directive language_level=3 -o chall.c chall.py && \
	gcc -O0 -ggdb -o chall -I /usr/include/python3.12 chall.c -lpython3.12 && \
	rm -f chall.py chall.c && \
	cd ..
	@mkdir -p dist
	@mv src/chall $@

src/chall: dist/chall src/chall.py.mako src/obfuscator.py src/flag.txt
	@echo "[+] Building with real flag..."
	@cd src && \
	mako-render --var flag="$(FLAG)" --output-file chall.py chall.py.mako && \
	python obfuscator.py chall.py chall.py && \
	cython --embed --directive language_level=3 -o chall.c chall.py && \
	gcc -O0 -ggdb -o chall -I /usr/include/python3.12 chall.c -lpython3.12 && \
	rm -f chall.py chall.c

define CHALLENGE
name: "Edge of Perception"
category: reverse engineering
description: |- 
	In an age when maps were etched not on parchment but in the whispers of the void, there 
	existed a realm known as the _Endless Expanse_. Legends spoke of a treasure hidden at the 
	edge of perception—a relic so ancient, its name had been worn away by time itself. Many 
	sought it, lured by tales of its power, but none returned with more than fragments of 
	stories.

	You are a seeker, armed with a compass that points not north, but _inward_. The Expanse 
	unfolds around you, a shifting tapestry of horizons that dance to the rhythm of your steps. 
	Beneath your feet, the ground murmurs with forgotten riches—bronze whispers, silver sighs, 
	gold’s hollow laughter. They glitter like false stars, tempting the impatient to kneel and 
	forget their purpose.

	But you are no ordinary hunter. Your eyes see beyond the immediate glow. The Expanse is vast, 
	its borders stretching farther than any mortal could traverse in a lifetime. Yet the relic 
	lies somewhere, waiting for one who understands that the journey is not measured in steps, 
	but in perception.

	Beware the mirage: the horizon bends as you move, always centering, always deceiving. The 
	relic does not hide—it waits, patient and eternal, for the seeker who dares to question the 
	boundaries of the unseen.

	The Expanse is alive. And it is watching.

	_What will you find when the map becomes the maze?_

	Story by deepseek

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
	- dist/chall

state: visible
version: "0.1"
endef

export CHALLENGE

.ONESHELL:
challenge.yml: src/flag.txt
	@echo "[+] Generating challenge.yml..."
	@echo "$$CHALLENGE" > challenge.yml

.PHONY: clean
clean:
	@rm -rf dist/chall challenge.yml
	@echo "[+] Cleaned build artifacts"

.PHONY: rebuild
rebuild: clean all

