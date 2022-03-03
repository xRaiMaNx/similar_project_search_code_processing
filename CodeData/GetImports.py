from . import Tokens
from .CustomSource import CustomSource
from cytoolz import groupby
from typing import Iterator, Tuple, List

from preprocess.mappers.files.tree_sitter import build_ts_tree_extractor
from preprocess.extractors.tree_sitter import TreeEntity
from preprocess.utils import ProgrammingLanguages
import tree_sitter

from collections import Counter


def traverse_tree(entity: TreeEntity, level: int = 0) -> Iterator[Tuple[int, TreeEntity]]:
    """Yield tree structure with depth level"""
    yield level, entity
    for child in entity.children:
        yield from traverse_tree(child, level + 1)


def node_to_str(node: tree_sitter.Node, code_bytes: bytes) -> str:
    """
    :param node: node for transforming into string
    :param code_bytes: code bytes of file
    :return: string representation of node
    """
    return code_bytes[node[1].start_byte: node[1].end_byte].decode()


def extract_dotted_name(nodes: list, index: int, code_bytes: bytes) -> List:
    """
    :param nodes: level of nodes
    :param index: index, beginning from we want extract dotted name
    :param code_bytes: code bytes of file
    :return: list of dotted name and index of level after extracting
    """
    res = [node_to_str(nodes[index], code_bytes)]
    index += 1
    while index < len(nodes) and nodes[index][1].type == '.':
        index += 1
        res.append(node_to_str(nodes[index], code_bytes))
        index += 1
    return [res, index]


def get_python_imports(sorted_items: list) -> List[str]:
    """
    :param sorted_items: levels of nodes of imports
    :return: list of python's imports
    """
    treeEntity = sorted_items[0][1][0][1]
    l1_index = 0
    l2_index = 0
    l3_index = 0
    prefix = []
    if sorted_items[1][1][l1_index][1].type == 'from':
        if sorted_items[1][1][l1_index + 1][1].type == '__future__':
            prefix = ['__future__']
        else:
            prefix, l2_index = extract_dotted_name(sorted_items[2][1],
                                                l2_index,
                                                treeEntity.file.code_bytes)
        l1_index += 2
    l1_index += 1

    import_items = []
    for i in sorted_items[1][1][l1_index:]:
        if (i[1].type == 'aliased_import'):
            import_items.append([node_to_str(sorted_items[3][1][l3_index],
                                             treeEntity.file.code_bytes)])
            l2_index += 3
            l3_index += 1
        elif i[1].type == 'dotted_name':
            res, l2_index = extract_dotted_name(sorted_items[2][1],
                                                l2_index,
                                                treeEntity.file.code_bytes)
            import_items.append(res)

    return list(map(lambda x: ' '.join(prefix + x), import_items))


def get_imports(path: str) -> List[str]:
    """
    :param path: the path of the project to get all imports
    :return: list of imports
    """

    imports_extractor = build_ts_tree_extractor(Tokens.IMPORTS_TREE_SITTER)

    imports_entities = (
        CustomSource(path)
        .files_chain
        .flat_map(imports_extractor)
        .elements()
    )

    # for tree_identifier in imports_entities:
    #     tree_nodes_by_depth = groupby(lambda i: i[0], traverse_tree(tree_identifier))
    #     print(f"Identifier: {tree_identifier.file.repo}/{tree_identifier.file.file}#L{tree_identifier.start_line}")
    #     print("Structure:")
    #     for level, identifiers in sorted(tree_nodes_by_depth.items()):
    #         print(f"L{level}: {' '.join([i[1].type for i in identifiers])}")

    imports = []

    for tree_identifier in imports_entities:
        tree_nodes_by_depth = groupby(lambda i: i[0], traverse_tree(tree_identifier))
        sorted_items = sorted(tree_nodes_by_depth.items())
        if sorted_items[0][1][0][1].file.language == ProgrammingLanguages.PYTHON:
            imports.extend(get_python_imports(sorted_items))

    return dict(Counter(imports))
