SHELL = /bin/bash
AN = proj5
CFLAGS = -Wall -Werror -g
CC = gcc $(CFLAGS)
CWD = $(shell pwd | sed 's/.*\///g')

.PHONY: clean clean-tests test-setup test

smock: matrix_1.o matrix_5.o work_queue.o worker_pool.o task_group.o smock_main.c
	$(CC) -o $@ $^ -lm -lpthread

matrix_5.o: matrix.h matrix_5.c
	$(CC) -c matrix_5.c

work_queue.o: work_queue.h work_queue.c
	$(CC) -c work_queue.c

worker_pool.o: worker_pool.h worker_pool.c
	$(CC) -c worker_pool.c

task_group.o: task_group.h task_group.c
	$(CC) -c task_group.c

test-setup:
	@chmod u+x testius

ifdef testnum
test: test-setup smock
	./testius test_cases/tests.json -v -n "$(testnum)"
else
test: test-setup smock
	./testius test_cases/tests.json
endif

clean:
	rm -f smock matrix_5.o work_queue.o worker_pool.o task_group.o

clean-tests:
	rm -rf test_results/

zip: clean clean-tests
	rm -f $(AN)-code.zip
	cd .. && zip "$(CWD)/$(AN)-code.zip" -r "$(CWD)" -x "$(CWD)/test_cases/*"
	@echo Zip created in $(AN)-code.zip
	@if (( $$(stat -c '%s' $(AN)-code.zip) > 10*(2**20) )); then echo "WARNING: $(AN)-code.zip seems REALLY big, check there are no abnormally large test files"; du -h $(AN)-code.zip; fi
	@if (( $$(unzip -t $(AN)-code.zip | wc -l) > 256 )); then echo "WARNING: $(AN)-code.zip has 256 or more files in it which may cause submission problems"; fi
