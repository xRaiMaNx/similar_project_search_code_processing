from . import Types
from cytoolz import groupby
from typing import Iterator, Tuple

from preprocess.mappers.files.tree_sitter import build_ts_tree_extractor
from preprocess.sources import FolderSource
from preprocess.extractors.tree_sitter import TreeEntity


def traverse_tree(entity: TreeEntity, level: int = 0) -> Iterator[Tuple[int, TreeEntity]]:
    """Yield tree structure with depth level"""
    yield level, entity
    for child in entity.children:
        yield from traverse_tree(child, level + 1)


def get_imports(path: str):
    """
    :param path: the path of the project to get all imports
    :return: list of imports
    """

    imports_extractor = build_ts_tree_extractor(Types.IMPORTS_TREE_SITTER)

    imports_entities = (
        FolderSource(path)
        .files_chain
        .flat_map(imports_extractor)
        .elements()
    )

    imports = []

    for tree_identifier in imports_entities:
        tree_nodes_by_depth = groupby(lambda i: i[0], traverse_tree(tree_identifier))
        treeEntity = sorted(tree_nodes_by_depth.items())[0][1][0][1]
        libs = []
        for _, identifiers in sorted(tree_nodes_by_depth.items()):
            decoded = [treeEntity.file.code_bytes[i[1].start_byte: i[1].end_byte].decode()
                       for i in identifiers if i[1].type == "identifier"]
            if decoded:
                libs += decoded
        imports.append(' '.join(libs))

    return imports
