
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

        accuracy = accuracy_score(dataset_test.get_labels_by_bag(), results)
        average_precision = average_precision_score(dataset_test.get_labels_by_bag(), results)
        f1_macro = f1_score(dataset_test.get_labels_by_bag(), results, average='macro')
        f1_micro = f1_score(dataset_test.get_labels_by_bag(), results, average='micro')
        hamming_loss_score = hamming_loss(dataset_test.get_labels_by_bag(), results)
        precision_macro = precision_score(dataset_test.get_labels_by_bag(), results, average='macro')
        precision_micro = precision_score(dataset_test.get_labels_by_bag(), results, average='micro')
        recall_macro = recall_score(dataset_test.get_labels_by_bag(), results, average='macro')
        recall_micro = recall_score(dataset_test.get_labels_by_bag(), results, average='micro')

        print(accuracy, average_precision, f1_macro, f1_micro, hamming_loss_score, precision_macro, precision_micro,
              recall_macro, recall_micro)
