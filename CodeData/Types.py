import pygments.token

COMMENTS_TREE_SITTER = {
    "JavaScript": {"comment"},
}

COMMENTS_PYGMENTS = {
    "Python": {pygments.token.Comment, pygments.token.Literal.String.Doc},
}

IMPORTS_TREE_SITTER = {
    "Python": {"import_statement", "import_from_statement", "future_import_statement"}
}

IMPORTS_PYGMENTS = {
    "Python": {pygments.token}
}
