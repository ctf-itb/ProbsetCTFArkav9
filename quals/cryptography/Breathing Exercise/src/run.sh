#!/bin/bash
socat tcp-l:8666,reuseaddr,fork exec:"sudo sage --python chall.py"