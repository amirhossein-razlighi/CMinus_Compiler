#!/bin/bash

pp=tests/S$1

cp $pp/input.txt ./
python3 compiler.py
cat semantic_errors.txt
echo "====="
cat $pp/semantic_errors.txt
echo "====="
diff semantic_errors.txt $pp/semantic_errors.txt
