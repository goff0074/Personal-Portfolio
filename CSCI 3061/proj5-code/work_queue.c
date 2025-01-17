#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "matrix.h"
#include "work_queue.h"

int work_queue_init(work_queue_t *queue, unsigned size) {
    if (size == 0) {
        return -1;
    }

    int err = pthread_mutex_init(&queue->mutex, NULL);
    if (err != 0) {
        fprintf(stderr, "pthread_mutex_init: %s\n", strerror(err));
        return -1;
    }
    err = pthread_cond_init(&queue->item_available, NULL);
    if (err != 0) {
        fprintf(stderr, "pthread_cond_init: %s\n", strerror(err));
        pthread_mutex_destroy(&queue->mutex);
        return -1;
    }
    err = pthread_cond_init(&queue->space_available, NULL);
    if (err != 0) {
        fprintf(stderr, "pthread_cond_init: %s\n", strerror(err));
        pthread_mutex_destroy(&queue->mutex);
        pthread_cond_destroy(&queue->item_available);
    }

    queue->buffer = malloc(size * sizeof(work_queue_item_t));
    if (queue->buffer == NULL) {
        perror("malloc");
        pthread_mutex_destroy(&queue->mutex);
        pthread_cond_destroy(&queue->item_available);
        pthread_cond_destroy(&queue->space_available);
        return -1;
    }

    queue->buf_read_idx = 0;
    queue->buf_write_idx = 0;
    queue->buf_len = 0;
    queue->buf_capacity = size;
    queue->shutdown = 0;
    return 0;
}

int work_queue_free(work_queue_t *queue) {
    free(queue->buffer);
    int ret_val = 0;
    int err;
    err = pthread_mutex_destroy(&queue->mutex);
    if (err != 0) {
        fprintf(stderr, "pthread_mutex_destroy: %s\n", strerror(err));
        ret_val = -1;
    }

    err = pthread_cond_destroy(&queue->item_available);
    if (err != 0) {
        fprintf(stderr, "pthread_cond_destroy: %s\n", strerror(err));
        ret_val = -1;
    }

    err = pthread_cond_destroy(&queue->space_available);
    if (err != 0) {
        fprintf(stderr, "pthread_cond_destroy: %s\n", strerror(err));
        ret_val = -1;
    }

    return ret_val;
}

int work_queue_put(work_queue_t *queue, work_queue_item_t *item) {
    pthread_mutex_lock(&queue -> mutex); //lock queue mutex to make sure we have exclusive access
    while (queue -> buf_len == queue -> buf_capacity) { //if the length is the same as the capacity (full)
        pthread_cond_wait(&queue -> space_available, &queue -> mutex); //wait for space to become available
    }

    queue -> buffer[queue -> buf_write_idx] = *item; //add new item to queue
    queue -> buf_write_idx = (queue -> buf_write_idx + 1) % queue -> buf_capacity; //update write index, using a circular buffer
    queue -> buf_len++; //increment buffer length
    pthread_cond_signal(&queue -> item_available); //signal that an item is able to be processed
    pthread_mutex_unlock(&queue -> mutex); //unlock mutex for other queues
    return 0;
}

int work_queue_get(work_queue_t *queue, work_queue_item_t *dest) {
    pthread_mutex_lock(&queue -> mutex); //lock mutex for exclusivity
    while (queue -> buf_len == 0 && !queue -> shutdown) { //if the buffer length is 0, AND the queue is not shutdown
        pthread_cond_wait(&queue -> item_available, &queue -> mutex); //wait until item is availble
    }
    if (queue->shutdown) { //if the queue is shut down
        pthread_mutex_unlock(&queue -> mutex); //unlock the mutex, return 1 (no more)
        return 1;
    }
    *dest = queue -> buffer[queue -> buf_read_idx]; //retrieve item from current index
    queue -> buf_read_idx = (queue -> buf_read_idx + 1) % queue -> buf_capacity; //update read index with circular buffer
    queue -> buf_len--; //decrement the length
    pthread_cond_signal(&queue -> space_available); //space is now available!
    pthread_mutex_unlock(&queue -> mutex); //unlock mutex for other threads
    return 0;
}

int work_queue_shut_down(work_queue_t *queue) {
    pthread_mutex_lock(&queue->mutex); //lock mutex for exclusivity
    queue->shutdown = 1; //shut the queue down, no more work done
    pthread_cond_broadcast(&queue->item_available); //wake up all waiting, terminate
    pthread_mutex_unlock(&queue->mutex); //unlock the mutex

    return 0;
}
