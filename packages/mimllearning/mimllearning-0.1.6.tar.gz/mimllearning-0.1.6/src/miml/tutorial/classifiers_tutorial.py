import miml
from sklearn.neighbors import KNeighborsClassifier

dataset_train = miml.load_dataset("../datasets/miml_birds_random_80train.arff", delimiter="'")
dataset_test = miml.load_dataset("../datasets/miml_birds_random_20test.arff", delimiter="'")

classifier_ml = miml.MIMLtoMLClassifier(KNeighborsClassifier(), miml.ArithmeticTransformation())
classifier_ml.fit(dataset_train)
print(classifier_ml.predict_bag(dataset_test.get_bag("366")))
print(dataset_test.get_bag("366").get_labels()[0])
classifier_ml.evaluate(dataset_test)

classifier_mi = miml.MIMLtoMIBRClassifier(miml.AllPositiveAPRClassifier())
classifier_mi.fit(dataset_train)
print(classifier_mi.predict_bag(dataset_test.get_bag("366")))
print(dataset_test.get_bag("366").get_labels()[0])
#classifier_mi.evaluate(dataset_test)

