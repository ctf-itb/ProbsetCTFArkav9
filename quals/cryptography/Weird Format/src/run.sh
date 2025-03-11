#!/bin/sh
socat tcp-l:8555,reuseaddr,fork EXEC:"python3 chall.py"