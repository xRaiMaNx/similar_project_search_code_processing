from Languages import GetLanguages
from Imports import GetImports
import os

path = input()  # enter path of project

# ~ doesn't work with os
if not os.path.exists(path):
    raise FileNotFoundError("Incorrect path")

stats = GetLanguages.get_languages(path)

imports = GetImports.get_imports(path)

print(stats)
print(imports)
