from toolz import identity
from preprocess.sources import FolderSource
from preprocess.mappers.files import extract_identifiers_from_file
from collections import Counter


def get_identifiers(path: str):
    """
    :param path: the path of the project to get all identifiers
    :return: set of identifiers in project
    """

    file_identifiers = (
        FolderSource(path)
        .files_chain
        .juxt(identity, extract_identifiers_from_file)
        .filter(lambda tpl: len(tpl[1]))
        .elements()
    )

    identifiers_list = []
    for _, identifiers in file_identifiers:
        identifiers_list += [i.body for i in identifiers]
    return [dict(Counter(identifiers_list)), dict(Counter(j for i in identifiers_list for j in i.split('_')))]
