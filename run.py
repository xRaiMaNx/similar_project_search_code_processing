import csv
import glob
import os
import time

import GetJSON
import multiprocessing as mp
from Logging.Logging import LOGGER


POOL_SIZE = 8


def save_json(id: int, queue, lock, count_bad_repos):
    while (True):
        lock.acquire()
        start_time = time.time()
        if not queue:
            lock.release()
            break
        index = len(queue) - 1
        data = queue.pop()
        lock.release()
        url = 'https://github.com/' + data['owner'] + '/' + data['name']
        git_info = {'stargazers_count': data['stargazers_count'],
                    'commit_sha': data['commit_sha'],
                    'repo_id': data['repo_id']}
        name = url.split('/')[-1].strip('\n')
        owner = url.split('/')[-2]
        LOGGER.info(f"worker#{id}  is processing repository#{index} {owner}/{name}")
        try:
            json_data = GetJSON.get_json(url.strip(), git_info)
            with open('jsons/' + owner + "_" + name + '.json', 'w') as file:
                file.write(json_data)
        except Exception as err:
            LOGGER.error(err)
            lock.acquire()
            count_bad_repos.value += 1
            lock.release()
        totr = time.time() - start_time  # totr -- time on this repository
        LOGGER.info(f"--- {owner}/{name}: {{:.2f}} seconds ---".format(totr))


def main() -> None:
    manager = mp.Manager()
    queue = manager.list([])
    count_bad_repos = manager.Value('count_bad_repos', 0)
    lock = mp.Lock()

    if not os.path.exists('jsons'):
        os.mkdir('jsons')
    if not os.path.exists('repos'):
        os.mkdir('repos')
    all_time = time.time()

    csvs = glob.glob('*.{}'.format('csv'))
    for filename in csvs:
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for dct in reader:
                queue.append(dct)
            pool = []
            for i in range(POOL_SIZE):
                pool.append(mp.Process(target=save_json, args=[i, queue, lock, count_bad_repos]))
                pool[-1].start()
            for p in pool:
                p.join()

    LOGGER.info("--- TOTAL TIME: {:.2f} seconds ---".format(time.time() - all_time))
    LOGGER.info(f"Bad repositories: {count_bad_repos.value}")


if __name__ == "__main__":
    main()
