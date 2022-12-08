//
// Created by nahod on 09.12.2019.
//

#ifndef CTYPES_TEST_PUREC_H
#define CTYPES_TEST_PUREC_H

#include <stdio.h>
#include <stdlib.h>

typedef struct test_st_t test_st_t;

int func_ret_int(int val);

double func_ret_double(double val);

char *func_ret_str(char *val);

char func_many_args(int val1, double val2, char val3, short val4);

void func_print_globals();

double func_struct(test_st_t test_st);

double * func_add_out(const double * left, const double * right, double * result);

void func_add_arrays_out(const double * left, const double * right, double * result, unsigned long long n);

struct test_st_t {
    int val1;
    double val2;
    char val3;
    int * array;
};

double * replace_zeros_to_means(double *X, unsigned long long n, unsigned long long m);

void free_double(double *ptr);

#endif //CTYPES_TEST_PUREC_H
