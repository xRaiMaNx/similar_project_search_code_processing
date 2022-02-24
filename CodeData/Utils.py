import git
import os
from shutil import rmtree
from Logging.Logging import LOGGER
import time


def remove_file(path: str):
    """
    must be used for removing path.txt and wabbit_sequences_names_0.txt
    :param path: path of file which should be removed
    """
    if os.path.exists(path):
        os.remove(path)


def remove_dir(path: str):
    """
    must be used for removing downloaded repository
    :param path: path of directory which should be removed
    """
    if os.path.exists(path):
        rmtree(path)


def download_repo(owner: str, name: str, path: str):
    """
    must be used for downloading repository
    :param owner: owner of repository
    :param name: name of repository
    :param path: path for downloaded reporitory
    :param download_zip: WARNING: experimental
    """
    start_time = time.time()

    remove_dir(path)
    git.Repo.clone_from('https://null:null@github.com/' + owner + '/' + name,
                        path)
    LOGGER.info(f"{owner}/{name} download time: {time.time() - start_time}")
