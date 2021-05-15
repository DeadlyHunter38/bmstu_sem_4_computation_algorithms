#include <stdio.h>
#include <stdlib.h>
#include "../inc/read.h"
#include "../inc/struct.h"
#include "../inc/defines.h"
#include "../inc/process_matrix.h"

void read_powers(int *nx, int *ny);
void read_args(double *x, double *y);
int fill_table_from_file(FILE *file, double ***table, int row, int column);

int read_data(char *file_name, matrix_t **table)
{
    int code_error = ERR_OK;
    FILE *file = fopen(file_name, "r");
    if (file != NULL)
    {
        *table = malloc(sizeof(matrix_t));
        if (fscanf(file, "%d%d", &(*table)->row, &(*table)->column) != 2)
        {
            printf("Неверный размер таблицы.\n");
            code_error = ERR_INCORRECT_SIZE_TABLE;
        }
        else
        {
            (*table)->x = malloc((*table)->row * sizeof(double));
            (*table)->y = malloc((*table)->column * sizeof(double));
            for (int i = 0; i < (*table)->row; i++)
                (*table)->x[i] = i, (*table)->y[i] = i;
            fill_table_from_file(file, &(*table)->matrix, (*table)->row, (*table)->column);            
        }

        if (code_error == ERR_OK)
        {
            read_powers(&(*table)->nx, &(*table)->ny);
            read_args(&(*table)->arg_x, &(*table)->arg_y);
        }
        fclose(file);
    }
    else
        code_error = ERR_NO_FILE;

    return code_error;
}

int fill_table_from_file(FILE *file, double ***table, int row, int column)
{
    int code_error = ERR_OK;
    *table = allocate_matrix(row, column);
    if (table != NULL)
    {
        for (int i = 0; code_error == ERR_OK && i < row; i++)
            for (int j = 0; code_error == ERR_OK && j < column; j++)
                if (fscanf(file, "%lf", &(*table)[i][j]) != 1)
                    code_error = ERR_INCORRECT_ELEM_TABLE;
    }
    print_matrix(*table, row, column);
    return code_error;
}

void read_powers(int *nx, int *ny)
{
    printf("Введите степени апроксимирующих полиномов (nx, ny): ");
    while (scanf("%d%d", nx, ny) != 2)
    {
        fflush(stdin);
        printf("Ошибка: некорректные значения.\n\n");
        printf("Введите степени апроксимирующих полиномов (nx, ny): ");
    }
}

void read_args(double *x, double *y)
{
    printf("Введите аргументы х и у через пробел: ");
    while(scanf("%lf%lf", x, y) != 2)
    {
        fflush(stdin);
        printf("Ошибка: некорректные значения.\n\n");
        printf("Введите аргументы х и у через пробел: ");
    }
}