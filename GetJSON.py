from Languages import GetLanguages
from Imports import GetImports
import os
import json


def get_json(path: str):
    """
    :param path: path to file ( ~ doesn't work with os )
    :return: json dump
    """
    if not os.path.exists(path):
        raise FileNotFoundError("Incorrect path")

    stats = GetLanguages.get_languages(path, 20)

    imports = GetImports.get_imports(path)

    languages = []
    percentages = []
    for percentage, language in stats:
        percentages.append(percentage)
        languages.append(language)
    return json.dumps({"languages": languages, "percentages": percentages, "imports": list(imports)})
