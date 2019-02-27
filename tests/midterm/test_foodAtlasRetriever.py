import unittest
from src.midterm import FoodAtlasRetriever
import requests
import os
import tempfile


class TestUrlException(unittest.TestCase):
    def runTest(self):
        self.atlas = FoodAtlasRetriever(url="http://thisisabrokendomain.foo")
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.atlas.get()


class TestFileException(unittest.TestCase):
    def runTest(self):
        self.atlas = FoodAtlasRetriever(url="https://google.com/")
        with self.assertRaises(FileNotFoundError):
            self.atlas.get()


class TestCleanException(unittest.TestCase):
    def runTest(self):
        self.atlas = FoodAtlasRetriever()
        self.assertFalse(self.atlas.clean())


class TestFoodAtlasRetriever(unittest.TestCase):
    def setUp(self):
        """
        Creates atlas object and temp file path before tests
        """
        self.atlas = FoodAtlasRetriever()
        self.pickle = os.path.join(tempfile.gettempdir(), "atlasTest.pickle")

    def tearDown(self):
        """
        Removes atlas object at end of test
        """
        self.atlas.clean()
        self.atlas = None


class TestWorkbook(TestFoodAtlasRetriever):
    def runTest(self):
        """
        Check if atlas.workbook initializes as None
        """
        self.assertIsNone(self.atlas.workbook)


class TestUrl(TestFoodAtlasRetriever):
    def runTest(self):
        """
        Check if atlas.url is a valid address
        """
        url_test = requests.get(self.atlas.url)
        self.assertTrue(url_test.ok)


class TestData(TestFoodAtlasRetriever):
    def runTest(self):
        """
        Check if atlas.data initializes as empty dictionary
        """
        self.assertDictEqual(self.atlas.data, {})


class TestExcelUrl(TestFoodAtlasRetriever):
    def runTest(self):
        """
        Check if atlas.excel_url initializes as None
        """
        self.assertIsNone(self.atlas.excel_url)


class TestExcel(TestFoodAtlasRetriever):
    def runTest(self):
        """
        Check if atlas.excel is a writable temp file
        """
        self.assertTrue(self.atlas.excel.file._checkWritable())


# Test methods
class TestGet(TestFoodAtlasRetriever):
    def testData(self):
        """
        Tests data validity after get method
        :return: None
        """
        self.atlas.get()
        self.assertIsNot(self.atlas.data, {})
        self.assertGreater(len(self.atlas.data), 1)
        self.assertIsNotNone(self.atlas.workbook)
        self.assertIsNotNone(self.atlas.excel_url)
        self.assertTrue(self.atlas.excel.file.readable())


class TestSave(TestFoodAtlasRetriever):
    def testSave(self):
        """
        Tests that save method writes a reasonably sized file to disk
        """
        self.atlas.load()
        self.atlas.clean()
        self.assertIsNone(self.atlas.excel)
        self.atlas.save(self.pickle)
        self.assertGreater(os.path.getsize(self.pickle), 1000000)


class TestLoad(TestFoodAtlasRetriever):
    def testLoad(self):
        """
        Tests that the load method retrieves at least one data frame
        """
        self.atlas.load(self.pickle)
        self.assertGreater(len(self.atlas.data), 1)


if __name__ == '__main__':
    unittest.main()
