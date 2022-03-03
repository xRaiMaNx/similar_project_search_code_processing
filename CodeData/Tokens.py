import pygments.token

DOCSTRINGS_PYGMENTS = {
    "Python": {pygments.token.Literal.String.Doc},
}

IMPORTS_TREE_SITTER = {
    "Python": {"import_statement", "import_from_statement", "future_import_statement"}
}
