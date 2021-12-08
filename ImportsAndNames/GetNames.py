from . import Utils
import os


def get_names(path: str):
    """
    :param path: the path of the project to get all names in all programs
    :return: set of names in project
    """
    cmd = "echo " + path + " > ImportsAndNames/path.txt"
    os.system(cmd)
    cmd = "cd ImportsAndNames/buckwheat && python3 -m buckwheat.run --local -i ../path.txt -o ../ -g names"
    os.system(cmd)
    names = set()
    Utils.remove_file("ImportsAndNames/path.txt")
    with open('ImportsAndNames/wabbit_sequences_names_0.txt', 'r', encoding='utf-8') as r:
        for line in r:
            for i in line.strip().split():
                names.add(i)
    Utils.remove_file("ImportsAndNames/wabbit_sequences_names_0.txt")
    return names
