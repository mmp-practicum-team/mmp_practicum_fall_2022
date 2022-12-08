#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time

import ctypes
import platform

import numpy as np

# Загрузка библиотеки

shared_lib_suffix = 'dll' if platform.system() == 'Windows' else 'so'
testcpp = ctypes.CDLL(f'./bin/liblibctypespython.{shared_lib_suffix}')


# Указываем, что функция возвращает void *
testcpp.test_new.restype = ctypes.c_void_p
# Указываем, что функция принимает аргумент int, char, double
testcpp.test_new.argtypes = [ctypes.c_int, ctypes.c_char, ctypes.c_double]

# Создание класса test
test = testcpp.test_new(10, 'C'.encode('utf-8'), 713.0)

##
# Работа с переменными
##

# Указываем, что функция возвращает int
testcpp.test_get_a.restype = ctypes.c_int
# Указываем, что функция принимает аргумент void *
testcpp.test_get_a.argtypes = [ctypes.c_void_p]

# Указываем, что функция возвращает double
testcpp.test_get_b.restype = ctypes.c_char
# Указываем, что функция принимает аргумент void *
testcpp.test_get_b.argtypes = [ctypes.c_void_p]

# Указываем, что функция возвращает char
testcpp.test_get_c.restype = ctypes.c_double
# Указываем, что функция принимает аргумент void *
testcpp.test_get_c.argtypes = [ctypes.c_void_p]

print('\nРабота с переменными:')
print('ret test_get_a: ', testcpp.test_get_a(test)); sys.stdout.flush()
print('ret test_get_b: ', testcpp.test_get_b(test).decode("utf-8")); sys.stdout.flush()
print('ret test_get_c: ', testcpp.test_get_c(test)); sys.stdout.flush()

print(); sys.stdout.flush()

##
# Работа с вектором
##

# Указываем, что функция возвращает void *
testcpp.test_get_vector.restype = ctypes.c_void_p
# Указываем, что функция принимает аргумент void *
testcpp.test_get_vector.argtypes = [ctypes.c_void_p]

# Указываем, что функция возвращает double
testcpp.test_vector_index.restype = ctypes.c_double
# Указываем, что функция принимает аргумент void *, unsigned long long
testcpp.test_vector_index.argtypes = [ctypes.c_void_p, ctypes.c_ulonglong]

# Указываем, что функция принимает аргумент void *, double
testcpp.test_vector_push_back.argtypes = [ctypes.c_void_p, ctypes.c_double]

# Указываем, что функция принимает аргумент void *
testcpp.test_vector_print.argtypes = [ctypes.c_void_p]

vector = testcpp.test_get_vector(test)
testcpp.test_vector_push_back(vector, 1.5)
testcpp.test_vector_push_back(vector, 2.5)
testcpp.test_vector_push_back(vector, 3.5)
testcpp.test_vector_print(vector)
print('vector[0]: {0:.3f}, vector[1]: {1:.3f}, vector[2]: {2:.3f}'.format(
    testcpp.test_vector_index(vector, 0), testcpp.test_vector_index(vector, 1), testcpp.test_vector_index(vector, 2)
)); sys.stdout.flush()
vector_one_more = testcpp.test_get_vector(test)
testcpp.test_vector_print(vector_one_more)
testcpp.test_vector_push_back(vector, -1.5)
testcpp.test_vector_print(vector)
print('vector[3]: {0:.3f}, vector_one_more[3]: {1:.3f}'.format(
    testcpp.test_vector_index(vector, 3), testcpp.test_vector_index(vector_one_more, 3)
)); sys.stdout.flush()

##
# Работа с методами
##

# Указываем, что функция возвращает char *
testcpp.test_is_prime.restype = ctypes.c_bool
# Указываем, что функция принимает аргумент void * и char *
testcpp.test_is_prime.argtypes = [ctypes.c_void_p, ctypes.c_int]

# Указываем, что функция возвращает int
testcpp.test_is_palindrome.restype = ctypes.c_bool
# Указываем, что функция принимает аргумент void * и int
testcpp.test_is_palindrome.argtypes = [ctypes.c_void_p, ctypes.c_char_p]

print('Работа с методами:'); sys.stdout.flush()
# В качестве 1-ого аргумента передаем указатель на наш класс
print('ret test_is_prime: {0}'.format(testcpp.test_is_prime(test, 317))); sys.stdout.flush()
print('ret test_is_palindrome: {0}'.format(testcpp.test_is_palindrome(test, 'nolemon,nomelon'.encode('utf-8')))); sys.stdout.flush()


# Указываем, что функция принимает аргумент void *
testcpp.test_del.argtypes = [ctypes.c_void_p]

# Удаляем класс
testcpp.test_del(test)

print(); sys.stdout.flush()

##
# IO операции
##
#
# Указываем, что функция возвращает int
testcpp.test_read_file.restype = ctypes.POINTER(ctypes.c_int)
# Указываем, что функция принимает аргумент char * и unsigned long long
testcpp.test_read_file.argtypes = [ctypes.c_char_p, ctypes.c_ulonglong]

# Указываем, что функция принимает аргумент int *
testcpp.test_int_array_delete.argtypes = [ctypes.POINTER(ctypes.c_int)]

start_cpp_read = time.time()
data_ptr = testcpp.test_read_file('data.txt'.encode('utf-8'), 10_000_000)
array_from_data = np.ctypeslib.as_array(data_ptr, shape=[10_000, 1_000])
print('Verify last value: {0}'.format(array_from_data[-1, -1]))
total_time_cpp_read = time.time() - start_cpp_read

testcpp.test_int_array_delete(data_ptr)


start_python_read = time.time()
array = np.empty([10_000, 1_000], dtype=np.int)

with open('data.txt', 'r') as file:
    for idx, line in enumerate(file):
        for jdx, value in enumerate(line.strip().split(' ')):
            array[idx, jdx] = int(value)

array_from_file = array.reshape([10_000, 1_000])
print('Verify last value: {0}'.format(array_from_file[-1, -1]))
total_time_python_read = time.time() - start_python_read

print('C function time: {0:.3f}'.format(total_time_cpp_read))
print('Pure Python time: {0:.3f}'.format(total_time_python_read))

##
#   libc
##

libc = ctypes.cdll.msvcrt if platform.system() == 'Windows' else ctypes.CDLL("libc.so.6")

libc.printf('Hello World!, %s\n'.encode('utf-8'), 'Maksim'.encode('utf-8'))
libc.fflush(None)

int_val = ctypes.c_int()
float_val = ctypes.c_float()
str_val = ctypes.create_string_buffer(1024)
libc.scanf('%d-%f-%s'.encode('utf-8'), ctypes.byref(int_val), ctypes.byref(float_val), str_val)
print(int_val, float_val, str_val.value.decode('utf-8')); sys.stdout.flush()

print(); sys.stdout.flush()

##
#   Callback functions
##


def simple_comparator(a, b):
    return int(a > b)


def advanced_comparator(a, b):
    return a[0] - b[0]


simple_comparator_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int)
advanced_comparator_type = ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

# Указываем, что функция принимает аргумент char * и unsigned long long
testcpp.test_sort.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_ulonglong, simple_comparator_type]

array = np.random.randint(0, 100, size=[15])
print("Before sorting: ", array); sys.stdout.flush()
testcpp.test_sort(
    array.ctypes.data_as(ctypes.POINTER(ctypes.c_int)), 15, simple_comparator_type(simple_comparator)
)
print("After sorting (std::sort): ", array); sys.stdout.flush()

array = np.random.randint(0, 100, size=[15])
print("Before sorting: ", array); sys.stdout.flush()
libc.qsort(
    array.ctypes.data_as(ctypes.POINTER(ctypes.c_int)), 15,
    ctypes.sizeof(ctypes.c_int), advanced_comparator_type(advanced_comparator)
)
print("After sorting (libc qsort): ", array); sys.stdout.flush()
