import pickle
from shutil import copyfileobj
from tempfile import NamedTemporaryFile
from urllib.request import urlopen
import pandas as _pd
import requests
from bs4 import BeautifulSoup
from xlrd import open_workbook


class FoodAtlasRetriever:
    """A class to retrieve the most recent data from the USDA's Food Environment Atlas"""
    def __init__(self):
        self.url = "https://www.ers.usda.gov/data-products/food-environment-atlas/data-access-and-documentation" \
                   "-downloads"
        self.workbook = None
        self.data = {}
        self.excel_url = None
        self.excel = NamedTemporaryFile(delete=False, suffix='.xls')

    def __get_current_version(self):
        # Get downloads page from USDA site
        try:
            page = requests.get(self.url)
        except ConnectionError:
            raise requests.exceptions.ConnectionError("Could not connect to the USDA site")

        # Parse download page
        soup = BeautifulSoup(page.text, 'html.parser')
        row = soup.find("td", {
            "class": "DataFileItem"
        })
        link = row.find("a")

        if link.text != "Data Download":
            raise FileNotFoundError("Could not find the USDA source file")
        else:
            self.excel_url = "https://www.ers.usda.gov{}".format(link["href"])
            print("url found")

    def __download_excel(self):
        print("downloading file")

        with urlopen(self.excel_url) as fsrc:
            copyfileobj(fsrc, self.excel)

        print("file downloaded")

    def __parse_excel(self):
        print("parsing file")
        self.workbook = open_workbook(self.excel.name)
        print("file parsed")

    def __create_frames(self):
        print("creating data frames")
        readme = 0
        for sheet in range(len(self.workbook.sheet_names())):
            sheet_name = self.workbook.sheet_names()[sheet]
            self.data[sheet_name] = _pd.read_excel(self.excel.name, sheet_name=sheet, header=readme)
            readme = 1
            self.data[sheet_name] = _pd.read_excel(self.excel.name, sheet_name=sheet)

    def clean(self):
        """Removes the temporary download files and raw copy of the data. Does not delete the .data"""
        self.workbook = None
        try:
            self.excel.close()
            self.excel = None
        except AttributeError:
            pass

    def save(self, filename: str):
        """Saves the data from the atlas retriever to a pickle file.

        :param filename: The pickle file name to save the data to
        """
        print("saving data")
        with open(filename, "wb") as f:
            pickle.dump(self.data, f)
        print("data saved to disk as: {}".format(filename))

    def get(self):
        """Queries the USDA site for the newest version of the atlas data and downloads it."""
        self.__get_current_version()
        self.__download_excel()
        self.__parse_excel()
        self.__create_frames()

    def load(self, filename: str):
        """Loads downloaded and saved data file pickle.

        :param filename: Pickle file containing the previously downloaded data
        """
        with open(filename, 'rb') as f:
            self.data = pickle.load(f)


if __name__ == '__main__':
    atlas = FoodAtlasRetriever()
    atlas.get()
    atlas.save('data/atlas_data.pickle')
