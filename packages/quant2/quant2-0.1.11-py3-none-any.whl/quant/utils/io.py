import json
import pickle
import shutil
from pathlib import Path


def make_dir(path, exist_ok=True):
    path = Path(path)

    if not exist_ok:
        shutil.rmtree(path, ignore_errors=True)

    path.mkdir(parents=True, exist_ok=True)
    return path


def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def load_pkl(file):
    with open(file, "rb") as f:
        data = pickle.load(f)
    return data


def save_json(file, data, indent=None):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
    return file


def save_pkl(file, data):
    with open(file, "wb") as f:
        pickle.dump(data, f)
    return file


def copy_file(src, dst, pattern=None):
    # Copies the file `src` to the file or directory `dst`.
    # Set `pattern` to glob the given relative pattern
    if pattern is not None:
        for src in Path(src).glob(pattern):
            shutil.copy(src, dst)
    else:
        shutil.copy(src, dst)
