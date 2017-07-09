from collections import deque
from os import remove, walk
from os.path import join
from pathlib import Path
from shutil import rmtree

DELETE_IN_ROOT = {
    '.cache',
    '.coverage',
    '.eggs',
    '.tox',
    'build',
    'dist',
    '*.egg-info',
}
DELETE_EVERYWHERE = {
    '__pycache__',
    '*.pyc'
}
ALL_GLOBS = DELETE_IN_ROOT | DELETE_EVERYWHERE


def get_path(dir_entry):
    return dir_entry.path


def delete_path(path):
    try:
        rmtree(path)
    except OSError:
        try:
            remove(path)
        except FileNotFoundError:
            pass


def clean_package(d):
    removal_queue = deque()
    removed = []

    root = Path(d)
    for glob in ALL_GLOBS:
        for p in root.glob(glob):
            removal_queue.append(str(p))

    for root, dirs, files in walk(d):
        for d in dirs:
            d = join(root, d)
            for glob in DELETE_EVERYWHERE:
                for p in Path(d).glob(glob):
                    removal_queue.append(str(p))

    for _ in range(len(removal_queue)):
        p = removal_queue.popleft()
        delete_path(p)
        removed.append(p)

    return sorted(removed)