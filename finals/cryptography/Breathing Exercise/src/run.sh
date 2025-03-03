#!/bin/bash
socat tcp-l:13750,reuseaddr,fork exec:"sudo sage --python chall.py"