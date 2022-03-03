from . import Tokens
from typing import List

from preprocess.mappers.files.base import compose_base_extractors, build_pygments_extractors_from_spec
from .CustomSource import CustomSource


def get_docstrings(path: str) -> List[str]:
    """
    :param path: the path of the project to get all docstrings
    :return: list of docstrings
    """

    docstrings_extractor = compose_base_extractors([
        *build_pygments_extractors_from_spec(Tokens.DOCSTRINGS_PYGMENTS),
    ])

    docstring_entities = (
        CustomSource(path)
        .files_chain
        .flat_map(docstrings_extractor)
        .elements()
    )

    docstrings = []
    for docstring_entity in docstring_entities:
        docstrings.append(docstring_entity.body)
    return docstrings
