VISUAL?=kate

all: compile-linux

clean:
	rm -rf obj

edit:
	$(VISUAL) ../../dataview/C/dataview-uniq.h \
                  src/hello_world.h \
                  src/hello_world.c

compile-linux:
	mkdir -p obj && cd obj && gcc -c ../src/*.c
