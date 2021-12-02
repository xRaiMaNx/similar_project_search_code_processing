from Languages import GetLanguages
from ImportsAndNames import GetImports
from ImportsAndNames import GetNames
import os
import json


def get_json(path: str):
    """
    :param path: path to file ( ~ doesn't work with os )
    :return: json dump
    """
    if not os.path.exists(path):
        raise FileNotFoundError("Incorrect path")

    repo_name = path.split("/")[-1]

    stats = GetLanguages.get_languages(path, 20)

    imports = GetImports.get_imports(path)

    names = GetNames.get_names(path)

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
