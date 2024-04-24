

from classifier.miml_classifier import *

from transformation.mimlTOml.miml_to_ml_transformation import MIMLtoMLTransformation


class MIMLtoMLClassifier(MIMLClassifier):

    def __init__(self, ml_classifier, transformation: MIMLtoMLTransformation) -> None:
        """
        Constructor of the class MIMLtoMIClassifier

        Parameters
        ----------
        ml_classifier
            Specific classifier to be used

        transformation : MIMLtoMLTransformation
            Transformation to be used
        """
        super().__init__()
        self.classifier = ml_classifier
        self.transformation = transformation

    def fit_internal(self, dataset_train: MIMLDataset) -> None:
        """

        Parameters
        ----------
        dataset_train
        """
        x_train, y_train = self.transformation.transform_dataset(dataset_train)
        self.classifier.fit(x_train, y_train)

    def predict(self, x: np.ndarray):
        return self.classifier.predict(x)

    def predict_bag(self, bag: Bag) -> np.ndarray:
        """

        Parameters
        ----------
        bag
        """
        # TODO: Check number attributes of bag with dataset
        super().predict_bag(bag)
        x_bag, _ = self.transformation.transform_bag(bag)
        x_bag = np.array(x_bag, ndmin=2)
        return self.predict(x_bag)

    def evaluate(self, dataset_test: MIMLDataset):
        """

        Parameters
        ----------
        dataset_test
        """
        super().evaluate(dataset_test)
        x_test, y_test = self.transformation.transform_dataset(dataset_test)
        results = self.predict(x_test)

        print(classification_report(dataset_test.get_labels_by_bag(), results))
        print("Hamming Loss: ", hamming_loss(dataset_test.get_labels_by_bag(), results))


