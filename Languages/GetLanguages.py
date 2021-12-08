import os
import subprocess


def get_languages(path, k=1):
    """
    :param path: the path of the project to define the main language for
    :param k: desired amount of most popular languages
    :return: list of pairs [rate, language] of no more than k most popular languages
    """
    cur_path = os.path.abspath(os.getcwd()) + "/parse_for_similar_projects/Languages"
    cmd = cur_path + "/enry -prog " + path
    p = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stats = []
    i = 0
    for line in p.stdout.readlines():
        if i >= k:
            break
        stats.append(line.strip().split('\t'))
        i += 1
    return stats
