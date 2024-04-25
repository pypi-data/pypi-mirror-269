import numpy as np

from data.bag import Bag
from data.instance import Instance


class MIMLDataset:
    """
    Class to manage MIML data obtained from datasets
    """

    def __init__(self) -> None:
        """
        Constructor of the class MIMLDataset
        """
        # TODO: Si dataset leido en csv, el nombre poner el del archivo
        self.name = "undefined"
        self.attributes = dict()
        self.data = dict()

    def set_name(self, name) -> None:
        """
        Set function for dataset name

        Parameters
        ----------
        name : str
            Name of the dataset
        """
        self.name = name

    def get_name(self) -> str:
        """
         Get function for dataset name

        Returns
        ----------
        name : str
            Name of the dataset
        """
        return self.name

    def get_attributes_name(self) -> list[str]:
        """
        Get attributes name

        Returns
        ----------
        attributes : list[str]
            Attributes name of the dataset
        """
        return list(self.attributes.keys())

    def get_attributes(self) -> np.ndarray:
        """
        Get attributes values of the dataset

        Returns
        -------
        attributes data: numpy array
            Values of the attributes of the dataset
        """
        pass
        # TODO: Ver si es necesario

    def get_number_attributes(self) -> int:
        """
        Get numbers of attributes of the bag

        Returns
        ----------
        numbers of attributes: int
            Numbers of attributes of the bag
        """
        return len(self.get_attributes_name())

    def set_features_name(self, features: list[str]) -> None:
        """
        Set function for dataset features name

        Parameters
        ----------
        features : list[str]
            List of the features name of the dataset
        """
        if len(self.attributes) != 0:
            for feature in self.get_features_name():
                if self.attributes[feature] == 0:
                    self.attributes.pop(feature)
        for feature in features:
            self.attributes[feature] = 0

    def get_features_name(self) -> list[str]:
        """
        Get function for dataset features name

        Returns
        ----------
        attributes : list[str]
            Attributes name of the dataset
        """
        features = []
        for feature in self.attributes.keys():
            if self.attributes[feature] == 0:
                features.append(feature)
        return features

    def get_features(self) -> np.ndarray:
        """
        Get features values of the dataset

        Returns
        -------
        features: numpy array
            Values of the features of the dataset
        """
        # TODO: Test
        features = np.zeros((self.get_number_instances(), self.get_number_features()))
        count = 0
        for key in self.data.keys():
            for instance in self.get_bag(key).get_features():
                features[count] = instance
                count += 1
        return features

    def get_features_by_bag(self) -> np.ndarray:
        features = []
        for key in self.data.keys():
            features.append(self.get_bag(key).get_features())
        return np.array(features, dtype=object)

    def get_number_features(self) -> int:
        """
        Get numbers of attributes of the dataset

        Returns
        ----------
         numbers of attributes: int
            Numbers of attributes of the dataset
        """
        return len(self.get_features_name())

    def set_labels_name(self, labels: list[str]) -> None:
        """
        Set function for dataset labels name

        Parameters
        ----------
        labels: list[str]
            List of the labels name of the dataset
        """
        if len(self.attributes) != 0:
            for label in self.get_labels_name():
                if self.attributes[label] == 1:
                    self.attributes.pop(label)
        for label in labels:
            self.attributes[label] = 1

    def get_labels_name(self) -> list[str]:
        """
        Get function for dataset labels name

        Returns
        ----------
        labels : list[str]
            Labels name of the dataset
        """
        labels = []
        for attribute in self.attributes.keys():
            if self.attributes[attribute] == 1:
                labels.append(attribute)
        return labels

    def get_labels(self):
        """
        Get labels values of the dataset

        Returns
        -------
        labels: ndarray of shape (n_instances, n_labels)
            Values of the labels of the dataset
        """
        labels = np.zeros((self.get_number_instances(), self.get_number_labels()))
        count = 0
        for key in self.data.keys():
            for instance in self.get_bag(key).get_labels():
                labels[count] = instance
                count += 1
        return labels

    def get_labels_by_bag(self):
        """
        Get labels values of the dataset

        Returns
        -------
        labels : ndarray of shape (n_bags, n_labels)
            Values of the labels of the dataset
        """
        labels = np.zeros((self.get_number_bags(), self.get_number_labels()))
        for bag_index, key in enumerate(self.data.keys()):
            labels[bag_index] = self.get_bag(key).get_labels()[0]
        return labels

    def get_number_labels(self) -> int:
        """
        Get numbers of labels of the dataset

        Returns
        ----------
        numbers of labels: int
            Numbers of labels of the dataset
        """
        return len(self.get_labels_name())

    def get_bag(self, key_bag: str) -> Bag:
        """
        Get data of a bag of the dataset

        Parameters
        ----------
        key_bag: str
            Key of the bag to be obtained

        Returns
        ----------
        bag: Bag
            Instance of Bag class
        """
        return self.data[key_bag]

    def get_number_bags(self) -> int:
        """
        Get numbers of bags of the dataset

        Returns
        ----------
        numbers of bags: int
            Numbers of bags of the dataset
        """
        return len(self.data)

    def add_bag(self, bag: Bag) -> None:
        """
        Add a bag to the dataset

        Parameters
        ----------
        bag : Bag
            Instance of Bag class to be added
        """
        bag.set_dataset(self)
        self.data[bag.key] = bag

    def delete_bag(self, key_bag: str) -> None:
        """
        Delete a bag of the dataset

        Parameters
        ----------
        key_bag : str
            Key of the bag which contains the instance to be deleted
        """
        self.data.pop(key_bag)

    def get_instance(self, key_bag, index_instance):
        """
        Get an Instance of the dataset

        Parameters
        ----------
        key_bag : str
            Key of the bag
            
        index_instance : int
            Index of the instance in the bag

        Returns
        -------
        instance : Instance
            Instance of Instance class
        """
        # TODO: check
        return self.get_bag(key_bag).get_instance(index_instance)

    def get_number_instances(self):
        """
        Get numbers of instances of the dataset

        Returns
        ----------
        numbers of instances: int
            Numbers of instances of the dataset
        """
        return sum(self.data[bag].get_number_instances() for bag in self.data.keys())

    def add_instance(self, key: str, instance: Instance) -> None:
        """
        Add an Instance to a Bag of the dataset

        Parameters
        ----------
        key : str
            Key of the bag where the instance will be added
        instance : Instance
            Instance of Instance class to be added
        """
        self.get_bag(key).add_instance(instance)

    def delete_instance(self, key_bag: str, index_instance: int) -> None:
        """
        Delete an instance of a bag of the dataset

        Parameters
        ----------
        key_bag : str
            Key of the bag which contains the instance to be deleted

        index_instance : int
            Index of the instance to be deleted
        """
        self.get_bag(key_bag).delete_instance(index_instance)

    def get_attribute(self, bag, instance, attribute):
        """
        Get value of an attribute of the bag

        Parameters
        ----------
        bag : str
            Key of the bag which contains the attribute

        instance : int
            Index of the instance in the bag

        attribute : int/str
            Index/Name of the attribute

        Returns
        -------
        value : float
            Value of the attribute
        """
        self.get_instance(bag, instance).get_attribute(attribute)

    def set_attribute(self, key_bag, index_instance, attribute, value):
        """
        Update value from attributes

            Parameters
            ----------
            key_bag : string
                Bag key of the dataset

            index_instance : int
                Index of the instance

            attribute: int/str
                Attribute of the dataset

            value: float
                New value for the update
            """
        self.get_instance(key_bag, index_instance).set_attribute(attribute, value)

    def add_attribute(self, position, values=None):
        """
        Add attribute to the bag

        Parameters
        ----------
        position : int
            Index for the new attribute

        values:  numpy array
            Values for the new attribute
        """
        # TODO: Test
        for bag_index, bag in enumerate(self.data.keys()):
            add_values = values[bag_index]
            if values is None:
                add_values = np.zeros(self.data[bag].get_number_instances)
            self.data[bag].add_attribute(position, add_values)

    def delete_attribute(self, position):
        for bag in self.data.keys():
            self.data[bag].delete_attribute(position)

    def show_dataset(self, head=None, attributes=None, labels=None):
        """
        Function to show information about the dataset

        Parameters
        ----------
            head : int
                Number of the nth firsts bag to show

            attributes: List of string
                Attributes to show

            labels : List of string
                Labels to show
        """
        # TODO: Formatearlo para que se vea bonito
        # TODO: Hacer algo como head y tail de pandas, ponerlo como parametro quizas, tambien lista atributos y labels
        #  a mostrar opcionales
        print("Name: ", self.get_name())
        print("Features: ", self.get_features_name())
        print("Labels: ", self.get_labels_name())
        print("Bags:")
        count = 0
        for key in self.data:
            # print("\n")
            bag = self.get_bag(key)
            # print("Key: ", key_bag)
            # print("Attributes: ", bag[0])
            # print("Labels: ", bag[1])
            bag.show_bag()
            count += 1
            if head is not None:
                if count >= head:
                    break

    # TODO: Ver si separar esto
    def cardinality(self):
        """
        Computes the Cardinality as the average number of labels per pattern.

        Returns
        ----------
        cardinality : float
            Average number of labels per pattern
        """
        suma = 0
        for key in self.data:
            suma += sum(self.get_bag(key).get_labels()[0])
        return suma / self.get_number_bags()

    def density(self):
        """
        Computes the density as the cardinality / numLabels.

        Returns
        ----------
        density : float
            Cardinality divided by number of labels
        """
        return self.cardinality() / self.get_number_labels()

    def distinct(self):
        """
        Computes the numbers of labels combinations used in the dataset respect all the possible ones

        Returns
        -------
        distinct : float
            Numbers of labels combinations used in the dataset divided by all possible combinations
        """
        options = set()
        for key in self.data:
            options.add(tuple(self.get_bag(key).get_labels()[0]))
        return len(options) / (2 ** self.get_number_labels())

    def get_statistics(self):
        """
        Calculate statistics of the dataset

        Returns
        -------
        n_instances : int
            Numbers of instances of the dataset

        min_instances : int
            Number of instances in the bag with minimum number of instances

        max_instances : int
            Number of instances in the bag with maximum number of instances

        distribution : dict
            Distribution of number of instances in bags
        """
        n_instances = self.get_number_instances()
        max_instances = 0
        # TODO: check
        min_instances = float("inf")
        distribution = dict()
        for key in self.data:
            instances_bag = self.get_bag(key).get_number_instances()
            if instances_bag in distribution:
                distribution[instances_bag] += 1
            else:
                distribution[instances_bag] = 1
            if instances_bag < min_instances:
                min_instances = instances_bag
            elif instances_bag > max_instances:
                max_instances = instances_bag
        return n_instances, min_instances, max_instances, distribution

    def describe(self):
        """
        Print statistics about the dataset
        """

        # TODO: Ponerlo bonito con tabulate

        print("-----MULTILABEL-----")
        print("Cardinalidad: ", self.cardinality())
        print("Densidad: ", self.density())
        print("Distinct: ", self.distinct())
        print("")
        # TODO: Testearlo
        n_instances, min_instances, max_instances, distribution = self.get_statistics()
        print("-----MULTIINSTANCE-----")
        print("Nº of bags: ", self.get_number_bags())
        print("Total instances: ", n_instances)
        print("Average Instances per bag: ", n_instances / self.get_number_bags())
        print("Min Instances per bag: ", min_instances)
        print("Max Instances per bag: ", max_instances)
        print("Attributes per bag: ", self.get_number_attributes())
        # TODO: Implementarlo
        # sb.append("\nDistribution of bags <nBags, nInstances>:");
