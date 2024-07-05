import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from datetime import datetime, timedelta
import requests
import logging
import json
import vixupdate

DATASET_NAME = 'jatinsh/nifty-50-index-2000-2024'
FILE_NAME = 'NIFTY50_2000_to_2024.csv'

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def authenticate_kaggle():
    logger.info("Authenticating Kaggle API client...")
    df = pd.read_csv("path")
    df.drop()
    kaggle_json_path = os.path.join(os.path.expanduser("~"), ".kaggle", "kaggle.json")

    if not os.path.exists(kaggle_json_path):
        logger.error("kaggle.json not found. Please ensure it is in the ~/.kaggle/ directory.")
        raise FileNotFoundError("kaggle.json not found.")

    if not os.access(kaggle_json_path, os.R_OK):
        logger.error("kaggle.json does not have read permissions. Please update the file permissions.")
        raise PermissionError("kaggle.json does not have read permissions.")

    api = KaggleApi()
    try:
        api.authenticate()
        logger.info("Kaggle API client authenticated")
    except Exception as e:
        logger.error("Kaggle API authentication failed: {}".format(e))
        raise e

    return api


def load_dataset(api, dataset_path):
    logger.info("Downloading and loading existing dataset from Kaggle...")
    api.dataset_download_file(DATASET_NAME, FILE_NAME, path=dataset_path)
    df = pd.read_csv(os.path.join(dataset_path, FILE_NAME))
    logger.info("Loaded dataset with {} rows".format(len(df)))
    return df


def get_last_date(df):
    logger.info("Getting last date in the dataset...")
    last_date = pd.to_datetime(df['Date']).max()
    logger.info("Last date: {}".format(last_date))
    return last_date


def fetch_nifty_data(start_date, end_date):
    logger.info("Fetching NIFTY50 data for {} to {}".format(start_date, end_date))
    url = 'https://www.niftyindices.com/Backpage.aspx/getHistoricaldatatabletoString'
    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'referer': 'https://www.nseindia.com/reports-indices-historical-vix',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        "cookie": "ASP.NET_SessionId=3tlufmmwwnv51spwkzbr0uda; _gid=GA1.2.795213390.1720076992; _gat_gtag_UA_171440393_1=1; _ga_GWBG20V2KQ=GS1.1.1720102906.10.0.1720102906.0.0.0; _ga=GA1.1.1723573675.1719848953; bm_mi=C2EE712DEA229B16288377507BD3AC27~YAAQZzLUF2ntLnqQAQAA7Woffhil7+/VH58KN/eaczQIWbF2cNNUOB8vR/34MiormSndWQH3r1upofH91BZR/W3XFWr+sSF5zrLxU/hYHMffb2gBBupAarYUdU5wR0eNd72FVhlb65OD1FEVjoQ9JdmlVanuF4YipH2/iLbvSXT+M5qhlvF8t6rFh+SUrr+NHce+hno7UDDmwuN/GnpV7Ioq57jt33AetC61syFbAnB+OLP0aNeTuMDH2AD/Q5TGeOqGNFKVO0Lsa8Zgcm3VoUiEOY+5BHoqqMPJkGnf5VdL/pBgBy5wPuQCDIOmRYz6BXBebA==~1; ak_bmsc=D934705477C0D9E76421EC82F09F0F6A~000000000000000000000000000000~YAAQZzLUF33tLnqQAQAAM20ffhjz2j0goWCWC1uBu1SAREbFkzQQ2SkinS8v8tfPcjhrUUHeAiAOkGO9oAOW0PAKbEcxik+y/8KwAzSBubUShfwGlFVGUnDJUVqegV7MG7Lu3/x5/E433xlFahrmwuusYS5fOrP/JUrXnyC/fxNohycGAd/7KWN2lTttQ7LRwrOCVIVj3sspUHXQIjW/xXEX5gMjflAG/sSERRmkolGMhhnb7hrMisfCs6eYG5bkfapiZWrxi+qwdkUZ3GiMDhi4IhuMJMb6LvRZuHMFRzgm6gtw6hqUMobVy5520kQfBI08O9HxttkiddP1HLH8b9N2g5HccbtkElmX8nqyE9R9EhmzzlvughhRDDpmp4GLr2PfZCHLop/tG+OB55ZLvKDgniigec/ANcu1SS8otrhxiMGDCVnMV+5pi8QhPQ2JU+9+4Q==; bm_sv=2B969A7AF1F46E4F219EF5E335CE37C9~YAAQZzLUF8btLnqQAQAAfXkffhgAqwxCLu3rxSqpEFEHVcVBeEWZEHQaMZ5DB8MOlXtvvVfvjVtNuo1j5hQqZ2C+HCeFIuNG6EUGh8dJvedkTYXCXUL2Ihb+cgZiIID0ISwCjNNACRCVoHnHo8iBcn4FFDvZnmf1pGglsKkdbBNLQOmzQmFI8yIGU/s620kBugz3tG9MqnchvPJeh0BNNNybkejQ8u6kAqS64qqvF89VicoREl+WXxbOYAM9bvZnadwCj9m2~1",
    }
    body = {
        "cinfo": "{'name':'NIFTY 50','startDate':'" + start_date + "','endDate':'" + end_date + "','indexName':'NIFTY 50'}"
    }
    logger.info(f"request body --> {body}")
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    data = response.json()
    logger.info(f"response body <-- {data}")
    historical_data = json.loads(data['d'])
    return historical_data


def update_dataset(df, new_data):
    logger.info("Updating dataset with new data...")
    new_df = pd.DataFrame(new_data)
    new_df.drop(columns=['Index Name', 'RequestNumber'], errors='ignore', inplace=True)
    new_df.rename(columns={
        'HistoricalDate': 'Date',
        'OPEN': 'Open',
        'HIGH': 'High',
        'LOW': 'Low',
        'CLOSE': 'Close',
        'INDEX_NAME': 'Index Name'
    }, inplace=True)

    new_df['Date'] = pd.to_datetime(new_df['Date'], format='%d %b %Y')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')

    df = pd.concat([df, new_df]).drop_duplicates(subset='Date', keep='last')
    df = df.sort_values(by='Date')
    df.drop(columns=['INDEX_NAME', 'RequestNumber'], errors='ignore', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['Index Name'] = df['Index Name'].str.upper()
    logger.info("Updated dataset with {} rows".format(len(df)))
    return df


def save_dataset(df, filename):
    logger.info("Saving updated dataset to file...")
    df.to_csv(filename, index=False)
    logger.info("Dataset saved to file")


def create_metadata_file(folder, version_notes):
    description = """
Historical data for NIFTY50 and INDIA VIX index from 2000 to present. Sources: 
* https://www.nseindia.com/reports-indices-historical-index-data
* https://www.niftyindices.com/reports/historical-data
* https://www.nseindia.com/reports-indices-historical-vix
    """
    metadata = {
        "id": "jatinsh/nifty-50-index-2000-2024",
        "description": description,
        "license": "CC0-1.0",
        "keywords": ["NIFTY50", "NSE", "Indian Stock Market", "Historical Data"],
        "version_notes": version_notes,
    }

    metadata_path = os.path.join(folder, 'dataset-metadata.json')
    with open(metadata_path, 'w') as f:
        json.dump(metadata, f, indent=4)
    logger.info(f"Metadata file created at {metadata_path}")


def upload_to_kaggle(api, folder):
    logger.info("Creating a new version of the dataset on Kaggle...")
    version_date = datetime.today().strftime('%Y-%m-%d')
    version_notes = f"v{version_date}"
    create_metadata_file(folder, version_notes)

    api.dataset_create_version(
        folder=folder,
        version_notes=version_notes,
        convert_to_csv=True,
        dir_mode='skip'
    )
    logger.info("Dataset version created successfully.")


def main():
    api = authenticate_kaggle()
    dataset_path = './datasets'
    # if not os.path.exists(dataset_path):
    #     os.makedirs(dataset_path)

    # df = load_dataset(api, dataset_path)
    # df = df.head(-1)
    # last_date = get_last_date(df)
    # start_date = (last_date + timedelta(days=1)).strftime('%d-%b-%Y')
    # end_date = datetime.today().strftime('%d-%b-%Y')
    # new_data = fetch_nifty_data(start_date, end_date)
    # df = update_dataset(df, new_data)
    # save_dataset(df, os.path.join(dataset_path, FILE_NAME))
    # vixupdate.get_and_save(os.path.join(dataset_path, 'vix_data.csv'))
    upload_to_kaggle(api, dataset_path)


if __name__ == '__main__':
    main()
