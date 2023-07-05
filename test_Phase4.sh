#!/bin/bash

# Loop through each folder in ./tests/phase4_testcases that doesn't end with "_r"
for folder in ./tests/phase4_testcases/*[^_r]; do
    if [ -d "$folder" ]; then
        echo "Running test in folder: $folder"

        # Copy the content of input.txt to ./input.txt
        cp "$folder/input.txt" ./input.txt

        # Run "python3 compiler.py"
        python3 compiler.py

        # Run "./tester_mac.out > expect.txt"
        ./tester_mac.out > expect.txt

        # Remove the last line of expect.txt using awk
        awk 'NR>1{print prev} {prev=$0}' expect.txt > expect.tmp && mv expect.tmp expect.txt

        # Run diff of "./expect.txt" and "expected.txt"
        diff_result=$(diff -q --ignore-all-space "./expect.txt" "$folder/expected.txt")

        # Check the diff result
        if [ $? -eq 0 ]; then
            echo "Test passed"
        else
            echo "Test failed"
            echo "Difference:"
            diff "./expect.txt" "$folder/expected.txt"
        fi

        echo "------------------------------"
    fi
done
