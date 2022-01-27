from . import Utils
import os


def get_docstrings(path: str, repo_name: str):
    """
    :param path: the path of the project to get all imports in all programs
    :return: set of imports in project
    """
    cur_path = os.path.abspath(os.getcwd()) + "/CodeData"
    path_filename = repo_name + "_path.txt"
    cmd = "echo " + path + " > " + cur_path + "/" + path_filename
    os.system(cmd)
    cmd = "cd " + cur_path + "/buckwheat && python3 -m buckwheat.run "\
          "--local -i ../" + path_filename + " -o ../ -g docstrings -rn " + repo_name +\
          "> /dev/null"
    os.system(cmd)
    docstrings = set()
    Utils.remove_file(cur_path + "/" + path_filename)
    filename = cur_path + "/" + repo_name + "_wabbit_sequences_docstrings_0.txt"
    with open(filename, 'r', encoding='utf-8') as r:
        is_new_el = False
        new_el = ""
        for line in r:
            if line.strip() == '"""':
                if is_new_el:
                    docstrings.add(new_el)
                is_new_el = not is_new_el
                new_el = ""
                continue
            if is_new_el:
                new_el += line
    Utils.remove_file(filename)
    return docstrings
