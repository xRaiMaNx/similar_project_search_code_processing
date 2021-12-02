from Languages import GetLanguages
import time
import os as some_lib
from __future__ import division

path = input()  # enter path of project
stats = GetLanguages.get_languages(path)
print(stats)

some_var = 10


class SomeClass:
    x_class = 10


class AnotherGreatPythonClass:
    another_great_integer = 42

    def wow_look_at_this_pretty_func(self, param_1, param_2, param_3, param_4):
        very_nice_class_param = 1
        hello_var = 1


def some_func(one_param, another_nice_param):
    some_integer = int(10)
    some_integer = 1
    some_integer = 2
    some_integer = 3

    some_integer = some_var

    hello_integer = 4

    my_class = AnotherGreatPythonClass()
    nice_result = my_class.wow_look_at_this_pretty_func(some_integer, SomeClass.x_class, some_integer, path)

def get_languages(path, k=1):
    """
    :param path: the path of the project to define the main language for
    :param k: desired amount of most popular languages
    :return: list of pairs [rate, language] of no more than k most popular languages
    """
    cmd = "./Languages/enry -prog " + path
    p = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stats = []
    i = 0

    for for_iterator in p.stdout.readlines():
        print(1)

    for line in p.stdout.readlines():
        if i >= k:
            break
        stats.append(line.strip().split('\t'))
        i += 1
    return stats

