import csv
import glob
import os
import time
import GetJSON


def main() -> None:
    count_bad_repos = 0
    all_time = time.time()
    csvs = glob.glob('*.{}'.format('csv'))
    for filename in csvs:
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for data in reader:
                start_time = time.time()
                url = 'https://github.com/' + data['owner'] + '/' + data['name']
                git_info = {'stargazers_count': data['stargazers_count'],
                            'commit_sha': data['commit_sha'],
                            'repo_id': data['repo_id']}
                try:
                    name = url.split('/')[-1]
                    name = name.strip('\n')
                    data = GetJSON.get_json(url.strip(), True, git_info)
                    with open('jsons/' + name + '.json', 'w') as file:
                        file.write(data)
                except Exception as err:
                    print(err)
                    count_bad_repos += 1
                totr = time.time() - start_time  # totr -- time on this repository
                print("--- %s seconds ---" % (totr))
    if not os.path.exists('jsons'):
        os.mkdir('jsons')
    repos_path = "repos"
    if not os.path.exists(repos_path):
        raise FileNotFoundError(repos_path, "is incorrect path")
    repos_path = os.path.abspath(repos_path)
    for project_name in os.listdir(repos_path):
        start_time = time.time()
        try:
            data = GetJSON.get_json(repos_path + "/" + project_name)
            with open('jsons/' + project_name + '.json', 'w') as file:
                file.write(data)
        except Exception as err:
            print(err)
            count_bad_repos += 1
        totr = time.time() - start_time  # totr -- time on this repository
        print("--- %s seconds ---" % (totr))
    with open("./urls.txt", 'r', encoding='utf-8') as urls:
        for url in urls:
            start_time = time.time()
            try:
                name = url.split('/')[-1]
                name = name.strip('\n')
                data = GetJSON.get_json(url.strip(), True)
                with open('jsons/' + name + '.json', 'w') as file:
                    file.write(data)
            except Exception as err:
                print(err)
                count_bad_repos += 1
            totr = time.time() - start_time  # totr -- time on this repository
            print("--- %s seconds ---" % (totr))

    print("--- %s second ---" % (time.time() - all_time))
    print("Bad repositories:", count_bad_repos)


if __name__ == "__main__":
    main()
