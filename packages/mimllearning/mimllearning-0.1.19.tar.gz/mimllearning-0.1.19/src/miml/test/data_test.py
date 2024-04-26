import unittest

from data.bag import Bag
from data.instance import Instance
from data.miml_dataset import MIMLDataset


class TestData(unittest.TestCase):
    def test_instance(self):
        values = [2, 7, 5.09, 1, 0]
        instance = Instance(values)
        self.assertEqual(instance.get_number_attributes(), 5)
        instance.add_attribute(0.8, 1)
        self.assertEqual(list(instance.get_attributes()), [2, 0.8, 7, 5.09, 1, 0])
        instance.delete_attribute(2)
        self.assertEqual(list(instance.get_attributes()), [2, 0.8, 5.09, 1, 0])
        instance.set_attribute(4, 1)
        self.assertEqual(list(instance.get_attributes()), [2, 0.8, 5.09, 1, 1])
        with self.assertRaises(Exception) as error:
            instance.get_number_features()
        self.assertEqual(error.exception.args[0], "The instance isn't in any dataset, so there is no features info")

    def test_bag(self):
        # TODO:
        values = [2, 7, 5.09, 1, 0]
        instance = Instance(values)
        bag = Bag("1")
        bag.add_instance(instance)
        self.assertEqual(bag.get_number_instances(), 1)
        self.assertEqual(list(bag.get_instance(0).get_attributes()), list(instance.get_attributes()))
        self.assertEqual(bag.get_number_attributes(), 5)
        instance.set_attribute(1, 1)
        self.assertEqual(list(bag.get_instance(0).get_attributes()), list(instance.get_attributes()))
        #bag.add_instance(instance)


    def test_mimldataset(self):
        # TODO:
        pass

    def test_final(self):
        # TODO:
        values = [2, 7, 5.09, 1, 0]
        instance1 = Instance(values)
        instance2 = Instance(values)
        bag = Bag("bag1")
        bag.add_instance(instance1)
        bag.add_instance(instance2)

        dataset = MIMLDataset()
        dataset.set_features_name(["attr1", "attr2", "attr3"])
        dataset.set_labels_name(["label1", "label2"])
        #instance1.show_instance()
        dataset.add_bag(bag)
        #instance1.show_instance()


if __name__ == '__main__':
    unittest.main()
