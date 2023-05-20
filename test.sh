#! /bin/bash

tests=$(ls tests/)
lnthresh=20

for test in $tests; do
	echo "[[[================ RUNNING $test ================]]]"
	path=tests/$test
	cp $path/input.txt ./
	echo "=========== compiler message ============="
	python3 compiler.py
	if [[ ! $? ]]; then
		echo "FAILED"
		continue
	fi;
	echo "=========== diff parse tree ============="
	lines=$(diff parse_tree.txt $path/parse_tree.txt | wc -l)
	if (( lines > lnthresh )); then
		diff parse_tree.txt $path/parse_tree.txt | head -n$lnthresh
		echo "..."
	else
		diff parse_tree.txt $path/parse_tree.txt 
	fi;
	echo "=========== diff syntax errors ============="
	lines=$(diff syntax_errors.txt $path/syntax_errors.txt | wc -l)
	if (( lines > lnthresh )); then
		diff syntax_errors.txt $path/syntax_errors.txt | head -n$lnthresh
		echo "..."
	else
		diff syntax_errors.txt $path/syntax_errors.txt 
	fi;
	echo ""
done;
echo "DONE TESTING"
