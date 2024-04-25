import numpy as np
from tabulate import tabulate

from data.instance import Instance


class Bag:
    """
    Class to manage MIML Bag data representation
    """

    def __init__(self, key: str) -> None:
        """
        Constructor of the class Bag

        Parameters
        ----------
        key : str
            Key of the bag
        """
        # TODO: Ver si quitar instance del constructor, se puede poner como parametro opcional
        self.data = None
        self.key = key
        self.dataset = None

    def get_attributes_name(self) -> list[str]:
        """
        Get attributes name of the bag

        Returns
        ----------
        attributes : list[str]
            Attributes name of the bag
        """
        if self.dataset is not None:
            return self.dataset.get_attributes_name()
        else:
            raise Exception("The bag isn't in any dataset, so there is no attributes info")

    def get_attributes(self) -> np.ndarray:
        """
        Get attributes values of the bag

        Returns
        -------
        attributes data: ndarray of shape(n_instances, n_attributes)
            Values of the attributes of the bag

        """
        return self.data

    def get_number_attributes(self) -> int:
        """
        Get numbers of attributes of the bag

        Returns
        ----------
         numbers of attributes: int
            Numbers of attributes of the bag
        """
        return len(self.get_attributes()[0])

    def get_features_name(self) -> list[str]:
        """
        Get features name of the bag

        Returns
        ----------
        features : list[str]
            Features name of the bag
        """
        if self.dataset is not None:
            return self.dataset.get_features_name()
        else:
            raise Exception("The bag isn't in any dataset, so there is no features info")

    def get_features(self) -> np.ndarray:
        """
        Get features values of the bag

        Returns
        -------
        features data: ndarray of shape (n_instances, n_features)
            Values of the features of the bag

        """
        return self.data[0:, 0:self.get_number_features()]

    def get_number_features(self) -> int:
        """
        Get numbers of features of the bag

        Returns
        ----------
         numbers of features: int
            Numbers of features of the bag
        """
        if self.dataset is not None:
            return self.dataset.get_number_features()
        else:
            raise Exception("The bag isn't in any dataset, so there is no features info")

    def get_labels_name(self) -> list[str]:
        """
        Get labels name of the bag

        Returns
        ----------
        labels : list[str]
            Labels name of the bag
        """
        if self.dataset is not None:
            return self.dataset.get_labels_name()
        else:
            raise Exception("The bag isn't in any dataset, so there is no label info")

    def get_labels(self) -> np.ndarray:
        """
        Get labels values of the bag

        Returns
        -------
        labels data : ndarray of shape (n_instances, n_labels)
            Values of the labels of the bag

        """
        return self.data[0:, -self.get_number_labels():]

    def get_number_labels(self) -> int:
        """
        Get numbers of labels of the bag

        Returns
        ----------
        numbers of labels: int
            Numbers of labels of the bag
        """
        if self.dataset is not None:
            return self.dataset.get_number_labels()
        else:
            raise Exception("The bag isn't in any dataset, so there is no label info")

    def get_instance(self, index: int) -> Instance:
        """
        Get an Instance of the Bag

        Parameters
        ----------
        index : int
            Index of the instance in the bag

        Returns
        -------
        instance : Instance
            Instance of Instance class
        """
        instance = Instance(self.data[index], self)
        return instance

    def get_number_instances(self) -> int:
        """
        Get numbers of instances of a bag

        Returns
        ----------
        numbers of instances: int
            Numbers of instances of a bag
        """
        return len(self.data)

    def add_instance(self, instance: Instance) -> None:
        """
        Add instance to the bag

        Parameters
        ----------
        instance : Instance
            Instance to be added
        """
        if self.data is None:
            self.data = np.zeros((1, instance.get_number_attributes()))
            self.data[0] = instance.data
        elif instance.get_number_attributes() == self.get_number_attributes():
            self.data = np.vstack((self.data, instance.data))
        else:
            raise Exception("The number of attributes of the bag and the instance to be added are different.")
        instance.set_bag(self)

    def delete_instance(self, index: int) -> None:
        """
        Delete an instance of the bag

        Parameters
        ----------
        index : int
            Index of the instance to be removed
        """
        self.data = np.delete(self.data, index, axis=0)

    def get_attribute(self, instance: int, attribute) -> float:
        """
        Get value of an attribute of the bag

        Parameters
        ----------
        instance : int
            Index of the instance in the bag

        attribute : int/str
            Index/Name of the attribute

        Returns
        -------
        value : float
            Value of the attribute
        """
        if isinstance(attribute, int):
            return self.data[instance].item(attribute)
        elif isinstance(attribute, str):
            index = list(self.get_attributes()).index(attribute)
            return self.data[instance].item(index)

    def set_attribute(self, instance: int, attribute, value: float) -> None:
        """
        Update value from attributes

        Parameters
        ----------
        instance : string
            Index of instance to be updated

        attribute: int/str
            Attribute name/index_instance of the bag to be updated

        value: float
            New value for the update
        """
        if isinstance(attribute, int):
            self.data[instance][attribute] = value
        elif isinstance(attribute, str):
            index = list(self.get_attributes()).index(attribute)
            self.data[instance][index] = value

    def add_attribute(self, position: int, values=None) -> None:
        """
        Add attribute to the bag

        Parameters
        ----------
        position : int
            Index for the new attribute

        values: array-like of shape (n_attributes)
            Values for the new attribute. If not provided, new values would be zero
        """
        if self.dataset is None:
            if position is None:
                position = len(self.data)
            if values is None:
                values = np.array([0]*self.get_number_instances())
            elif len(values) != self.get_number_instances():
                raise Exception("Incorrect number of values for the new attribute. Should be the same as number of "
                                "instances of the bag")
            self.data = np.insert(self.data, position, values, axis=1)
        else:
            raise Exception("Can't add an attribute to a bag assigned to a dataset")

    def delete_attribute(self, position: int) -> None:
        """
        Delete attribute of the bag

        Parameters
        ----------
        position : int
            Position of the attribute in the bag
        """
        if self.dataset is None:
            self.data = np.delete(self.data, position, axis=1)
        else:
            raise Exception("Can't delete an attribute of a bag assigned to a dataset")

    def set_dataset(self, dataset) -> None:
        """
        Set dataset which contains the bag

        Parameters
        ----------
        dataset : MIMLDataset
            Dataset for the bag
        """
        self.dataset = dataset

    def show_bag(self) -> None:
        """
        Show bag info in table format
        """
        if self.dataset is None:
            table = [[self.key]+[""]*self.get_number_attributes()]
        else:
            table = [[self.key] + self.get_features_name() + self.get_labels_name()]
        for index_instance in range(self.get_number_instances()):
            table.append([index_instance] + list(self.get_instance(index_instance).get_attributes()))
        print(tabulate(table, headers='firstrow', tablefmt="grid", numalign="center"))
