from CodeData import Utils
from LanguagesAndReadme import GetLanguagesAndReadme
from CodeData import GetImports
from CodeData import GetIdentifiers
from CodeData import GetDocstrings
from threading import Thread
import json
import os


DEFAULT_GIT_INFO = {'stargazers_count': '0', 'commit_sha': '0', 'repo_id': '0'}


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


def get_json(url: str, git_info: dict = DEFAULT_GIT_INFO):
    """
    :param path: 1) path to file ( ~ doesn't work with os ) or 2) url to github repository
    :param as_url: False (default) - path is treated as 1), True - path is treated as 2)
    :param git_info: Meta info about repository
    :return: json dump
    """

    if url.endswith(".git"):
        url = url[:-4]
    name = url.split("/")[-1].strip('\n')
    owner = url.split("/")[-2]
    repo_name = owner + '_' + name
    path = os.path.abspath(os.getcwd()) + "/repos/" + repo_name

    Utils.download_repo(owner, name, path)

    if not os.path.exists(path):
        raise FileNotFoundError(path, "is incorrect path")

    lang_and_readme_thread = ThreadWithReturnValue(
        target=GetLanguagesAndReadme.get_languages_and_readme, args=(path, 20,))
    import_thread = ThreadWithReturnValue(
        target=GetImports.get_imports, args=(path,))
    identifier_thread = ThreadWithReturnValue(
        target=GetIdentifiers.get_identifiers, args=(path,))
    docstring_thread = ThreadWithReturnValue(
        target=GetDocstrings.get_docstrings, args=(path,))

    lang_and_readme_thread.start()
    import_thread.start()
    identifier_thread.start()
    docstring_thread.start()

    [stats, readme] = lang_and_readme_thread.join()
    imports = import_thread.join()
    identifiers, splitted_identifiers = identifier_thread.join()
    docstrings = docstring_thread.join()

    readme_content = []
    for filename in readme:
        with open(path + "/" + filename, 'r') as file:
            readme_content.append(file.read())

    languages = []
    percentages = []
    for percentage, language in stats:
        percentages.append(percentage.strip("%"))
        languages.append(language)

    Utils.remove_dir(path)

    data = {"owner": owner, "name": name, "readme": readme_content, "languages": languages,
            "percentages": percentages, "imports": imports, "identifiers": identifiers,
            "splitted_identifiers": splitted_identifiers, "docstrings": docstrings}
    data.update(git_info)
    return json.dumps(data)
