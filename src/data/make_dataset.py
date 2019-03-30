# -*- coding: utf-8 -*-
import logging
from pathlib import Path
from shutil import copyfileobj
from urllib.request import urlopen
import pandas as pd
import pkg_resources
import requests
from bs4 import BeautifulSoup
from xlrd import open_workbook


# @click.command()
# @click.argument('input_filepath', type=click.Path(exists=True))
# @click.argument('output_filepath', type=click.Path())
def main():
    """ Runs data processing scripts to download USDA data and parse it into pandas
    """

    # Get downloads page from USDA site
    logger.info('Scraping USDA.GOV for the download link')
    try:
        page = requests.get(atlas_url)
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
        excel_url = "https://www.ers.usda.gov{}".format(link["href"])

    # Download the excel file
    logger.info('Excel file found, beginning download')
    with open(excel_file_name, "wb") as excel:
        with urlopen(excel_url) as source:
            copyfileobj(source, excel)

    # Parse the excel sheets into dataframes
    logger.info('Download Complete, parsing excel file into pandas')
    data = {}
    with open_workbook(excel_file_name) as workbook:
        for sheet in range(len(workbook.sheet_names())):
            data[workbook.sheet_names()[sheet]] = pd.read_excel(
                excel.name, sheet_name=sheet)

    # load the fips lookup table from file
    fips_reference = pd.read_csv(fips_file,
                                 encoding='latin-1')

    # Joins all of the county-level tables into a single data frame
    logger.info('Joining excel sheets')
    to_join = [x for x in data.keys()
               if x not in
               ['Read_Me', 'Variable List', 'Supplemental Data - State']]

    out_frame = pd.DataFrame(
        index=fips_reference['FIPS Code'].unique())
    for df in to_join:
        d_prime = data[df].rename(str.strip, axis='columns')
        d_prime.index = d_prime['FIPS']
        d_prime = d_prime.drop(['FIPS', 'State', 'County'], axis='columns')
        out_frame = out_frame.join(d_prime)

    # State supplemental data
    state_frame = pd.DataFrame(
        index=fips_reference['FIPS Code'].unique())
    state_frame['StateFIPS'] = [int(str(x)[:2]) for x in state_frame.index.get_values()]
    state_frame = state_frame.join(data['Supplemental Data - State'], on='StateFIPS', rsuffix=" STATE")
    state_frame = state_frame.drop(['State'], axis='columns')
    out_frame = out_frame.join(state_frame)

    # Save the dataframe to pickle file
    logger.info('Saving dataset to pickle')
    out_frame.to_pickle(interim_pickle)

    # Create a data dictionary for variables
    logger.info('Creating data dictionary')
    dd = data['Variable List']
    dd.index = dd['Variable Code']

    logger.info('saving data dictionary to pickle')
    # save data dictionary to pickle
    dd.to_pickle(interim_pickle_dd)

    return


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    atlas_url = "https://www.ers.usda.gov/data-products/food-environment-atlas/data-access-and-documentation" \
                "-downloads"
    excel_file_name = Path.joinpath(project_dir, "data/raw/usda.xlsx")
    interim_pickle = Path.joinpath(project_dir, "data/interim/usda.pickle")
    interim_pickle_dd = Path.joinpath(project_dir, "data/interim/usda_dictionary.pickle")
    fips_file = Path.joinpath(project_dir, "data/external/county.csv")

    logger = logging.getLogger(__name__)
    logger.info('Getting data from the USDA')

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    # load_dotenv(find_dotenv())

    main()
