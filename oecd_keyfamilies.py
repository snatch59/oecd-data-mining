import requests
import xmltodict
import pandas as pd
import logging
import datetime
import os

# http://stats.oecd.org/restsdmx/sdmx.ashx/GetDataStructure/ALL
# Extract OECD KeyFamily id (dataset id) and English description

# where to save
LOG_DIR = 'logs'
DATA_DIR = 'OECD_keys'

LOGFILE = os.path.join(LOG_DIR, 'oecd_keyfamilies.log')
DATAFILE = os.path.join(DATA_DIR, 'OECD_key_names.csv')

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# logging
logging.basicConfig(filename=LOGFILE, filemode='w', level=logging.DEBUG)
logging.debug("Log started at %s", str(datetime.datetime.now()))

# get the data structure schema with the key families (dataset ids)
dataStructureUrl = 'http://stats.oecd.org/RESTSDMX/sdmx.ashx/GetDataStructure/ALL/'

try:
    r = requests.get(dataStructureUrl, timeout=61)
except requests.exceptions.ReadTimeout:
    print("Data request read timed out")
    logging.debug('Data read timed out')
except requests.exceptions.Timeout:
    print("Data request timed out")
    logging.debug('Data request timed out')
except requests.exceptions.HTTPError:
    print("HTTP error")
    logging.debug('HTTP error')
except requests.exceptions.ConnectionError:
    print("Connection error")
    logging.debug('Connection error')
else:
    if r.status_code == 200:
        keyFamIdList = []
        keyFamNameList = []

        # use xmltodict and traverse nested ordered dictionaries
        keyfamilies_dict = xmltodict.parse(r.text)
        keyFamilies = keyfamilies_dict['message:Structure']['message:KeyFamilies']['KeyFamily']

        for keyFamily in keyFamilies:
            keyfam_id = keyFamily['@id']
            keyFamIdList.append(keyfam_id)
            keyNames = keyFamily['Name']
            if isinstance(keyNames, list):
                for keyName in keyNames:
                    try:
                        keyfam_lang = keyName['@xml:lang']
                        if keyfam_lang == 'en':
                            keyfam_text = keyName['#text']
                            keyFamNameList.append(keyfam_text)
                            # print(keyfam_id, keyfam_text)
                    except KeyError as e:
                        logging.debug("No @xml:lang/#text key in {}".format(keyName))
            elif isinstance(keyNames, dict):
                try:
                    keyfam_lang = keyNames['@xml:lang']
                    if keyfam_lang == 'en':
                        keyfam_text = keyNames['#text']
                        keyFamNameList.append(keyfam_text)
                        # print(keyfam_id, keyfam_text)
                except KeyError as e:
                    logging.debug("No @xml:lang/#text key in {}".format(keyNames))

        # create a 2D list(needed?), and a data frame. Save data frame to csv file
        # keyFamTable = [keyFamIdList, keyFamNameList]
        keyFamDF = pd.DataFrame({'KeyFamilyId': keyFamIdList, 'KeyFamilyName': keyFamNameList})
        keyFamDF.set_index('KeyFamilyId', inplace=True)
        keyFamDF.to_csv(DATAFILE)
    else:
        print('HTTP Failed with code', r.status_code)
        logging.debug('HTTP Failed with code %d', r.status_code)

print("completed ...")
logging.debug("Log ended at %s", str(datetime.datetime.now()))
