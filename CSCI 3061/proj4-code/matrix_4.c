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



matrix_t *matrix_download_udp(const char *host, const char *port, const char *matrix_name) {
    struct addrinfo hints, *ser;
    memset(&hints, 0, sizeof(hints)); //Initialize addr info (all 0)
    hints.ai_family = AF_INET; //IPv4
    hints.ai_socktype = SOCK_DGRAM; //UDP
    matrix_t *mat = NULL; //Matrix pointer
    int sockfd; //Socket

    if (getaddrinfo(host, port, &hints, &ser) != 0) {
        return NULL; //Get the address info, return NUll if there was an error
    }

    if ((sockfd = socket(ser->ai_family, ser->ai_socktype, ser->ai_protocol)) == -1) { //Create UDP socket
        freeaddrinfo(ser); //If it fails, free the addr info and return NULL
        return NULL; 
    }

    char request[128]; //request array to store information
    snprintf(request, sizeof(request), "goff0074:%s", matrix_name); //format the message (x500: matrix name)
    if (sendto(sockfd, request, strlen(request), 0, ser->ai_addr, ser->ai_addrlen) == -1) { //send the request through the socket
        close(sockfd);
        freeaddrinfo(ser);
        return NULL; //if the request fails, close the socket, free the addr info and return NULL
    }

    unsigned char mat_buffer[4112]; //create an array for the matrix information (matrix status (4), rows, (4 bytes), columns (4 bytes), and the matrix information (4108))
    socklen_t addr_len = ser->ai_addrlen; //length of the address
    ssize_t bytes_rec = recvfrom(sockfd, mat_buffer, sizeof(mat_buffer), 0, ser -> ai_addr, &addr_len); //amount of bytes received

    int32_t status = (mat_buffer[3]) | (mat_buffer[2] << 8) | (mat_buffer[1] << 16) | (mat_buffer[0] << 24); //convert the "status" aspect of the buffer from big endian to little endian
    int32_t mat_rows = (mat_buffer[7]) | (mat_buffer[6] << 8) | (mat_buffer[5] << 16) | (mat_buffer[4] << 24); //convert the "rows" aspect of the buffer from big endian to little endian
    int32_t mat_cols = (mat_buffer[11]) | (mat_buffer[10] << 8) | (mat_buffer[9] << 16) | (mat_buffer[8] << 24); //convert the "colums" aspect of the buffer from big endian to little endian
    if (status != 0 || mat_rows <= 0 || mat_cols <= 0) {
        close(sockfd);
        freeaddrinfo(ser);
        return NULL; //Return NULL if the status is not 0, or the rows/columns is invalid
    }
    mat = matrix_init(mat_rows, mat_cols); //initialize a matrix
    if (mat == NULL) {
        close(sockfd);
        freeaddrinfo(ser);
        return NULL; //handle creation issues
    }
    
    unsigned char *mat_data_ptr = mat_buffer + 12; //create a pointer for the mat_buffer that ignores the first 12 bytes to read in matrix index data
    for (int i = 0; i < mat -> nrows; i++) {
        for (int j = 0; j < mat -> ncols; j++) { //loop through rows/cols to fill the matrix
            if (mat_data_ptr >= mat_buffer + bytes_rec) { //see if we have reached the end
                matrix_free(mat);
                close(sockfd);
                freeaddrinfo(ser);
                return NULL; //free all of the data if you reach the end
            }
            int32_t value = (mat_data_ptr[3]) | (mat_data_ptr[2] << 8) | (mat_data_ptr[1] << 16) | (mat_data_ptr[0] << 24); //convert the value from big endian to little endian
            matrix_put(mat, i, j, value); //place the value in the matrix
            mat_data_ptr += 4; // increment the pointer
        }
    }
    
    close(sockfd);
    freeaddrinfo(ser);
    return mat; //close socket, free addr info, and return the matrix

}

matrix_t *matrix_download_tcp(const char *host, const char *port, const char *matrix_name) {
    struct addrinfo hints, *ser;
    memset(&hints, 0, sizeof(hints)); //initialize addr info (all 0)
    hints.ai_family = AF_INET; //ipv4
    hints.ai_socktype = SOCK_STREAM; //TCP
    matrix_t *mat = NULL; //matrix pointer
    int sockfd;
    if (getaddrinfo(host, port, &hints, &ser) != 0) {
        return NULL; //return NULL if addrinfo does not work
    }

    if ((sockfd = socket(ser->ai_family, ser->ai_socktype, ser->ai_protocol)) == -1) {
        freeaddrinfo(ser);
        return NULL; //return addr info if socket connection does not work
    }
    if (connect(sockfd, ser->ai_addr, ser->ai_addrlen) == -1) {
        close(sockfd);
        freeaddrinfo(ser);
        return NULL; //free info, return NULL if connecting does not work
    }

    char request[128]; //connection request
    snprintf(request, sizeof(request), "goff0074:%s", matrix_name); //format the message
    if (write(sockfd, request, strlen(request)) != strlen(request)) {
        close(sockfd);
        freeaddrinfo(ser);
        return NULL; //If the request writing does not work, close the socket, free the addr info, and return NULL
    }

    unsigned char mat_status_bytes[4]; //status bytes
    if (read(sockfd, mat_status_bytes, 4) != 4) {
        close(sockfd);
        freeaddrinfo(ser);
        return NULL; //if the status read does not work
    }
    int32_t status = (mat_status_bytes[3]) | (mat_status_bytes[2] << 8) | (mat_status_bytes[1] << 16) | (mat_status_bytes[0] << 24); //convert status from big -> little endian
    if (status != 0) {
        close(sockfd);
        freeaddrinfo(ser);
        return NULL;  //if the status is not 0
    }
    
    unsigned char dimensions[8]; //dimensions of matrix
    if (read(sockfd, dimensions, 8) != 8) {
        close(sockfd);
        freeaddrinfo(ser);
        return NULL; //if the read is unsuccesful
    }
    int32_t mat_rows = (dimensions[3]) | (dimensions[2] << 8) | (dimensions[1] << 16) | (dimensions[0] << 24); //convert row value from big to little endian
    int32_t mat_cols = (dimensions[7]) | (dimensions[6] << 8) | (dimensions[5] << 16) | (dimensions[4] << 24); //convert column value from big to little endian
    if (mat_rows <= 0 || mat_cols <= 0) {
        close(sockfd);
        freeaddrinfo(ser);
        return NULL; //Check to see if the rows and columns are above 0
    }
    
    mat = matrix_init(mat_rows, mat_cols); //initialize a matrix with those rows and columns
    if (mat == NULL) {
        close(sockfd);
        freeaddrinfo(ser);
        return NULL; // check if matrix is NULL
    }

    unsigned char mat_value_bytes[4]; //matrix index value
    for (int i = 0; i < mat -> nrows; i++) {
        for (int j = 0; j < mat -> ncols; j++) { //loop through rows and columns of matrix
            if (read(sockfd, mat_value_bytes, 4) != 4) { //read a single value from the matrix obtained
                matrix_free(mat);
                close(sockfd);
                freeaddrinfo(ser);
                return NULL; //if the read does not work
            }
            int32_t mat_value = (mat_value_bytes[3]) | (mat_value_bytes[2] << 8) | (mat_value_bytes[1] << 16) | (mat_value_bytes[0] << 24); //convert matrix value from big to little endian
            matrix_put(mat, i, j, mat_value); //put the matrix value in the matrix
        }
    }
    close(sockfd); //close socket
    freeaddrinfo(ser); //free address info
    return mat; //return matrix
}

