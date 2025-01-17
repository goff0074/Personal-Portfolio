#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include "matrix.h"

matrix_t *matrix_init(unsigned nrows, unsigned ncols) {
    matrix_t *mat = malloc(sizeof(matrix_t));
    if (mat == NULL) {
        return NULL;
    }
    mat->data = malloc(nrows * sizeof(int *));
    if (mat->data == NULL) {
        free(mat);
        return  NULL;
    }

    for (int i = 0; i < nrows; i++) {
        mat->data[i] = malloc(ncols * sizeof(int));
        if (mat->data[i] == NULL) {
            // Need to free previously allocated matrix rows
            for (int j = 0; j < i; j++) {
                free(mat->data[j]);
            }
            free(mat->data);
            free(mat);
            return NULL;
        }
    }
    mat->nrows = nrows;
    mat->ncols = ncols;

    return mat;
}

void matrix_free(matrix_t *mat) {
    for (int i = 0; i < mat->nrows; i++) {
        free(mat->data[i]);
    }
    free(mat->data);
    free(mat);
}

void matrix_put(matrix_t *mat, unsigned i, unsigned j, int val) {
    if (i > mat-> nrows && j > mat -> ncols) {
        printf("Error: that index does not exist\n"); //First make sure the user is trying to put a number in an index not present in the matrix
    } else {
        mat -> data[i][j] = val; //Set the matrix index to that number
    }
}

int matrix_get(const matrix_t *mat, unsigned i, unsigned j) {
    if (i > mat-> nrows && j > mat -> ncols) {
        printf("Error: entered index does not exist\n");
        return -1; //Once again make sure the user enters in an index that is in bounds
    } else {
        return mat -> data[i][j]; // return the value at that index
    }
}

long matrix_sum(const matrix_t *mat) {
    long matrix_sum = 0; //Initialize a long variable
    for (int i = 0; i < mat -> nrows; i++) {
        for (int j = 0; j < mat -> ncols; j++) {
            matrix_sum += mat -> data[i][j]; //Loop through the rows & cols, adding each value to the sum
        }
    }
    return matrix_sum;
}

int matrix_max(const matrix_t *mat) {
    int matrix_max = mat -> data[0][0]; //Initialize the max as the first index
    for (int i = 0; i < mat -> nrows; i++) {
        for (int j = 0; j < mat -> ncols; j++) {
            if (mat -> data[i][j] > matrix_max) {
                matrix_max = mat -> data[i][j]; //Loop through the rows and columns, checking if the current value is greater than the previous max
            }
        }
    }
    return matrix_max;
}

long matrix_count(const matrix_t *mat, int val) {
    long val_count = 0; //initialize a count variable
    for (int i = 0; i < mat -> nrows; i++) {
        for (int j = 0; j < mat -> ncols; j++) {
            if (mat -> data[i][j] == val) { //Loop through each index, and check if the current index is equal to the entered value
                val_count += 1; //If it is, add 1 to the count for that value
            }
        }
    }
    return val_count;
}

int matrix_write_text(const matrix_t *mat, const char *file_name) {
    FILE *f = fopen(file_name, "w");
    if (f == NULL) {
        return -1;
    }

    fprintf(f, "%u %u\n", mat->nrows, mat->ncols);
    for (int i = 0; i < mat->nrows; i++) {
        for (int j = 0; j < mat->ncols; j++) {
            fprintf(f, "%d ", mat->data[i][j]);
        }
        fprintf(f, "\n");
    }

    fclose(f);
    return 0;
}

matrix_t *matrix_read_text(const char *file_name) {
    FILE *f = fopen(file_name, "r");
    if (f == NULL) {
        return NULL; // check to see if the file opened correctly
    }
    int nrows, ncols;
    if (fscanf(f, "%u %u", &nrows, &ncols) != 2) { //Make sure to read the dimensions from the file
        fclose(f);
        return NULL;
    }
    matrix_t *mat = matrix_init(nrows, ncols); //Initialize the matrix
    if (mat == NULL) {
        fclose(f);
        return NULL; //Make sure the matrix initializing worked
    }
    for (int i = 0; i < nrows; i++) {
        for (int j = 0; j < ncols; j++) {
            if (fscanf(f, "%d", &(mat -> data[i][j])) != 1) { //Loop through every index in the text tile matrix, and assign it to the initialized matrix above in the correct index
                fclose(f);
                matrix_free(mat); //Free the memory for the matrix
                return NULL;
            }
        }
    }
    fclose(f);
    return mat; //Close the file and return the matrix
    
}

int matrix_write_bin(const matrix_t *mat, const char *file_name) {
    FILE *f = fopen(file_name, "wb");
    if (f == NULL) {
        printf("ERROR: Failed to open binary file for matrix writing\n");
        return -1; //Check to make sure the file opening works
    }
    if (fwrite(&(mat->nrows), sizeof(unsigned), 1, f) != 1 || fwrite(&(mat->ncols), sizeof(unsigned), 1, f) != 1) {
        printf("ERROR: Failed to write matrix dimensions to binary matrix");
        return -1; //Make sure the writing of the matrix dimensions works, and write them to the binary file
    }
    for (int i = 0; i < mat -> nrows; i++) {
        fwrite(mat -> data[i], sizeof(int), mat -> ncols, f); //loop through all of the matrix and write it to the binary file
    }
    fclose(f); //close the file
    return 0;
}

matrix_t *matrix_read_bin(const char *file_name) {
    FILE *f = fopen(file_name, "rb");
    if (f == NULL) {
        return NULL; //Make sure the file opening worked
    }
    int nrows, ncols;
    if (fread(&nrows, sizeof(int), 1, f) != 1 || fread(&ncols, sizeof(int), 1, f) != 1) {
        fclose(f);
        return NULL; //Make sure the reading of the dimensions worked correctly
    }
    matrix_t *mat = matrix_init(nrows, ncols); //initialize the matrix
    if (mat == NULL) {
        fclose(f);
        return NULL; //make sure the initialization worked
    }
    for (int i = 0; i < nrows; i++) {
        if (fread(mat -> data[i], sizeof(int), ncols, f) != ncols) {
            fclose(f);
            matrix_free(mat);
            return NULL; //Loop through the information in the binary matrix file, reading all of the indexes and their values
        }
    }
    fclose(f);
    return mat;
}
