from . import Utils
import os


def get_imports(path: str):
    """
    :param path: the path of the project to get all imports in all programs
    :return: set of imports in project
    """
    cmd = "echo " + path + " > ImportsAndNames/path.txt"
    os.system(cmd)
    cmd = "cd ImportsAndNames/buckwheat && python3 -m buckwheat.run --local -i ../path.txt -o ../ -g imports"
    os.system(cmd)
    imports = set()
    Utils.remove_file("ImportsAndNames/path.txt")
    with open('ImportsAndNames/wabbit_sequences_imports_0.txt', 'r', encoding='utf-8') as r:
        for line in r:
            imports.add(line.strip())
    Utils.remove_file("ImportsAndNames/wabbit_sequences_imports_0.txt")
    return imports
