all: compile
compile: pa2
pa2: pa2.cpp
	g++ -std=c++11 -o pa2 pa2.cpp
test: compile
	./test
test_alot: compile
	./test_alot
.PHONY: all compile test
