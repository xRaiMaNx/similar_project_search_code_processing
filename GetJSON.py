from Languages import GetLanguages

path = input()  # enter path of project
stats = GetLanguages.get_languages(path)
print(stats)
