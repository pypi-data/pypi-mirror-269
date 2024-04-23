from .base import ClassificationDataset, RegressionDataset, FootballDatasetV1, FootballDatasetV2


def get_dataset(dataset_type, *args, **kwargs):
    if dataset_type == "ClassificationDataset":
        return ClassificationDataset(*args, **kwargs)
    elif dataset_type == "RegressionDataset":
        return RegressionDataset(*args, **kwargs)
    elif dataset_type == "FootballDatasetV1":
        return FootballDatasetV1(*args, **kwargs)
    elif dataset_type == "FootballDatasetV2":
        return FootballDatasetV2(*args, **kwargs)
    else:
        raise NotImplementedError(f"Not supported <{dataset_type=}>.")
