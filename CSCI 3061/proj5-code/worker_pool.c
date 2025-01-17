#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "worker_pool.h"
#include "matrix.h"
#include "task_group.h"

void *worker_thread_func(void *arg) {
    work_queue_t *queue = (work_queue_t *)arg; //cast argument to pointer of work queue
    work_queue_item_t item; //variable to hold an item (task retrieved)

    while (1) { //check and process tasks until the queue is completely empty 
        if (work_queue_get(queue, &item) != 0) { //try to retrieve an item from the queue
            break; // if none available, break the loop
        }
        int row_sum = 0; //variable for the row sum
        for (int i = 0; i < item.mat -> ncols; i++) { //loop through the columns
            row_sum += item.mat->data[item.row_num * item.mat -> ncols + i]; //access matrix value (row major indexing)
        }
        pthread_mutex_lock(item.dest_mutex); //lock mutex to ensure only one thread updates at a time
        *(item.destination) += row_sum; // add rows sum to the total sum
        pthread_mutex_unlock(item.dest_mutex); //unlock mutex after you update
        task_group_done(item.task_group); //signal your task is done
    }
    return NULL;
}

int worker_pool_init(worker_pool_t *pool, unsigned pool_size, unsigned queue_size) {
    if (pool_size == 0 || queue_size == 0) {
        return -1;
    }

    pool->threads = malloc(pool_size * sizeof(pthread_t));
    if (pool->threads == NULL) {
        return -1;
    }

    if (work_queue_init(&pool->queue, queue_size) == -1) {
        free(pool->threads);
        return -1;
    }
    pool->size = pool_size;

    for (int i = 0; i < pool_size; i++) {
        int err = pthread_create(pool->threads + i, NULL, worker_thread_func, &pool->queue);
        if (err != 0) {
            fprintf(stderr, "pthread_create: %s\n", strerror(err));
            work_queue_shut_down(&pool->queue);
            for (int j = 0; j < i; j++) {
                pthread_join(pool->threads[j], NULL);
            }
            work_queue_free(&pool->queue);
            free(pool->threads);
            return -1;
        }
    }

    return 0;
}

int worker_pool_free(worker_pool_t *pool) {
    if (work_queue_shut_down(&pool->queue) == -1) {
        return -1;
    }
    int ret_val = 0;
    int err;
    for (int i = 0; i < pool->size; i++) {
        err = pthread_join(pool->threads[i], NULL);
        if (err != 0) {
            fprintf(stderr, "pthread_join: %s\n", strerror(err));
            ret_val = -1;
        }
    }
    free(pool->threads);
    if (work_queue_free(&pool->queue) != 0) {
        ret_val = -1;
    }
    return ret_val;
}

int matrix_parallel_sum_pool(const matrix_t *mat, worker_pool_t *pool, long *result) {
    *result = 0;

    task_group_t group;
    if (task_group_init(&group, mat->nrows) == -1) {
        printf("Task goup initialization failed\n");
        return -1;
    }

    pthread_mutex_t result_mutex;
    int err = pthread_mutex_init(&result_mutex, NULL);
    if (err != 0) {
        fprintf(stderr, "pthread_mutex_init: %s\n", strerror(err));
        return -1;
    }

    // Put one item into queue for each row of the matrix
    work_queue_item_t item;
    item.mat = mat;
    item.destination = result;
    item.dest_mutex = &result_mutex;
    item.task_group = &group;
    for (int i = 0; i < mat->nrows; i++) {
        item.row_num = i;
        if (work_queue_put(&pool->queue, &item) == -1) {
            return -1;
        }
    }

    // Wait for all workers to finish summing each row
    if (task_group_wait(&group) == -1) {
        return -1;
    }
    return 0;
}
