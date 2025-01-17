#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "matrix.h"

#define MAX_INPUT_LEN 128
#define PROMPT ">> "

/*
 * This is generally similar to the linked list application you will see in lab 2
 * One big difference is the notion of switching between different matrices in one
 * run of the program.
 * You have to create or load a matrix from a file before you can do things like
 * print, sum, and max operations.
 * Also, the user must explicitly clear the current matrix before they can create
 * or load in a new matrix.
 */
int main(int argc, char *argv[]) {
    printf("SMOCK - Simple Matrix Operations for C Knowledge\n");
    printf("Commands:\n");
    printf("  new <nrows> <ncols>: Create new <nrows> x <ncols> matrix\n");
    printf("  put <i> <j> <value>: Change entry (i,j) of current matrix\n");
    printf("  get <i> <j>: Retrieve entry (i,j) of current matrix\n");
    printf("  print: Print out entries in the current matrix\n");
    printf("  sum: Compute and print out sum of all elements in current matrix\n");
    printf("  max: Compute and print out maximum of all elements in current matrix\n");
    printf("  clear: Delete current matrix\n");
    printf("  write_text <file_name>: Write current matrix to a text file\n");
    printf("  read_text <file_name>: Read a matrix from a text file\n");
    printf("  write_bin <file_name>: Write current matrix to a binary file\n");
    printf("  read_bin <file_name>: Read current matrix from a binary file\n");
    printf("  exit: Quit this program\n");

    char input[MAX_INPUT_LEN];
    matrix_t *mat = NULL;
    while (1) { // Keep reading until we break out of loop
        printf("%s", PROMPT);

        if (scanf("%s", input) == EOF) {
            printf("\n");
            break;
        }

        if (strcmp("exit", input) == 0) {
            break;
        }

        else if (strcmp("new", input) == 0) {
            if (mat != NULL) {
                printf("Error: You must clear the current matrix first\n");
            } else {
                unsigned nrows;
                unsigned ncols;
                scanf("%u %u", &nrows, &ncols);
                mat = matrix_init(nrows, ncols);
                if (mat == NULL) {
                    printf("Matrix creation failed\n");
                } else {
                    int val;
                    for (int i = 0; i < nrows; i++) {
                        for (int j = 0; j < ncols; j++) {
                            scanf("%d", &val);
                            matrix_put(mat, i , j, val);
                        }
                    }
                }
            }
        }

        else if (strcmp("put", input) == 0) {
            // Still have to read these even if no active matrix
            unsigned i;
            unsigned j;
            int val;
            scanf("%u %u %d", &i, &j, &val);
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                matrix_put(mat, i, j, val);
            }
        }

        else if (strcmp("get", input) == 0) { //Get an index from a matrix
            unsigned i;
            unsigned j;
            scanf("%u %u", &i, &j);
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                int mat_getval = matrix_get(mat,i,j); //call matrix_get to get the value at the desired index
                printf("%d\n", mat_getval); //Print the value that was obtained
            }
        }

        else if (strcmp("print", input) == 0) { //Print a matrix
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                for (int i = 0; i < mat->nrows; i++) {
                    for (int j = 0; j < mat->ncols; j++) {
                        printf(" %d", mat->data[i][j]); //Loop through the rows and columns, printing the matrix as you go
                    }
                    printf("\n"); //Print a newline after each row
                }
            }
        }
        else if (strcmp("sum", input) == 0) { //Find the sum of each index in the matrix
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                long mat_sum = matrix_sum(mat); //Call matrix_sum to get a sum
                printf("%ld\n", mat_sum); //Print a sum
            }
        }
        else if (strcmp("max", input) == 0) { //Find the max value in a matrix
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                int mat_maxval = matrix_max(mat); //Call matrix_max to get the max
                printf("%d\n", mat_maxval); //Print out the max
            }
        }
        else if (strcmp("clear", input) == 0) { //Clear a matrix
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                matrix_free(mat); //Clear memory for the matrix
                mat = NULL; //Set the matrix to NULL, clearing it
            }
        }
        else if (strcmp("write_text", input) == 0) { //Write the matrix to a text file
            char file_name[MAX_INPUT_LEN];
            scanf("%s", file_name); //Get a file name
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                int write_text_result = matrix_write_text(mat, file_name); //Call matrix_write_text
                if (write_text_result == 0) {
                    printf("Matrix successfully written to text file\n"); //If it returns 0, it successfully was written
                } else {
                    printf("Failed to write matrix to text file\n"); //Otherwise, it failed
                }
            }
        }
        else if (strcmp("read_text", input) == 0) { //Read a matrix in from a text file
            char file_name[MAX_INPUT_LEN]; //Get a file name
            scanf("%s", file_name);
            if (mat != NULL) {
                printf("Error: You must clear the current matrix first\n");
            } else {
                mat = matrix_read_text(file_name); //Call matrix_read_text to get the matrix from the file read
                if (mat == NULL) {
                    printf("Failed to read matrix from text file\n"); //If no matrix is active, the read failed
                } else {
                    printf("Matrix successfully read from text file\n"); //Otherwise, the read worked
                }
            }
        }
        else if (strcmp("write_bin", input) == 0) { //Write the matrix description to a binary file
            char file_name[MAX_INPUT_LEN];
            scanf("%s", file_name); //Get a file name
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                int write_bin_result = matrix_write_bin(mat, file_name); //Call matrix_write_bin to write a matrix to a binary file
                if (write_bin_result == 0) {
                    printf("Matrix successfully written to binary file\n"); //if it returned 0, it successfully was written
                } else {
                    printf("Failed to write matrix to binary file\n"); //Otherwise, it did not write to a binary file correctly
                }
            }
        }
        else if (strcmp("read_bin", input) == 0) { //Read a matrix from a binary file
            char file_name[MAX_INPUT_LEN];
            scanf("%s", file_name); //Get a file name
            if (mat != NULL) {
                printf("Error: You must clear the current matrix first\n");
            } else {
                mat = matrix_read_bin(file_name); //Call matrix_read_bin to read in a matrix from a binary file
                if (mat == NULL) {
                    printf("Failed to read matrix from binary file\n"); //If the active matrix is null, the read did not work
                } else {
                    printf("Matrix successfully read from binary file\n"); //Otherwise, the read was successful
                }
            }
        }

        else {
            printf("Unknown command'%s'\n", input);
        }
    }

    if (mat != NULL) {
        matrix_free(mat);
    }
    return 0;
}
