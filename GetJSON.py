from Languages import GetLanguages
from ImportsAndNames import GetImports
from ImportsAndNames import GetNames
from ImportsAndNames import Utils
from threading import Thread
import json
import os
import subprocess
import time


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self):
        self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        Thread.join(self, *args)
        if self._return is None:
            raise Exception("This function hasn't return value")
        return self._return


def get_json(path: str, as_url: bool = False):
    """
    :param path: 1) path to file ( ~ doesn't work with os ) or 2) url to github repository
    :param as_url: False (default) - path is treated as 1), True - path is treated as 2)
    :return: json dump
    """
    if as_url:
        if not os.path.exists('repos'):
            os.mkdir('repos')
        cmd = "(cd repos && git clone " + path + ")"
        p = subprocess.Popen(cmd, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for line in p.stdout.readlines():
            print(line)
        path = path.split("/")[-1]
        if path.endswith(".git"):
            path = path[:-4]
        path = os.path.abspath(os.getcwd()) + "/repos/" + path

    if not os.path.exists(path):
        raise FileNotFoundError("Incorrect path")
        
    repo_name = path.split("/")[-1]

    lang_thread = ThreadWithReturnValue(target=GetLanguages.get_languages, args=(path, 20,))
    import_thread = ThreadWithReturnValue(target=GetImports.get_imports, args=(path,))
    name_thread = ThreadWithReturnValue(target=GetNames.get_names, args=(path,))

    lang_thread.start()
    import_thread.start()
    name_thread.start()

    stats = lang_thread.join()
    imports = import_thread.join()
    names = name_thread.join()
    # stats = GetLanguages.get_languages(path, 20)
    # imports = GetImports.get_imports(path)
    # names = GetNames.get_names(path)

    if as_url:
        Utils.remove_dir(os.path.abspath(os.getcwd()) + "/repos/")

    languages = []
    percentages = []
    for percentage, language in stats:
        percentages.append(percentage.strip("%"))
        languages.append(language)

    # with open(repo_name + ".json", 'w') as f:
    # json.dump({"repo_name:": repo_name, "languages": languages, "percentages": percentages, "imports": list(imports)}, f)

    return json.dumps(
        {"repo_name:": repo_name, "languages": languages, "percentages": percentages, "imports": list(imports),
         "names": list(names)})


start_time = time.time()
print(get_json("https://github.com/dkshtakin/buckwheat.git", True))
print("--- %s seconds ---" % (time.time() - start_time))
