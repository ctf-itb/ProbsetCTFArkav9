#!/bin/sh
socat tcp-l:8010,reuseaddr,fork exec:"sudo sage --python chall.py"