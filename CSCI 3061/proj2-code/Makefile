SHELL = /bin/bash
AN = proj2
CFLAGS = -Wall -Werror -g
CC = gcc $(CFLAGS)
CWD = $(shell pwd | sed 's/.*\///g')

.PHONY: all clean test-setup test clean-tests

all: smock

smock: matrix_2.o smock_main.c
	$(CC) -o $@ $^

matrix_2.o: matrix.h matrix_2.c
	$(CC) -c matrix_2.c

clean:
	rm -f smock *.o

test-setup:
	@chmod u+x testius
	rm -f my_matrix.txt my_matrix.bin test_matrix.txt test_matrix.bin \
		large_test.txt large_test.bin

ifdef testnum
test: test-setup smock
		./testius test_cases/tests.json -v -n "$(testnum)"
else
test: test-setup smock
	./testius test_cases/tests.json
endif

clean-tests:
	rm -rf test_results my_matrix.txt my_matrix.bin test_matrix.txt \
		test_matrix.bin large_test.txt large_test.bin

zip: clean clean-tests
	rm -f $(AN)-code.zip
	cd .. && zip "$(CWD)/$(AN)-code.zip" -r "$(CWD)" -x "$(CWD)/test_cases/*"
	@echo Zip created in $(AN)-code.zip
	@if (( $$(stat -c '%s' $(AN)-code.zip) > 10*(2**20) )); then echo "WARNING: $(AN)-code.zip seems REALLY big, check there are no abnormally large test files"; du -h $(AN)-code.zip; fi
	@if (( $$(unzip -t $(AN)-code.zip | wc -l) > 256 )); then echo "WARNING: $(AN)-code.zip has 256 or more files in it which may cause submission problems"; fi
