import numpy as np

from data.bag import Bag
from data.miml_dataset import MIMLDataset
from transformation.mimlTOml.miml_to_ml_transformation import MIMLtoMLTransformation


class ArithmeticTransformation(MIMLtoMLTransformation):
    """
    Class that performs an arithmetic transformation to convert a MIMLDataset class to numpy ndarrays.
    """

    def __init__(self):
        super().__init__()

    def transform_dataset(self, dataset: MIMLDataset) -> tuple:
        """
        Transform the dataset to multilabel dataset converting each bag into a single instance being the value of each
        attribute the mean value of the instances in the bag.

        Returns
        -------

        X : ndarray of shape (n_bags, n_features)
            Training vector

        Y : ndarray of shape (n_bags, n_labels)
            Target vector relative to X.
        """
        self.dataset = dataset
        x = np.empty(shape=(self.dataset.get_number_bags(), self.dataset.get_number_features()))
        y = np.empty(shape=(self.dataset.get_number_bags(), self.dataset.get_number_labels()))
        for bag_index, key in enumerate(self.dataset.data.keys()):
            features, labels = self.transform_bag(self.dataset.get_bag(key))
            x[bag_index] = features
            y[bag_index] = labels

        return x, y

    def transform_bag(self, bag: Bag):
        """
        Transform a bag to a multilabel instance

        Parameters
        ----------
        bag : Bag
            Key of the bag to be transformed

        Returns
        -------
        features : ndarray of shape (n_features)
            Numpy array with feature values

        labels : ndarray of shape (n_labels)
            Numpy array with label values
        """

        features = bag.get_features()
        labels = bag.get_labels()[0]
        features = np.mean(features, axis=0)
        return features, labels
