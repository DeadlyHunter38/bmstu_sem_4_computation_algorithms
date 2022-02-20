#include <stdio.h>
#include <stdlib.h>
#include "../inc/process_matrix.h"
#include "../inc/struct.h"

double **allocate_matrix(int row, int column)
{
    double **table = NULL;
    table = malloc(row * sizeof(double*) + row * column * sizeof(double));
    if (table != NULL)
    {
        for (int i = 0; i < row; i++)
        {
            table[i] = (double*)((char*)table + row * sizeof(int*) + i * column * sizeof(double));
        }
    }

    return table;
}

void free_table(matrix_t **table)
{
    free((*table)->matrix);
    free((*table)->x);
    free((*table)->y);
    free(*table);
}

void print_matrix(double **matrix, int row, int column)
{
    for (int i = 0; i < row; i++)
    {
        for (int j = 0; j < column; j++)
            printf("%lf ", matrix[i][j]);
        printf("\n");
    }
}