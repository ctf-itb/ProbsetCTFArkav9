#!/bin/sh
socat tcp-l:8101,reuseaddr,fork EXEC:"python chall.py"