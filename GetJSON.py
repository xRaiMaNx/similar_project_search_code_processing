from Languages import GetLanguages
from ImportsAndNames import GetImports
from ImportsAndNames import GetNames
from threading import Thread
import os
import json
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


def get_json(path: str):
    """
    :param path: path to file ( ~ doesn't work with os )
    :return: json dump
    """
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
print(get_json("/home/raiman/mlflow"))
print("--- %s seconds ---" % (time.time() - start_time))
