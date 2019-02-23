import unittest
from src.midterm import FoodAtlasRetriever
import requests
from tempfile import NamedTemporaryFile
import os


class TestFoodAtlasRetriever(unittest.TestCase):
    def setUp(self):
        self.atlas = FoodAtlasRetriever()

    def tearDown(self):
        self.atlas.clean()
        self.atlas = None

# Tests for initial values

class TestWorkbook(TestFoodAtlasRetriever):
    def runTest(self):
        self.assertIsNone(self.atlas.workbook)

class TestUrl(TestFoodAtlasRetriever):
    def runTest(self):
        url_test = requests.get(self.atlas.url)
        self.assertTrue(url_test.ok)

class TestData(TestFoodAtlasRetriever):
    def runTest(self):
        self.assertDictEqual(self.atlas.data, {})

class TestExcelUrl(TestFoodAtlasRetriever):
    def runTest(self):
        self.assertIsNone(self.atlas.excel_url)

class TestExcel(TestFoodAtlasRetriever):
    def runTest(self):
        self.assertTrue(self.atlas.excel.file._checkWritable())

# Test methods

class TestGet(TestFoodAtlasRetriever):
    def setUp(self):
        self.atlas = FoodAtlasRetriever()
        self.atlas.get()

    def testDataEmpty(self):
        self.assertIsNot(self.atlas.data, {})

    def testDataSingle(self):
        self.assertGreater(len(self.atlas.data), 1)

    def testWorkbook(self):
        self.assertIsNotNone(self.atlas.workbook)

    def testExcelUrl(self):
        self.assertIsNotNone(self.atlas.excel_url)

    def testExcel(self):
        self.assertTrue(self.atlas.excel.file.__checkReadable())

class TestOtherMethods(TestGet):
    def setUp(self):
        self.atlas = FoodAtlasRetriever()
        self.atlas.get()
        self.atlas.clean()
        self.pickle = NamedTemporaryFile(delete=False, suffix='.pickle')

    def testWorkbookNone(self):
        self.assertIsNotNone(self.atlas.workbook)

    def testExcelOpen(self):
        self.assertIsNone(self.atlas.excel)

    def testSave(self):
        self.atlas.save(self.pickle.name)
        self.assertGreater(os.path.getsize(self.pickle.name), 1000000)

    def testLoad(self):
        self.atlas = FoodAtlasRetriever
        self.atlas.load(self.pickle.name)
        self.assertGreater(len(self.atlas.data, 1))


if __name__ == '__main__':
    unittest.main()