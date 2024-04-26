from sklearn.neighbors import KNeighborsClassifier
#from miml.datasets.load_dataset import load_dataset
#from miml.classifier.mimlTOml.miml_to_ml_classifier import MIMLtoMLClassifier
#from miml.transformation.mimlTOml.arithmetic import ArithmeticTransformation
#from miml.classifier.mimlTOmi.miml_to_mi_br_classifier import MIMLtoMIBRClassifier
#from miml.classifier.mi.all_positive_apr_classifier import AllPositiveAPRClassifier

from miml import *

dataset_train = miml.datasets.load_dataset.load_dataset("../datasets/miml_birds_random_80train.arff", delimiter="'")
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

