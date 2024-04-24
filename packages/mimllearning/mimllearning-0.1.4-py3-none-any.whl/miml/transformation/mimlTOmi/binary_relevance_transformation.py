from data.bag import Bag
from data.miml_dataset import MIMLDataset


class BinaryRelevanceTransformation:
    """
    Class that performs a binary relevance transformation to convert a MIMLDataset class to numpy ndarrays.
    """

    def __init__(self):
        self.dataset = None

    def transform_dataset(self, dataset: MIMLDataset) -> list:
        """
        Transform the dataset to multiinstance datasets dividing the original dataset into n datasets with a single
        label, where n is the number of labels.

        Returns
        -------

        datasets: list
            Multi instance datasets

        """
        self.dataset = dataset
        datasets = []
        x = self.dataset.get_features_by_bag()
        y = self.dataset.get_labels_by_bag()
        for i in range(self.dataset.get_number_labels()):
            datasets.append([x, y[:, i].reshape(-1, 1)])

        return datasets

    def transform_bag(self, bag: Bag) -> list:
        """
        Transform miml bag to multi instance bags

        Parameters
        ----------
        bag :
            Bag to be transformed to multiinstance bag

        Returns
        -------
        bags : list[ndarray]
        Tuple of numpy ndarray with attribute values and labels

        """
        bags = [[bag.get_features(), label] for label in bag.get_labels()[0]]
        return bags


