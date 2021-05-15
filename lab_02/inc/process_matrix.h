#ifndef _PROCESS_MATRIX_H_
#define _PROCESS_MATRIX_H_

#include "../inc/struct.h"

double **allocate_matrix(int row, int column);
void free_table(matrix_t **table);
void print_matrix(double **matrix, int row, int column);

#endif
