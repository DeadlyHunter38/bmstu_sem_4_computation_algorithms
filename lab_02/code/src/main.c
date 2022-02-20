#include <stdio.h>
#include "../inc/defines.h"
#include "../inc/struct.h"
#include "../inc/read.h"
#include "../inc/process_matrix.h"
#include "../inc/multiply_interpolation.h"

int main(int argc, char **argv)
{
    int code_error = ERR_OK;
    if (argc != 2)
    {
        printf("Ошибка. Некорректное количество переданных аргументов.\n");
        code_error = ERR_NOT_ENOUGH_ARGS;
    }
    else
    {
        matrix_t *table = NULL;
        if (read_data(argv[1], &table) == ERR_OK)
        {
            double result = 0;
            result = do_multiply_interpolation(&table);
            printf("Результат интерполяции: %lf\n", result);
        }

        free_table(&table);
    }
    return code_error;
}