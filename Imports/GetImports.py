import os


def remove_file(path: str):
    """
    must be used for removing path.txt and wabbit_sequences_imports_0.txt
    :param path: path of file which should be removed
    """
    if os.path.exists(path):
        #p = os.path.join(os.path.abspath(os.path.dirname(__file__)), path)
        os.remove(path)


def get_imports(path: str):
    """
    :param path: the path of the project to get all imports in all programs
    :return: set of imports in project
    """
    cmd = "echo " + path + " > Imports/path.txt"
    os.system(cmd)
    cmd = "cd Imports/buckwheat && python3 -m buckwheat.run --local -i ../path.txt -o ../ -g imports"
    os.system(cmd)
    imports = set()
    with open('Imports/wabbit_sequences_imports_0.txt', 'r', encoding='utf-8') as r:
        for line in r:
            imports.add(line.strip())
    remove_file("Imports/path.txt")
    remove_file("Imports/wabbit_sequences_imports_0.txt")
    return imports
