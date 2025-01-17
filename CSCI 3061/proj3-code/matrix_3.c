#include <limits.h>
#include <math.h>
#include <netdb.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/wait.h>
#include <unistd.h>
#include "matrix.h"

int matrix_parallel_max(const matrix_t *mat, unsigned n_procs, int *result) {
    int pipe_mats[2]; //initialize a pipe
    if (pipe(pipe_mats) == -1) {
        return -1; //pipe error handling
    }
    pid_t pid; //process IDs

    int rows_per_proc = mat->nrows / n_procs; //Find rows for each process
    int other_rows = mat->nrows % n_procs; //Find remainder rows
    int mat_max_val = INT_MIN; //Initialize a max value

    for (int i = 0; i < n_procs; i++) { //create the correct child processes
        pid = fork(); //fork the process
        if (pid == -1) {
            return -1;
        }
        if (pid == 0) { //child process
            close(pipe_mats[0]); //close read side

            int initial_start_row = i * rows_per_proc; //starting row for the process
            int offset_if_extra;
            if (i < other_rows) {
                offset_if_extra = i; //extra row if needed
            } else {
                offset_if_extra = other_rows; //no extras
            }
            int start_row = initial_start_row + offset_if_extra; //find correct starting row with the offset included

            int num_rows;
            if (i < other_rows) {
                num_rows = rows_per_proc + 1; //an extra row for this process if you need
            } else {
                num_rows = rows_per_proc;
            }

            int local_max = INT_MIN; //initialize a local max
            for (int i = start_row; i < start_row + num_rows; i ++) {
                for (int j = 0; j < mat -> ncols; j++) { //loop thorugh these process rows and their indexes
                    if (mat->data[i][j] > local_max) { 
                        local_max = mat -> data[i][j]; //update the local max if it is higher than the current max
                    }
                }
            }
            write(pipe_mats[1], &local_max, sizeof(int)); //write the max
            close(pipe_mats[1]);
            exit(0); //Close and exit pipe and processes
        }

    }
    close(pipe_mats[1]); //close writing side
    for (int i = 0; i < n_procs; i++) { //loop through processes
        int local_max;
        read(pipe_mats[0], &local_max, sizeof(int)); //read local max
        if (local_max > mat_max_val) {
            mat_max_val = local_max; //update the matrix max if applicable
        }
        wait(NULL); //wait on the child
    }
    close(pipe_mats[0]); //close read end
    *result = mat_max_val; //store the max val
    return 0;
}

int matrix_parallel_count(const matrix_t *mat, int val, unsigned n_procs, int *result) {
    int pipe_mats[2]; //initialize a pipe
    if (pipe(pipe_mats) == -1) {
        return -1; //pipe error handling
    }
    pid_t pid; //process IDs
    int total_elems = mat -> nrows * mat -> ncols; //calculate the total elements
    int elems_per_proc = total_elems / n_procs; //calc elements for each process
    int remain_elems = total_elems % n_procs; //find the remaining elements
    int total_count = 0; //initialize a count

    for (int i = 0; i < n_procs; i++) { //create the appropriate amount of processes
        pid = fork(); //fork the process
        if (pid == -1) {
            return -1; //pipe error
        }
        if (pid == 0) {
            close(pipe_mats[0]);//close the read end

            int start_elem_child = i * elems_per_proc; //start element for applicaple process
            int num_elems_child = elems_per_proc; //elements for this specific process

            if (i < remain_elems) {
                num_elems_child = elems_per_proc + 1; //an extra element if there are remaining
            }
            if (i < remain_elems) {
                start_elem_child = start_elem_child + i; //alter starting point if there are remainders
            } else {
                start_elem_child = start_elem_child + remain_elems; //start after the previous childs indexes
            }

            int local_count = 0; //initialize a local count
            for (int i = start_elem_child; i < start_elem_child + num_elems_child; i++) {
                int row = i / mat->ncols; //find the row index
                int col = i % mat->ncols; //find the column index
                if (mat -> data[row][col] == val) {
                    local_count++; //if the current value is equal to the specified one, add one to the count
                }
            }
            write(pipe_mats[1], &local_count, sizeof(int)); //write the result to the pipe
            close(pipe_mats[1]); //close write end
            exit(0); //terminate process

        }
    }
    close(pipe_mats[1]); //close write side
    for (int i = 0; i < n_procs; i++) { //loop through all processes
        int local_count;
        read(pipe_mats[0], &local_count, sizeof(int)); //read local count from the pipe
        total_count += local_count; //add the local count to the total
        wait(NULL); //wait on the child
    }
    close(pipe_mats[0]); //close read end
    *result = total_count; //store the total count result
    return 0;

}
