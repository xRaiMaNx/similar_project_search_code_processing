import GetLanguages

path = input()  # enter path of project
stats = GetLanguages.get_languages(path)
if stats:
    print(stats[0][1])
