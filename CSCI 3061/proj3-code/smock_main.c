#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "matrix.h"

#define MAX_INPUT_LEN 128
#define PROMPT ">> "

int main(int argc, char *argv[]) {
    
    char input[MAX_INPUT_LEN];
    matrix_t *mat = NULL;
    FILE *script = NULL; //script file
    if (argc > 1) { //if there are command line arguments
        script = fopen(argv[1], "r"); //open the script file for reading
        if (script == NULL) {
            printf("Failed to open script file\n");
            return 1; //error handling
        }
    } else {
        printf("SMOCK - Simple Matrix Operations for C Knowledge\n");
        printf("Commands:\n");
        printf("  new <nrows> <ncols>: Create new <nrows> x <ncols> matrix\n");
        printf("  put <i> <j> <value>: Change entry (i,j) of current matrix\n");
        printf("  get <i> <j>: Retrieve entry (i,j) of current matrix\n");
        printf("  print: Print out entries in the current matrix\n");
        printf("  sum: Compute and print out sum of all elements in current matrix\n");
        printf("  max: Compute and print out maximum of all elements in current matrix\n");
        printf("  count <val>: Compute and print out count of all elements with value <val> in current matrix\n");
        printf("  clear: Delete current matrix\n");
        printf("  write_text <file_name>: Write current matrix to a text file\n");
        printf("  read_text <file_name>: Read a matrix from a text file\n");
        printf("  write_bin <file_name>: Write current matrix to a binary file\n");
        printf("  read_bin <file_name>: Read current matrix from a binary file\n");
        printf("  parallel_max <n_procs>: Compute matrix max with multiple processes\n");
        printf("  parallel_count <val> <n_procs>: Compute count of <val> in matrix using multiple processes\n");
        printf("  exit: Quit this program\n");
    }
    while (1) { // Keep reading until we break out of loop
        if (script) {
            if (fscanf(script, "%s", input) == EOF) { //read script file until end
                break;
            }
        } else {
            printf("%s", PROMPT);
            if (scanf("%s", input) == EOF) {
                printf("\n");
                break;
            }
        }
        
        if (strcmp("exit", input) == 0) {
            break;
        }

        else if (strcmp("new", input) == 0) {
            // Always need to read in nrows and ncols
            unsigned nrows;
            unsigned ncols;
            if (script) {
                fscanf(script, "%u %u", &nrows, &ncols); //read the matrix from the script
            } else {
                scanf("%u %u", &nrows, &ncols);
            }
            if (mat != NULL) {
                printf("Error: You must clear the current matrix first\n");
            } else {
                mat = matrix_init(nrows, ncols);
                if (mat == NULL) {
                    printf("Matrix creation failed\n");
                } else {
                    int val;
                    for (int i = 0; i < nrows; i++) {
                        for (int j = 0; j < ncols; j++) {
                            if (script) {
                                fscanf(script, "%d", &val);
                            } else {
                                scanf("%d", &val);
                            }
                            matrix_put(mat, i , j, val);
                        }
                    }
                }
            }
        }

        else if (strcmp("clear", input) == 0) {
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                matrix_free(mat);
                mat = NULL;
            }
        }

        else if (strcmp("print", input) == 0) {
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                for (int i = 0; i < mat->nrows; i++) {
                    printf("  ");
                    for (int j = 0; j < mat->ncols; j++) {
                        printf("%d ", matrix_get(mat, i, j));
                    }
                    printf("\n");
                }
            }
        }

        else if (strcmp("get", input) == 0) {
            // Still have to read these even if no active matrix
            unsigned i;
            unsigned j;
            if (script) {
                fscanf(script, "%u %u", &i, &j); //get an index from the script
            } else {
                scanf("%u %u", &i, &j);
            }
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                printf("%d\n", matrix_get(mat, i, j));
            }
        }

        else if (strcmp("put", input) == 0) {
            // Still have to read these even if no active matrix
            unsigned i;
            unsigned j;
            int val;
            if (script) {
                fscanf(script, "%u %u %d", &i, &j, &val); //put a value based on the script
            } else {
                scanf("%u %u %d", &i, &j, &val);
            }
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                matrix_put(mat, i, j, val);
            }
        }

        else if (strcmp("sum", input) == 0) {
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                printf("%ld\n", matrix_sum(mat));
            }
        }

        else if (strcmp("max", input) == 0) {
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                printf("%d\n", matrix_max(mat));
            }
        }

        else if (strcmp("count", input) == 0) {
            int val;
            if (script) {
                fscanf(script, "%d", &val); //find a count from the script file
            } else {
                scanf("%d", &val);
            }
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                printf("%ld\n", matrix_count(mat, val));
            }
        }

        else if (strcmp("write_text", input) == 0) {
            scanf("%s", input); // Read in file name
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                if (matrix_write_text(mat, input) != 0) {
                    printf("Failed to write matrix to text file\n");
                } else {
                    printf("Matrix successfully written to text file\n");
                }
            }
        }

        else if (strcmp("read_text", input) == 0) {
            scanf("%s", input); // Read in file name
            if (mat != NULL) {
                printf("Error: You must clear the current matrix first\n");
            } else {
                mat = matrix_read_text(input);
                if (mat == NULL) {
                    printf("Failed to read matrix from text file\n");
                } else {
                    printf("Matrix successfully read from text file\n");
                }
            }
        }

        else if (strcmp("write_bin", input) == 0) {
            scanf("%s", input); // Read in file name
            if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                if (matrix_write_bin(mat, input) != 0) {
                    printf("Failed to write matrix to binary file\n");
                } else {
                    printf("Matrix successfully written to binary file\n");
                }
            }
        }

        else if (strcmp("read_bin", input) == 0) {
            scanf("%s", input); // Read in file name
            if (mat != NULL) {
                printf("Error: You must clear the current matrix first\n");
            } else {
                mat = matrix_read_bin(input);
                if (mat == NULL) {
                    printf("Failed to read matrix from binary file\n");
                } else {
                    printf("Matrix successfully read from binary file\n");
                }
            }
        }
        else if (strcmp("parallel_max", input) == 0) {
            int n_procs;
            if (script) {
                fscanf(script, "%d", &n_procs); //parallel max from the script file matrix
            } else {
                scanf("%d", &n_procs);
            }
            if (n_procs <= 0) {
                printf("Error: Invalid n_procs argument\n");
            } else if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                int max_value;
                if (matrix_parallel_max(mat, n_procs, &max_value) == 0) {
                    printf("%d\n", max_value);
                } else {
                    printf("Error computing maximum value\n");
                }
            }
        }
        else if (strcmp("parallel_count", input) == 0) {
            int value;
            unsigned n_procs;
            if (script) {
                fscanf(script, "%d %u", &value, &n_procs); //parallel file from script file
            } else {
                scanf("%d %u",&value, &n_procs);
            }
            if (n_procs <= 0) {
                printf("Error: Invalid n_procs argument\n");
            } else if (mat == NULL) {
                printf("Error: There is no active matrix\n");
            } else {
                int count;
                if (matrix_parallel_count(mat, value, n_procs, &count) == 0) {
                    printf("%d\n", count);
                } else {
                    printf("Error counting occurrences\n");
                }
            }
        }

        else {
            printf("Unknown command'%s'\n", input);
        }
    }
    if (script) {
        fclose(script);
    }
    if (mat != NULL) {
        matrix_free(mat);
    }
    return 0;
}
