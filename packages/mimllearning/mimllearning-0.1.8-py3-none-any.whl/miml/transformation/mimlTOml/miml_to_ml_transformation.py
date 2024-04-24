from abc import ABC, abstractmethod

from data.bag import Bag
from data.miml_dataset import MIMLDataset


class MIMLtoMLTransformation(ABC):

    def __init__(self) -> None:
        self.dataset = None

    @abstractmethod
    def transform_dataset(self, dataset: MIMLDataset):
        pass

    @abstractmethod
    def transform_bag(self, bag: Bag):
        pass
