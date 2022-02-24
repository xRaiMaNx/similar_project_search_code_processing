from . import Types

from preprocess.mappers.files.base import compose_base_extractors, build_pygments_extractors_from_spec
from preprocess.mappers.files.tree_sitter import build_ts_extractors_from_spec
from preprocess.sources import FolderSource


def get_docstrings(path: str):
    """
    :param path: the path of the project to get all docstrings
    :return: list of docstrings
    """

    comments_extractor = compose_base_extractors([
        *build_pygments_extractors_from_spec(Types.COMMENTS_PYGMENTS),
        *build_ts_extractors_from_spec(Types.COMMENTS_TREE_SITTER),
    ])

    comments_entities = (
        FolderSource(path)
        .files_chain
        .flat_map(comments_extractor)
        .elements()
    )

    docstrings = []
    for comment_entity in comments_entities:
        docstrings.append(comment_entity.body)
    return docstrings
