#include <limits.h>
#include <math.h>
#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include "matrix.h"

typedef struct { //custom struct to hold different arguments that will be passed into threads
    const matrix_t *mat; //Pointer to matrix
    unsigned start_row; //start row of thread
    unsigned end_row; //end row of thread
    long result; //result of the operation
} thread_args_t;

void *worker_thread_sum(void *args) { //HELPER for sum computing
    thread_args_t *mat_data = (thread_args_t *)args; //cast arguments back to struct
    const matrix_t *mat = mat_data->mat; //point to a matrix
    int mat_sum = 0; //initialize sum at 0

    for (int i = mat_data -> start_row; i < mat_data -> end_row; i++) { // loop through the rows indicated by the start/end rows
        for (int j = 0; j < mat -> ncols; j++) { //loop through each column index
            mat_sum += matrix_get(mat, i, j); //obtain that value, add it to our sum
        }
    }
    mat_data -> result = mat_sum; //store result in the struct
    return NULL;
}

void *worker_thread_max(void *args) { //HELPER for max finding
    thread_args_t *mat_data = (thread_args_t *)args; //cast arguments back
    const matrix_t *mat = mat_data -> mat; //pointer to matrix
    int max_val = INT_MIN; //initialize a minimum as the integer minimum

    for (int i = mat_data -> start_row; i < mat_data -> end_row; i++) { //loop through every row for this process
        for (int j = 0; j < mat -> ncols; j++) { //every column index
            int mat_val = matrix_get(mat, i, j); //obtain the value
            if (mat_val > max_val) { 
                max_val = mat_val; //If that obtained value is greater than our stored max, update it to that value
            }
        }
    }
    mat_data -> result = max_val; // store our max value
    return NULL;
}


int matrix_parallel_sum(const matrix_t *mat, unsigned n_threads, long *result) {
    pthread_t tot_threads[n_threads]; //array of total threads
    thread_args_t thread_args[n_threads]; //arguments for each thread

    int thread_rows = (mat -> nrows + n_threads - 1) / n_threads; //rows for each thread
    int thread_start_row = 0; //start row

    for (int i = 0; i < n_threads; i++) { 
        int thread_end_row = thread_start_row + thread_rows; //find the start row for this thread
        if (thread_end_row > mat -> nrows) {
            thread_end_row = mat -> nrows; //if the end row exceeds the matrix rows, set it to the number of rows
        }
        thread_args_t args;
        args.mat = mat;
        args.start_row = thread_start_row;
        args.end_row = thread_end_row;
        thread_args[i] = args; //all of the thread arguments

        if (pthread_create(&tot_threads[i], NULL, worker_thread_sum, &thread_args[i]) != 0) { //create worker thread, have that thread compute its local sum
            perror("Failed to create thread");
            return -1;
        }
        thread_start_row = thread_end_row; //start row becomes the end row of the last thread
    }
    int total_sum = 0;

    for (int i = 0; i < n_threads; i++) { // loop through every thread
        pthread_join(tot_threads[i], NULL); //wait for thread
        total_sum += thread_args[i].result; //add the result to the total
    }

    *result = total_sum; //store the sum
    return 0;
}

int matrix_parallel_max(const matrix_t *mat, unsigned n_threads, long *result) {
    pthread_t tot_threads[n_threads]; //total threads
    thread_args_t thread_args[n_threads]; //thread args

    int thread_rows = (mat -> nrows + n_threads - 1) / n_threads; //rows per thread
    int thread_start_row = 0; //start row

    for (int i = 0; i < n_threads; i++) {
        int thread_end_row = thread_start_row + thread_rows; //find the start row for this thread
        if (thread_end_row > mat -> nrows) {
            thread_end_row = mat -> nrows; //if the end row exceeds the matrix rows, set it to the number of rows
        }
        thread_args_t args;
        args.mat = mat;
        args.start_row = thread_start_row;
        args.end_row = thread_end_row;
        thread_args[i] = args; //all of the arguments
        if (pthread_create(&tot_threads[i], NULL, worker_thread_max, &thread_args[i]) != 0) { //create a thread, have it find local max
            perror("Failed to create thread");
            return -1;
        }
        thread_start_row = thread_end_row; //update start row
    }
    long mat_max = LONG_MIN;

    for (int i = 0; i < n_threads; i++) { //look through every process
        pthread_join(tot_threads[i], NULL); //wait on thread
        if (thread_args[i].result > mat_max) {
            mat_max = thread_args[i].result; //update our max based on threads finding
        }
    }

    *result = mat_max; //store result
    return 0;
}
