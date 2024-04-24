import 

dataset_train = load_dataset("../datasets/miml_birds_random_80train.arff", delimiter="'")
dataset_test = load_dataset("../datasets/miml_birds_random_20test.arff", delimiter="'")

#classifier = MIMLtoMLClassifier(KNeighborsClassifier(), ArithmeticTransformation())
classifier = MIMLtoMIBRClassifier(AllPositiveAPRClassifier())

classifier.fit(dataset_train)

print(classifier.predict_bag(dataset_test.get_bag("366")))
print(dataset_test.get_bag("366").get_labels()[0])

classifier.evaluate(dataset_test)
