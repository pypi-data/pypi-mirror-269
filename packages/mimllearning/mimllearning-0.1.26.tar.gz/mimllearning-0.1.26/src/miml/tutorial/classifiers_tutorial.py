from sklearn.neighbors import KNeighborsClassifier
from miml.datasets import load_dataset
from miml.transformation import ArithmeticTransformation
from miml.classifier import MIMLtoMLClassifier, MIMLtoMIBRClassifier, AllPositiveAPRClassifier

dataset_train = load_dataset("../datasets/miml_birds_random_80train.arff", delimiter="'")
dataset_test = load_dataset("../datasets/miml_birds_random_20test.arff", delimiter="'")

classifier_ml = MIMLtoMLClassifier(KNeighborsClassifier(), ArithmeticTransformation())
classifier_ml.fit(dataset_train)
print(classifier_ml.predict_bag(dataset_test.get_bag("366")))
print(dataset_test.get_bag("366").get_labels()[0])
classifier_ml.evaluate(dataset_test)

classifier_mi = MIMLtoMIBRClassifier(AllPositiveAPRClassifier())
classifier_mi.fit(dataset_train)
print(classifier_mi.predict_bag(dataset_test.get_bag("366")))
print(dataset_test.get_bag("366").get_labels()[0])
classifier_mi.evaluate(dataset_test)
