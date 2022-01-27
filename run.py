import csv
import glob
import os
import time
import GetJSON
import multiprocessing as mp


POOL_SIZE = 8
count_bad_repos = 0
lock = mp.Lock()


def save_json(data: list, start: int, pool_size: int):
    global count_bad_repos
    for i in range(start, 2, pool_size):
        print("worker #", start, " is processing repository #", i, sep='')
        start_time = time.time()
        url = 'https://github.com/' + data[i]['owner'] + '/' + data[i]['name']
        git_info = {'stargazers_count': data[i]['stargazers_count'],
                    'commit_sha': data[i]['commit_sha'],
                    'repo_id': data[i]['repo_id']}
        name = url.split('/')[-1].strip('\n')
        owner = url.split('/')[-2]
        try:
            json_data = GetJSON.get_json(url.strip(), git_info)
            with open('jsons/' + owner + "_" + name + '.json', 'w') as file:
                file.write(json_data)    
        except Exception as err:
            print(err)
            lock.acquire()
            count_bad_repos += 1
            lock.release()
        totr = time.time() - start_time  # totr -- time on this repository
        print("--- " + owner + "/" + name + ": {:.2f} seconds ---".format(totr))


def main() -> None:
    global count_bad_repos

    if not os.path.exists('jsons'):
        os.mkdir('jsons')
    if not os.path.exists('repos'):
        os.mkdir('repos')
    all_time = time.time()

    csvs = glob.glob('*.{}'.format('csv'))
    for filename in csvs:
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            data = []
            for dct in reader:
                data.append(dct)
            pool = []
            for i in range(POOL_SIZE):
                pool.append(mp.Process(target=save_json, args=[data, i, POOL_SIZE]))
                pool[-1].start()
            for p in pool:
                p.join()

    print("--- TOTAL TIME: {:.2f} seconds ---".format(time.time() - all_time))
    print("Bad repositories:", count_bad_repos)


if __name__ == "__main__":
    main()
