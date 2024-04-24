
from classifier.miml_classifier import *


class MIMLtoMIClassifier(MIMLClassifier):
    """
    Class to represent a multiinstance classifier
    """

    def __init__(self, mi_classifier):
        """
        Constructor of the class MIMLtoMIClassifier

        Parameters
        ----------
        mi_classifier
            Specific classifier to be used
        """
        super().__init__()
        self.classifier = mi_classifier

    @abstractmethod
    def fit_internal(self, dataset_train: MIMLDataset):
        pass

    def predict(self, x: np.ndarray):
        return self.classifier.predict(x)

    def predict_bag(self, bag: Bag):
        """
        Predict labels of given data

        Parameters
        ----------
        bag : Bag
            Bag to predict their classes
        """
        super().predict_bag(bag)

    def evaluate(self, dataset_test: MIMLDataset):
        """

        Parameters
        ----------
        dataset_test
        """
        super().evaluate(dataset_test)
