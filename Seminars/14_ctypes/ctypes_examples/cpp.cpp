//
// Created by nahod on 10.12.2019.
//

#pragma GCC optimize("O3","unroll-loops","omit-frame-pointer","inline") //  Optimization flags
#pragma GCC option("arch=native","tune=native","no-zero-upper") //  Enable AVX
#pragma GCC target("avx")  //   Enable AVX

#include <fstream>
#include "cpp.hpp"

/*
 * Методы класса
 */
bool Test::is_prime(int val){
    val = std::abs(val);
    if(val <= 2) return true;

    for(int i = 2; i * i <= val; ++i){
        if(val % i == 0) return false;
    }

    return true;
}

bool Test::is_palindrome(const std::string& string){
    for(unsigned long long i = 0; i < string.size(); ++i){
        if(string[i] != string[string.size() - 1 - i]) return false;
    }

    return true;
}

// /*
//  * Обвязка C для методов класса C++
//  */

// Создаем класс test, и получаем указатель на него.
Test * test_new(int a, char b, double c) {
    return new Test(a, b, c);
}

// Удаляем класс test.
void test_del(Test * test) {
    delete test;
}

bool test_is_prime(Test * test, int val){
    return test->is_prime(val);
}

bool test_is_palindrome(Test * test, char * c_ptr){
    std::string string(c_ptr);

    return test->is_palindrome(string);
}

int test_get_a(Test * test){
    return test->a;
}

char test_get_b(Test * test){
    return test->b;
}

double test_get_c(Test * test){
    return test->c;
}

std::vector<double> * test_get_vector(Test * test){
    return &test->vector;
}

double test_vector_index(std::vector<double> * vector, unsigned long long idx){
    return *(vector->begin() + idx);
}

void test_vector_push_back(std::vector<double> * vector, double value){
    vector->push_back(value);
}

void test_vector_print(std::vector<double> * vector){
    std::cout << "Vector contains: ";
    for(auto v : *vector){
        std::cout << v << ' ';
    }
    std::cout << std::endl;
}

int * test_read_file(const char * path, unsigned long long n){
    auto * array = new int[n];
    std::ifstream file(path);
    for(unsigned long long i = 0; i < n; ++i){
        file >> array[i];
    }
    return array;
}

void test_int_array_delete(const int * array){
    delete[] array;
}

void test_sort(int * array, unsigned long long n, comparator_type comparator){
    std::sort(array, array + n, comparator);
}
