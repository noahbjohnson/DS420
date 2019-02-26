import unittest
import pkg_resources

from pandas import DataFrame

from src.midterm import AtlasCountyParser


class TestCached(unittest.TestCase):
    def runTest(self):
        self.parser = AtlasCountyParser()
        self.assertIsInstance(self.parser.dataFrame, DataFrame)


class TestNoCache(unittest.TestCase):
    def runTest(self):
        self.parser = AtlasCountyParser(use_cached=False)
        self.assertIsInstance(self.parser.dataFrame, DataFrame)


class TestNoCachePath(unittest.TestCase):
    def runTest(self):
        self.parser = AtlasCountyParser(use_cached=False, custom_cache_file=pkg_resources.resource_filename(__name__,
                                                                                                            "data/atlas_data.pickle"))
        self.assertIsInstance(self.parser.dataFrame, DataFrame)
