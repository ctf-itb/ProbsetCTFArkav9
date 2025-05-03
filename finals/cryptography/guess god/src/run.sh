#!/bin/bash
socat tcp-l:8369,reuseaddr,fork exec:"python chall.py"