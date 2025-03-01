#!/bin/bash

./redpwnpow && exec timeout --foreground 30 wasmtime --dir . chall
