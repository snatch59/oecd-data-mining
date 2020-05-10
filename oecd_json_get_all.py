import requests
import pandas as pd
from tqdm import tqdm
import logging
import datetime
import os

# http://stats.oecd.org/sdmx-json/data/<id>/all/all
# Get JSON datasets for all key families (dataset ids)

# where to save or read
LOG_DIR = 'logs'
STORE_DIR = 'OECD_json_datasets'
DATA_DIR = 'OECD_keys'

LOGFILE = os.path.join(LOG_DIR, 'oecd_datasets.log')
KEYNAMESFILE = os.path.join(DATA_DIR, 'OECD_key_names.csv')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

if not os.path.exists(STORE_DIR):
    os.makedirs(STORE_DIR)

# logfile = 'logs/oecd_datasets.log'
# storedir = 'OECD_json_datasets/'
# keyNamesFile = 'OECD_keys/OECD_key_names.csv'

# logging
logging.basicConfig(filename=LOGFILE, filemode='w', level=logging.DEBUG)
logging.debug("Log started at %s", str(datetime.datetime.now()))

# read in list of dataset ids
datasourceUrl = 'http://stats.oecd.org/sdmx-json/data/'

dataset_ids_df = pd.read_csv(KEYNAMESFILE)
dataset_ids = dataset_ids_df['KeyFamilyId'].tolist()

success_count = 0

with requests.Session() as s:
    for dataset_id in tqdm(dataset_ids):
        try:
            r = s.get(datasourceUrl + dataset_id + '/all/all', timeout=61)
        except requests.exceptions.ReadTimeout:
            print(dataset_id, ": OECD data request read timed out")
            logging.debug('%s: OECD data request read timed out', dataset_id)
        except requests.exceptions.Timeout:
            print(dataset_id, ": OECD data request timed out")
            logging.debug('%s: OECD data request timed out', dataset_id)
        except requests.exceptions.HTTPError:
            print(dataset_id, ": HTTP error")
            logging.debug('%s: HTTP error', dataset_id)
        except requests.exceptions.ConnectionError:
            print(dataset_id, ": Connection error", )
            logging.debug('%s: Connection error', dataset_id)
        else:
            if r.status_code == 200:
                # save the json file - don't prettify to save space
                target = os.path.join(STORE_DIR, dataset_id + ".json")
                with open(target, 'w', encoding='utf-8') as f:
                    f.write(r.text)
                    success_count += 1
            else:
                print(dataset_id, 'HTTP Failed with code', r.status_code)
                logging.debug('%s HTTP Failed with code %d', dataset_id, r.status_code)

print("completed ...")
print(len(dataset_ids), " Dataset Ids")
print(success_count, " datasets retrieved")
logging.debug("Log ended at %s", str(datetime.datetime.now()))
