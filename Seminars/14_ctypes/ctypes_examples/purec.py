#!/usr/bin/python3
# -*- coding: utf-8 -*-

import ctypes
import platform
import sys

import time
import numpy as np
from array import array

# Загрузка библиотеки

shared_lib_suffix = 'dll' if platform.system() == 'Windows' else 'so'
test = ctypes.CDLL(f'./bin/liblibctypespython.{shared_lib_suffix}')

##
# Работа с функциями
##

# All Python types except INTEGERS, STRINGS, and BYTES objects have to be wrapped in their
#   corresponding ctypes type, so that they can be converted to the required C data type


# Указываем, что функция возвращает int
test.func_ret_int.restype = ctypes.c_int
# Указываем, что функция принимает аргумент int
test.func_ret_int.argtypes = [ctypes.c_int]

# Указываем, что функция возвращает double
test.func_ret_double.restype = ctypes.c_double
# Указываем, что функция принимает аргумент double
test.func_ret_double.argtypes = [ctypes.c_double]

# Указываем, что функция возвращает char *
# ctypes.c_char_p -- указатель нуль-терминированных строк
test.func_ret_str.restype = ctypes.c_char_p
# Указываем, что функция принимает аргумент char *
# ctypes.POINTER -- произвольный указатель
test.func_ret_str.argtypes = [ctypes.POINTER(ctypes.c_char)]

# Указываем, что функция возвращает char
test.func_many_args.restype = ctypes.c_char
# Указываем, что функция принимает аргументы int, double, char, short
test.func_many_args.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_char, ctypes.c_short]


print('ret func_ret_int: ', test.func_ret_int(101)); sys.stdout.flush()
print('ret func_ret_double: ', test.func_ret_double(12.123456789)); sys.stdout.flush()

# Необходимо строку привести к массиву байтов, затем полученный массив байтов приводим к строке.
print('ret func_ret_str: ', test.func_ret_str('Hello!'.encode('utf-8')).decode('utf-8')); sys.stdout.flush()

print('ret func_many_args: ', test.func_many_args(15, 18.1617, 'X'.encode('utf-8'), 32000).decode('utf-8')); sys.stdout.flush()

print(); sys.stdout.flush()

##
# Работа с переменными
##

# Указываем, что переменная типа int
a = ctypes.c_int.in_dll(test, 'a')
print('ret a: ', a.value); sys.stdout.flush()

# Изменяем значение переменной.
a.value = 22
a = ctypes.c_int.in_dll(test, 'a')
print('ret a: ', a.value); sys.stdout.flush()

# Указываем, что переменная типа double
b = ctypes.c_double.in_dll(test, 'b')
print('ret b: ', b.value); sys.stdout.flush()

# Указываем, что переменная типа char
c = ctypes.c_char.in_dll(test, 'c')
print('ret c: ', c.value.decode('utf-8')); sys.stdout.flush()

a.value = 317
b.value = 0.317
c.value = 'B'.encode('utf-8')
test.func_print_globals()

print(); sys.stdout.flush()

##
# Работа со структурами
##


# Дублируюем структуру из C в Python
class TestST(ctypes.Structure):
    _fields_ = [('val1', ctypes.c_int),
                ('val2', ctypes.c_double),
                ('val3', ctypes.c_char)]

    def __str__(self):
        return f'val1 - {self.val1}, val2 - {self.val2}, val3 - {self.val3.decode("utf8")}'


# Передаём по значению:

# Указываем, что функция возвращает double
test.func_struct.restype = ctypes.c_double
# Указываем, что функция принимает аргумент TestST
test.func_struct.argtypes = [TestST]

# Создаем структуру
test_st = TestST(19, 3.5, 'Z'.encode('utf-8'))
ret = test.func_struct(test_st)
print(f'ret func_struct: {ret}'); sys.stdout.flush()

# Передаём по указателю:

# Указываем, что функция возвращает TestST *
test.func_ret_struct.restype = ctypes.POINTER(TestST)
# Указываем, что функция принимает аргумент TestST *
test.func_ret_struct.argtypes = [ctypes.POINTER(TestST)]

# Python None == Null C
ret = test.func_ret_struct(None)
if ret:
    print(f'ret func_ret_struct: {ret.contents}'); sys.stdout.flush()
else:
    print('ret func_ret_struct: null pointer'); sys.stdout.flush()

ret = test.func_ret_struct(test_st)
if ret:
    print(f'ret func_ret_struct: {ret.contents}'); sys.stdout.flush()
else:
    print('ret func_ret_struct: null pointer'); sys.stdout.flush()

print()

##
# Работа с указателями
##

# Указываем, что функция возвращает double *
test.func_add_out.restype = ctypes.POINTER(ctypes.c_double)
# Указываем, что функция принимает аргумент double *, double *, double *
test.func_add_out.argtypes = [
    ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double)
]

left, right, result = ctypes.c_double(300.0), ctypes.c_double(17.0), ctypes.c_double()
print(left, right, result); sys.stdout.flush()
res = test.func_add_out(ctypes.byref(left), right, result)
print(left, right, result, res.contents); sys.stdout.flush()
res.contents.value = 100500.0
print(left, right, result, res.contents); sys.stdout.flush()

print(); sys.stdout.flush()

##
# Работа с массивами
##

test.func_add_arrays_out.restype = ctypes.POINTER(ctypes.c_double)
test.func_add_arrays_out.argtypes = [
    ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double),
    ctypes.POINTER(ctypes.c_double), ctypes.c_ulonglong
]

# Эквивалентно int array[10]. Т.е. эта конструкция -- новый класс
double_array_10 = ctypes.c_double * 10

# 1 Способ: создание internal массива из списка (медленно)
left_array = double_array_10(*[i for i in range(10)])
right_array = double_array_10(*[2.0 * i for i in range(10)])
result_array = double_array_10()

test.func_add_arrays_out(left_array, right_array, result_array, 10)
print(result_array[:]); sys.stdout.flush()

# 2 Способ: создание internal массива из underlying memory в array (быстро)
left_array = double_array_10.from_buffer(array('d', (i for i in range(10))))
right_array = double_array_10.from_buffer(array('d', (2.0 * i for i in range(10))))
result_array = double_array_10.from_buffer(array('d', (0.0 for i in range(10))))

test.func_add_arrays_out(left_array, right_array, result_array, 10)
print(result_array[:]); sys.stdout.flush()

# 3 Способ: создание internal массива из прямой конвертацией указателя в C указатель (ещё быстрее)
left_array = array('d', (i for i in range(10)))
right_array = array('d', (2.0 * i for i in range(10)))
result_array = array('d', (0.0 for i in range(10)))

test.func_add_arrays_out(
    ctypes.cast(left_array.buffer_info()[0], ctypes.POINTER(ctypes.c_double)),
    ctypes.cast(right_array.buffer_info()[0], ctypes.POINTER(ctypes.c_double)),
    ctypes.cast(result_array.buffer_info()[0], ctypes.POINTER(ctypes.c_double)),
    10
)

print(result_array); sys.stdout.flush()

# 4 Способ: numpy
left_array = np.array([2.0 * i for i in range(10)], dtype=np.double)
right_array = np.array([i for i in range(10)], dtype=np.double)
result_array = np.array([0.0 for i in range(10)], dtype=np.double)

test.func_add_arrays_out(
    left_array.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
    right_array.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
    result_array.ctypes.data_as(ctypes.POINTER(ctypes.c_double)),
    10
)

print(result_array); sys.stdout.flush()

print(); sys.stdout.flush()

##
# Замеры скорости
##

n = 10_000_000

# Numpy
left_numpy = np.array([1.0 * i for i in range(n)], dtype=np.double)
right_numpy = np.array([2.0 * i for i in range(n)], dtype=np.double)
result_numpy = np.empty([n], dtype=np.double)

start_numpy = time.time()
result_numpy = left_numpy + right_numpy
total_time_numpy = time.time() - start_numpy

# Python lists
left_lists = [1.0 * i for i in range(n)]
right_lists = [2.0 * i for i in range(n)]

start_lists = time.time()
result_lists = [i + j for (i, j) in zip(left_lists, right_lists)]
total_time_lists = time.time() - start_lists

# C function + lists
double_array_n = ctypes.c_double * n

left_c_lists = double_array_n(*[i for i in range(n)])
right_c_lists = double_array_n(*[2.0 * i for i in range(n)])
result_c_lists = double_array_n()

start_c_lists = time.time()
test.func_add_arrays_out(left_c_lists, right_c_lists, result_c_lists, n)
total_c_lists = time.time() - start_c_lists


print('Numpy time: {0:.3f}'.format(total_time_numpy)); sys.stdout.flush()
print('Pure Python time: {0:.3f}'.format(total_time_lists)); sys.stdout.flush()
print('C function (with lists) time: {0:.3f}'.format(total_c_lists)); sys.stdout.flush()
