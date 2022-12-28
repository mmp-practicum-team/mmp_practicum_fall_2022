//
// Created by nahod on 10.12.2019.
//

#ifndef CTYPES_TEST_CPP_H
#define CTYPES_TEST_CPP_H

#include <string>
#include <vector>
#include <cstring>
#include <iostream>
#include <algorithm>


class Test {
public:
    Test(int a, char b, double c): a{a}, b{b}, c{c} {};

    static bool is_prime(int val);
    static bool is_palindrome(const std::string& string);
public:
    int a;
    char b;
    double c;

    std::vector<double> vector;
};

typedef int (*comparator_type)(int, int);

extern "C" {

Test * test_new(int a, char b, double c);
void test_del(Test * test);
bool test_is_prime(Test * test, int val);
bool test_is_palindrome(Test * test, char * val);

int test_get_a(Test * test);
char test_get_b(Test * test);
double test_get_c(Test * test);
std::vector<double> * test_get_vector(Test * test);

double test_vector_index(std::vector<double> * vector, unsigned long long idx);
void test_vector_push_back(std::vector<double> * vector, double value);
void test_vector_print(std::vector<double> * vector);

int * test_read_file(const char * path, unsigned long long n);
void test_int_array_delete(const int * array);

void test_sort(int * array, unsigned long long n, comparator_type comparator);

}

#endif //CTYPES_TEST_CPP_H
