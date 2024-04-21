import numpy as np
from pathlib import Path
from quant.utils.io import load_pkl, make_dir, save_pkl


def get_subset(X, Y, Z, indices):
    _X, _Y, _Z = [], [], []
    for index in indices:
        _X.append(X[index])
        _Y.append(Y[index])
        _Z.append(Z[index])
    return _X, _Y, _Z


def shuffle_split(pkl_file, n_splits=10, test_size=None, train_size=None, random_state=1):
    X, Y, Z = load_pkl(pkl_file)
    out_dir = Path(pkl_file).parent

    n_samples = len(X)

    test_size = test_size or 0.1
    train_size = train_size or 0.3

    n_test = test_size if isinstance(test_size, int) else int(test_size * n_samples)
    n_train = train_size if isinstance(train_size, int) else int(train_size * n_samples)

    rng = np.random.RandomState(random_state)
    for i in range(n_splits):
        split_dir = make_dir(out_dir / f"split{i:02d}", exist_ok=False)
        permutation = rng.permutation(n_samples)
        ind_test = permutation[:n_test]
        ind_train = permutation[n_test: (n_test + n_train)]
        save_pkl(split_dir / "test.pkl", get_subset(X, Y, Z, ind_test))
        save_pkl(split_dir / "train.pkl", get_subset(X, Y, Z, ind_train))
        print(f"{split_dir}: train {len(ind_train)}, test {len(ind_test)}.")
