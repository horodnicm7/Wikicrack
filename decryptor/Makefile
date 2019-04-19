COMPILER = g++

build: main.o utils.o
	$(COMPILER) -o main main.o utils.o
main.o: main.cpp
	$(COMPILER) -c main.cpp
utils.o: utils.cpp
	$(COMPILER) -c utils.cpp
clean:
	rm -rf *.o
	rm -rf main
