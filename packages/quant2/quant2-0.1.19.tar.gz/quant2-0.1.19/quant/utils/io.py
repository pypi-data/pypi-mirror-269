import json
import pickle
import shutil
import numpy as np
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


def load_npy(file):
    with open(file, "rb") as f:
        data = np.load(f)
    return data


def load_npz(file):
    with open(file, "rb") as f:
        data = {n: a for n, a in np.load(f).items()}
    return data


def save_json(file, data, indent=None):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)
    return file


def save_pkl(file, data):
    with open(file, "wb") as f:
        pickle.dump(data, f)
    return file


def save_npy(file, data):
    with open(file, "wb") as f:
        np.save(f, data)
    return file


def save_npz(file, **kwargs):
    with open(file, "wb") as f:
        np.savez(f, **kwargs)
    return file


def auto_load(file):
    suffix = Path(file).suffix
    if suffix == ".json":
        return load_json(file)
    elif suffix == ".pkl":
        return load_pkl(file)
    elif suffix == ".npy":
        return load_npy(file)
    elif suffix == ".npz":
        return load_npz(file)
    else:
        raise NotImplementedError(f"Not supported <{suffix=}>.")


def auto_save(file, *args, **kwargs):
    suffix = Path(file).suffix
    if suffix == ".json":
        return save_json(file, *args)
    elif suffix == ".pkl":
        return save_pkl(file, *args)
    elif suffix == ".npy":
        return save_npy(file, *args)
    elif suffix == ".npz":
        return save_npz(file, **kwargs)
    else:
        raise NotImplementedError(f"Not supported <{suffix=}>.")


def copy_file(src, dst, pattern=None):
    # Copies the file `src` to the file or directory `dst`.
    # Set `pattern` to glob the given relative pattern
    if pattern is not None:
        for src in Path(src).glob(pattern):
            shutil.copy(src, dst)
    else:
        shutil.copy(src, dst)
