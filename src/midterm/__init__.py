import pickle
from os import path
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
from urllib3.request import RequestMethods

import pandas as pd
import pkg_resources
import requests
from bs4 import BeautifulSoup
# from pandas.tests.extension.test_datetime import data
from xlrd import open_workbook

atlas_url = "https://www.ers.usda.gov/data-products/food-environment-atlas/data-access-and-documentation" \
    "-downloads"


# TODO: Document FoodAtlasRetriever usage
class FoodAtlasRetriever:
    """A class to retrieve the most recent data from the USDA's Food Environment Atlas"""

    def __init__(self, url=atlas_url):
        self.url = url
        self.workbook = None
        self.data = {}
        self.excel_url = None
        self.excel = NamedTemporaryFile(delete=False, suffix='.xls')

    def __get_current_version(self):
        # Get downloads page from USDA site
        try:
            page = requests.get(self.url)
        except ConnectionError:
            raise requests.exceptions.ConnectionError(
                "Could not connect to the USDA site")

        # Parse download page
        try:
            soup = BeautifulSoup(page.text, 'html.parser')
            row = soup.find("td", {
                "class": "DataFileItem"
            })
            link = row.find("a")
            assert link.text == "Data Download"
        except (AssertionError, AttributeError):
            raise FileNotFoundError("Could not find the USDA source file")
        else:
            self.excel_url = "https://www.ers.usda.gov{}".format(link["href"])

    def __download_excel(self):
        with RequestMethods.urlopen(self.excel_url) as fsrc:
            copyfileobj(fsrc, self.excel)

    def __parse_excel(self):
        self.workbook = open_workbook(self.excel.name)

    def __create_frames(self):
        for sheet in range(len(self.workbook.sheet_names())):
            sheet_name = self.workbook.sheet_names()[sheet]
            self.data[sheet_name] = pd.read_excel(
                self.excel.name, sheet_name=sheet)

    def clean(self):
        """Removes the temporary download files and raw copy of the data. Does not delete the .data"""
        self.workbook = None
        try:
            self.excel.close()
            self.excel = None
        except AttributeError:
            return False

    def save(self, filename):
        """Saves the data from the atlas retriever to a pickle file.

        :param filename: The pickle file name to save the data to
        :type filename: str
        """
        with open(filename, "wb") as f:
            pickle.dump(self.data, f)

    def get(self):
        """Queries the USDA site for the newest version of the atlas data and downloads it."""
        self.__get_current_version()
        self.__download_excel()
        self.__parse_excel()
        self.__create_frames()

    def load(self, filename=""):
        """Loads downloaded and saved data file pickle. Defaults to package data

        :param filename: Pickle file containing the previously downloaded data
        :type filename: str
        """
        if filename != "":
            file_path = filename
        else:
            file_path = pkg_resources.resource_filename(__name__,
                                                        "data/atlas_data.pickle")
        with open(file_path, 'rb') as f:
            self.data = pickle.load(f)


# TODO: Document DataDictionary usage
class DataDictionary(pd.DataFrame):
    """Creates a single data frame acting as a data dictionary for the food atlas data

    :param atlas_obj: The FoodAtlasRetriever object to build a dictionary for
    """

    def __init__(self, atlas_obj):
        """
        Creates the data dictionary

        :type atlas_obj: FoodAtlasRetriever
        """
        if not isinstance(atlas_obj, FoodAtlasRetriever):
            raise TypeError(
                "DataDictionary object must take FoodAtlasRetriever object as parameter")
        else:
            frame = atlas_obj.data['Variable List']
            frame.index = frame['Variable Code']
            super().__init__(frame)

    def get_props(self):
        """
        Returns a list of all the properties (columns) in the data dictionary

        :return: list
        """
        return self.columns.tolist()

    def get_vars(self):
        """
        Returns a list of all the variables (rows index) in the data dictionary

        :return: list
        """
        return self.index.tolist()

    def get_variable_properties(self, variable, prop_list=None):
        """
        Takes the name of a variable and returns the specified properties for it

        :param variable: The variable to get properties of
        :type variable: str
        :param prop_list: The properties to return
        :return: dict
        """
        if isinstance(prop_list, list):
            get_props = prop_list
        elif prop_list:
            raise TypeError("prop_list argument must be a list")
        else:
            get_props = self.get_props()

        if variable not in self.get_vars():
            raise IndexError("{} not in variable list: {}".format(
                variable, self.get_vars()))
        variable_row = self.loc[variable].to_dict()
        result = {}
        for p in get_props:
            if p in self.get_props():
                result[p] = variable_row[p]
        return result


# TODO: Document AtlasCountyParser usage
# TODO: Complete AtlasCountyParser test coverage
class AtlasCountyParser:
    """Creates a single data frame from a FoodAtlasRetriever object with county-level data. If loading from cache, \
    data from the package will be used unless another file is specified

    :param use_cached: If true, the parser will attempt to load cached data.
    :param custom_cache_file: If true, the parser will attempt to load cached data.
    """

    def __init__(self,
                 use_cached=True,
                 custom_cache_file=""
                 ):

        self.atlas = FoodAtlasRetriever()

        if not use_cached:
            self.atlas.get()
        else:
            if path.isfile(custom_cache_file):
                self.atlas.load(custom_cache_file)
            else:
                self.atlas.load()

        self.dataFrame = pd.DataFrame()

        self.data_dictionary = DataDictionary(self.atlas)

        self.fips_reference = pd.read_csv(pkg_resources.resource_filename(__name__,
                                                                          "data/county.csv"),
                                          encoding='latin-1')

        self._join_tables()

    def _join_tables(self):
        """Joins all of the county-level tables into a single data frame"""
        to_join = [x for x in self.atlas.data.keys()
                   if x not in
                   ['Read_Me', 'Variable List', 'Supplemental Data - County', 'Supplemental Data - State']]

        self.dataFrame = pd.DataFrame(
            index=self.fips_reference['FIPS Code'].unique())

        for df in to_join:
            d_prime = self.atlas.data[df]
            d_prime.index = d_prime['FIPS']
            d_prime = d_prime.drop(['FIPS', 'State', 'County'], axis='columns')
            self.dataFrame = self.dataFrame.join(d_prime)


if __name__ == '__main__':
    atlas = FoodAtlasRetriever()
    atlas.get()
    atlas.save('data/atlas_data.pickle')
