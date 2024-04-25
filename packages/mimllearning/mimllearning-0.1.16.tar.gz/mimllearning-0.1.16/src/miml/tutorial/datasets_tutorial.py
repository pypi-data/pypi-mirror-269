import miml

dataset_train = miml.load_dataset("../datasets/miml_birds_random_80train.arff", delimiter="'")
dataset_test = miml.load_dataset("../datasets/miml_birds_random_20test.arff", delimiter="'")

dataset_test.show_dataset(head=5)

