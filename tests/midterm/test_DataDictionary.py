from src.midterm import FoodAtlasRetriever, DataDictionary
import unittest
import random


class TestAtlasObjException(unittest.TestCase):
    def runTest(self):
        with self.assertRaises(TypeError):
            DataDictionary('foo')


class TestDataDictionary(unittest.TestCase):
    def setUp(self):
        """
        Creates atlas object and temp file path before tests
        """
        self.atlas = FoodAtlasRetriever()
        self.atlas.load()
        self.data_dictionary = DataDictionary(self.atlas)

    def tearDown(self):
        """
        Removes atlas object at end of test
        """
        self.atlas.clean()
        self.atlas = None


class TestPropObjException(TestDataDictionary):
    def runTest(self):
        with self.assertRaises(TypeError):
            self.data_dictionary.get_variable_properties('foo', 'bar')


class TestVarObjException(TestDataDictionary):
    def runTest(self):
        with self.assertRaises(IndexError):
            self.data_dictionary.get_variable_properties('foo')


# Test methods
class TestAll(TestDataDictionary):
    def testData(self):
        """
        Tests table existence
        :return: None
        """
        self.assertIn('Variable List', self.atlas.data.keys())
        self.assertGreater(len(self.atlas.data.keys()), 3)

    def testMethods(self):
        """
        Tests that get methods return lists
        """
        self.assertIsInstance(self.data_dictionary.get_vars(), list)
        self.assertIsInstance(self.data_dictionary.get_props(), list)

    def testGetProps(self):
        """
        Tests that the get props method returns correctly
        """
        self.assertIsInstance(self.data_dictionary.get_variable_properties(
            random.choice(self.data_dictionary.get_vars())
        ),
            dict)
        self.assertIsInstance(self.data_dictionary.get_variable_properties(
            random.choice(self.data_dictionary.get_vars()),
            [random.choice(self.data_dictionary.get_props())]
        ),
            dict)


if __name__ == '__main__':
    unittest.main()
