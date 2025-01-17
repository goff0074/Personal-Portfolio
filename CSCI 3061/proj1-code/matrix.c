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

void matrix_free(matrix_t *mat) { // Free the memory for a matrix
    if (mat != NULL) {
        for (int i = 0; i < mat->nrows; i++) {
            free(mat->data[i]); // Loop through each row, clearing memory for each of the rows
        }
        free(mat->data); //Free memory for the data
        free(mat); //Free memory for the matrix
    }
}

void matrix_put(matrix_t *mat, unsigned i, unsigned j, int val) { //Place a number in a matrix slot
    if (mat == NULL) {
        printf("Error: There is no active matrix\n"); //Check to see if there is a matrix active
    } else {
        mat->data[i][j] = val; //Set a specific index in the matrix to a specific number
    }
    
}

int matrix_get(const matrix_t *mat, unsigned i, unsigned j) { //Retrieve the content of an index of a matrix
    if (mat == NULL) {
        printf("Error: There is no active matrix\n");
        return 0; //Return an error if there isnt a matrix active
    } else {
        return mat->data[i][j]; //Return the value at the specified index
    }
}

long matrix_sum(const matrix_t *mat) { //Find the sum of every index of a matrix
    if (mat == NULL) {
        printf("Error: There is no active matrix\n");
        return 0; //Check to see if there is an active matrix
    } else {
        long sum = 0; //Initialize a sum
        for (int i = 0; i < mat->nrows; i++) {
            for (int j = 0; j < mat->ncols; j++) {
                sum += mat->data[i][j]; //Loop through every row and column, then add every value in each index to the sum
            }
        }
        return sum; //return the sum
    }
}

int matrix_max(const matrix_t *mat) { //Find the max of the matrix
    if (mat == NULL) {
        printf("Error: There is no active matrix\n");
        return 0; //Check to see if there is an active matrix
    } else {
        int mat_max = mat->data[0][0]; //Initialize the first value as the max
        for (int i = 0; i < mat->nrows; i++) {
            for (int j = 0; j < mat->ncols; j++) { //Loop through each row and column of the matrix
                if (mat->data[i][j] > mat_max) {
                    mat_max = mat->data[i][j]; //If the value at that index is higher than the stored max, update the max
                }
            }
        }
        return mat_max; //Return the value of the max
    }
}

int matrix_write_text(const matrix_t *mat, const char *file_name) {
    if (mat == NULL) {
        printf("Error: There is no active matrix\n");
        return -1;
    }
    FILE *f = fopen(file_name, "w"); //open the file for writing
    if (f == NULL) {
        printf("Failed to write matrix to text file\n");
        return -1;
    }

    fprintf(f, "%u %u\n", mat->nrows, mat->ncols); // write the dimensions of the file to the first line of the file
    for (int i = 0; i < mat->nrows; i++) {
        for (int j = 0; j < mat->ncols; j++) {
            fprintf(f, "%d ", mat->data[i][j]); //Loop through the active matrix, and write the current index to the correct spot in the file
        }
        fprintf(f, "\n");
    }

    fclose(f);
    return 0;
}

matrix_t *matrix_read_text(const char *file_name) { //Read a matrix in from a text file
    FILE *f = fopen(file_name, "r"); //Open up the text file for reading
    if (f == NULL) {
        return NULL;
    }
    unsigned nrows, ncols;
    if (fscanf(f, "%u %u", &nrows, &ncols) != 2) { //Read the matrix dimensions from the text file
        fclose(f);
        return NULL;
    }
    matrix_t *mat = matrix_init(nrows, ncols); //Create a new matrix with the dimensions above
    if (mat == NULL) {
        fclose(f);
        return NULL;
    }
    for (int i = 0; i < nrows; i++) { 
        for (int j = 0; j < ncols; j++) {
            if (fscanf(f, "%d", &(mat->data[i][j])) != 1) { //Loop through every "index" in the text file, and assign it to the appropriate index in the matrix
                fclose(f);
                matrix_free(mat);
                return NULL;
            }
        }
    }
    fclose(f);
    return mat; //Return the matrix
}

int matrix_write_bin(const matrix_t *mat, const char *file_name) { //Write a matrix to a binary file
    if (mat == NULL) {
        printf("Error: There is no active matrix\n");
        return -1;
    }
    FILE *f = fopen(file_name, "wb"); //Open a file to write a matrix in binary
    if (f == NULL) {
        printf("Failed to write matrix to binary file\n");
        return -1;
    }
    fwrite(&(mat->nrows), sizeof(unsigned), 1, f); //Write the number of rows
    fwrite(&(mat->ncols), sizeof(unsigned), 1, f); //Write the number of columns
    for (int i = 0; i < mat->nrows; i++) {
        fwrite(mat->data[i], sizeof(int), mat->ncols, f); //Write each element of the matrix into binary
    }
    fclose(f);
    return 0;
}

matrix_t *matrix_read_bin(const char *file_name) { //Read in a matrix from a binary file
    FILE *f = fopen(file_name, "r"); //Open a binary file for reading
    if (f == NULL) {
        return NULL;
    }
    unsigned nrows, ncols; //Get the rows and columns from the file
    if (fread(&nrows, sizeof(unsigned), 1, f) != 1 || fread(&ncols, sizeof(unsigned), 1, f) != 1) {
        fclose(f);
        return NULL;
    }
    matrix_t *mat = matrix_init(nrows, ncols); //Create a matrix with the dimensions stored above
    if (mat == NULL) {
        fclose(f);
        return NULL;
    }
    for (int i = 0; i < nrows; i++) {
        if (fread(mat->data[i], sizeof(int), ncols, f) != ncols) { //Read each element from the binary file
            fclose(f);
            matrix_free(mat);
            return NULL;
        }
    }
    fclose(f);
    return mat;
}
