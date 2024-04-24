import os

import numpy as np

from data.bag import Bag
from data.instance import Instance
from data.miml_dataset import MIMLDataset


def load_dataset(file, delimiter="\""):
    """
    Function to load a dataset

    Parameters
    ----------

    file : str
        Path of the dataset file
    delimiter : str
        Character to separate instances in bag of the arff files
    """
    if file[-4:] == ".csv":
        return load_dataset_csv(file)
    elif file[-5:] == ".arff":
        return load_dataset_arff(file, delimiter)
    else:
        print("Error")
        # TODO: Control de errores


def load_dataset_csv(file, header=0):
    """
    Function to load a dataset in csv format

    Parameters
    ----------
    file : str
        Path of the dataset file

    Returns
    -------
    dataset : MIMLDataset
        Dataset loaded
    """
    # dataset = pd.read_csv(file, header=0)
    # TODO: Hay que ver como diferenciar los atributos de las labels
    # TODO: Si no se puede implementar la funcionalidad de pandas "[]"
    # TODO: y poner atributos y labels como parametros opcionales quizas

    dataset = MIMLDataset()
    csv_file = open(file)

    file_name = os.path.basename(file)
    dataset.set_name(os.path.splitext(file_name)[0])

    # TODO: Hacer que se pueda pasar por parametro
    num_labels = int(csv_file.readline().replace("\n", ""))

    header_line = csv_file.readline().replace("\n", "").split(",")
    features_name = header_line[1:-num_labels]
    dataset.set_features_name(features_name)
    labels_name = header_line[-num_labels:]
    dataset.set_labels_name(labels_name)

    for line in csv_file:

        data = line.split(",")

        key = data[0]

        # TODO: Revisar porque values tiene el ndmin=2
        values = np.array([float(i) for i in data[1:-num_labels]], ndmin=2)
        labels = np.array([int(i) for i in data[-num_labels:]])

        instance = Instance(values + labels)

        if key not in dataset.data:
            bag = Bag(key)
            dataset.add_bag(bag)
        dataset.add_instance(key, instance)

    return dataset


def load_dataset_arff(file, delimiter="\""):
    """
    Function to load a dataset in arff format

    Parameters
    ----------
    file : str
        Path of the dataset file
    delimiter : str
        Delimiter of instances in a bag in the arff file
    """
    dataset = MIMLDataset()
    arff_file = open(file)
    features_name = []
    labels_name = []
    flag = 0
    for line in arff_file:

        # Comprobamos que la cadena no contenga espacios en blanco a la izquierda ni que sea vacía
        line = line.lstrip()

        if not line or line.startswith("%") or line.startswith("@data"):
            continue

        if line.startswith("@"):

            if line.startswith("@relation"):
                dataset.set_name(line[line.find(" ") + 1:])
            elif line.startswith("@attribute bag relational"):
                flag = 1
            elif line.startswith("@end bag"):
                flag = 2
            elif flag == 1:
                features_name.append(line.split(" ")[1])
            elif flag == 2:
                labels_name.append(line.split(" ")[1])

        else:
            # Eliminanos el salto de línea del final de la cadena
            line = line.strip("\n")

            # Asumimos que el primer elemento de cada instancia es el identificador de la bolsa
            key = line[0:line.find(",")]

            # Empiezan los datos de la bolsa cuando encontremos la primera '"' y terminan con la segunda '"'
            line = line[line.find(delimiter) + 1:]
            values = line[:line.find(delimiter, 2)]
            # Separamos los valores por instancias de la bolsa
            values = values.split("\\n")

            # El resto de la cadena se trata de las etiquetas
            labels = line[line.find(delimiter, 2) + 2:]
            labels_values = np.array([int(i) for i in labels.split(",")], ndmin=1)
            # print("Labels: ", labels)

            values_list = []
            for v in values:
                values_instance = np.array([float(i) for i in v.split(',')], ndmin=1)
                instance = Instance(np.hstack((values_instance, labels_values)))
                if key not in dataset.data:
                    bag = Bag(key)
                    bag.add_instance(instance)
                    dataset.add_bag(bag)
                else:
                    dataset.add_instance(key, instance)

    dataset.set_features_name(features_name)
    dataset.set_labels_name(labels_name)
    return dataset
