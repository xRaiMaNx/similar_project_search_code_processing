from CodeData import Utils
from LanguagesAndReadme import GetLanguagesAndReadme
from CodeData import GetImports
from CodeData import GetIdentifiers
from CodeData import GetDocstrings
import json
import os


DEFAULT_GIT_INFO = {'stargazers_count': '0', 'commit_sha': '0', 'repo_id': '0'}


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

    [stats, readme] = GetLanguagesAndReadme.get_languages_and_readme(path, 20)
    imports = GetImports.get_imports(path)
    identifiers, splitted_identifiers = GetIdentifiers.get_identifiers(path)
    docstrings = GetDocstrings.get_docstrings(path)

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
