all: compile
compile: pa2
pa2: pa2.cpp
	g++ -std=c++11 -o pa2 pa2.cpp
test: compile
	./test
test_alot: compile
	./test_alot
draw: corrupt_exp drop_exp
	python3 plot.py
corrupt_exp: compile
	bash experiment.sh
drop_exp: corrupt_exp
.PHONY: all compile test
