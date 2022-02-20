#ifndef _STRUCT_H_
#define _STRUCT_H_

typedef struct matrix matrix_t;
struct matrix
{
    double **matrix;
    int row, column;
    double *x, *y;
    int nx, ny;
    double arg_x, arg_y;
};

#endif