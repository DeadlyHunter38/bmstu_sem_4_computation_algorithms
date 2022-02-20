#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "../inc/multiply_interpolation.h"
#include "../inc/defines.h"
#include "../inc/struct.h"
#include "../inc/process_matrix.h"

void get_nodes(double *list_values, int degree, int table_size, double arg, int *index_low,
               int *index_high);
int find_index_near(double *x, int table_size, double arg);
void choose_need_table_place(double **table, double ***need_table, int index_low_x, int index_high_x,
                            int index_low_y, int index_high_y);
void get_f_values(double **f_received_values, double **need_table, double *x, double arg_x,
                  int nx, int ny, int index_low, int index_high);
double interpolate_newton(double *x, double *y, double *matrix, int degree, double arg,
                          int index_low, int index_high);
void fill_newton_splitted_difference(double *matrix, int index_low, int index_high, 
                              double step, int degree);


double do_multiply_interpolation(matrix_t **table)
{
    int index_low_x = 0, index_low_y = 0,
        index_high_x = 0, index_high_y = 0;
    double result = 0;
    
    get_nodes((*table)->x, (*table)->nx, (*table)->column, (*table)->arg_x, &index_low_x, &index_high_x);
    get_nodes((*table)->y, (*table)->ny, (*table)->row, (*table)->arg_y, &index_low_y, &index_high_y);

    double **need_table = NULL;
    choose_need_table_place((*table)->matrix, &need_table, index_low_x, index_high_x,
                            index_low_y, index_high_y);
    if (need_table != NULL)
    {
        double *f_received_values = NULL;
        get_f_values(&f_received_values, need_table, (*table)->x, (*table)->arg_x,
                     (*table)->nx, (*table)->ny, index_low_x, index_high_x);
        if (f_received_values != NULL)
        {
            double diff_matrix[15] = { 0 };
            result = interpolate_newton((*table)->y, f_received_values, diff_matrix, (*table)->ny, 
                               (*table)->arg_y, index_low_y, index_high_y);
        }
        free(f_received_values);
    }
    free(need_table);
    
    return result;
}

void get_nodes(double *list_values, int degree, int table_size, double arg, int *index_low,
               int *index_high)
{
    //найти ближайшую точку
    int index_near = 0;
    index_near = find_index_near(list_values, table_size, arg);

    int need_space = degree / 2;

    if (index_near + need_space + 1 > table_size) //если не хватает снизу узлов
    {
        *index_low = table_size - 1 - degree;
        *index_high = table_size - 1;
    }
    else if (index_near < need_space) //если не хватает узлов сверху
    {
        *index_low = 0;
        *index_high = *index_low + degree;
    }
    else
    {
        *index_low = index_near - need_space;
        *index_high = *index_low + degree;
    }      
}

int find_index_near(double *x, int table_size, double arg)
{
    int index_near = 0;
    double min_diff = fabs(x[0] - arg);

    for (int i = 1; i < table_size; i++)
    {
        if (fabs(x[i] - arg) < min_diff && fabs(fabs(x[i] - arg) - min_diff) >= EPS)
        {
            index_near = i;
            min_diff = fabs(x[i] - arg);
        }
    }

    return index_near;
}

void choose_need_table_place(double **table, double ***need_table, int index_low_x, int index_high_x,
                            int index_low_y, int index_high_y)
{
    *need_table = allocate_matrix(index_high_y - index_low_y + 1, index_high_x - index_low_x + 1);
    if (*need_table != NULL)
    {
        for (int i = index_low_y, k = 0; i <= index_high_y; i++, k++)
            for (int j = index_low_x, l = 0; j <= index_high_x; j++, l++)
                (*need_table)[k][l] = table[i][j];
    }
}

void get_f_values(double **f_received_values, double **need_table, double *x, double arg_x,
                  int nx, int ny, int index_low, int index_high)
{
    *f_received_values = malloc((ny + 1) * sizeof(double));
    if (f_received_values != NULL)
    {
        double diff_matrix[15] = { 0 };
        for (int i = 0; i < ny + 1; i++)
        {
            (*f_received_values)[i] = interpolate_newton(x, need_table[i], diff_matrix, nx, arg_x,
                        index_low, index_high);
            printf("(*f_received_values)[i] = %lf\n", (*f_received_values)[i]);
        }
    }
}

double interpolate_newton(double *x, double *y, double *matrix, int degree, double arg,
                          int index_low, int index_high)
{
    double result = 0, temp = 1;

    for (int i = 0, j = 0; i <= index_high - index_low; i++, j++)
        matrix[j] = y[i];

    fill_newton_splitted_difference(matrix, index_low, index_high, x[1] - x[0], degree);

    for (int i = 0, k = 0, p = degree + 1; i <= degree; i++, k += p, p--)
    {
        result += matrix[k] * temp;
        temp *= (arg - x[index_low + i]);
    }

    return result;
}

void fill_newton_splitted_difference(double *matrix, int index_low, int index_high, 
                              double step, int degree)
{
    int k = 1, koeff = 1, p = 0, shift = 1;
    for (int i = index_high - index_low; i > 0; i--)
    {
        for (int j = 0; j < i; j++)
        {
            matrix[degree + p + 1] = (matrix[shift] - matrix[shift - 1]) / (step * koeff);
            shift++, p++;
        }
        koeff++, k++, shift++;
    }
}
