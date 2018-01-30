import requests
import pandas as pd
import lxml.etree as etree
from tqdm import tqdm
import logging
import datetime

# http://stats.oecd.org/restsdmx/sdmx.ashx/GetSchema/
# Get and save the xml schema for each KeyFamily ID
# Should complete in around seven minutes

# where to save or read
logfile = 'logs/oecd_schema.log'
storedir = 'OECD_schema/'
keyNamesFile = 'OECD_keys/OECD_key_names.csv'

# logging
logging.basicConfig(filename=logfile, filemode='w', level=logging.DEBUG)
logging.debug("Log started at %s", str(datetime.datetime.now()))

# get the XML schema for each key family (dataset) id
schemaUrl = 'http://stats.oecd.org/restsdmx/sdmx.ashx/GetSchema/'

# use Key Family IDs to get Schema for that ID
df = pd.read_csv(keyNamesFile)
keynames = df['KeyFamilyId'].tolist()

success_count = 0

with requests.Session() as s:
    for keyname in tqdm(keynames):
        try:
            r = s.get(schemaUrl + keyname, timeout=61)
        except requests.exceptions.ReadTimeout:
            print(keyname, ": Data request read timed out")
            logging.debug('%s: Data read timed out', keyname)
        except requests.exceptions.Timeout:
            print(keyname, ": Data request timed out")
            logging.debug('%s: Data request timed out', keyname)
        except requests.exceptions.HTTPError:
            print(keyname, ": HTTP error")
            logging.debug('%s: HTTP error', keyname)
        except requests.exceptions.ConnectionError:
            print(keyname, ": Connection error")
            logging.debug('%s: Connection error', keyname)
        else:
            if r.status_code == 200:
                target = storedir + keyname + ".xml"
                tree = etree.fromstring(r.text)
                pretty_xml_str = etree.tostring(tree, pretty_print=True).decode("utf-8")
                with open(target, 'w', encoding='utf-8') as f:
                    f.write(pretty_xml_str)
                    success_count += 1
            else:
                print(keyname, r.status_code)
                logging.debug('%s HTTP Failed with code %d', keyname, r.status_code)

print("completed ...")
print(len(keynames), " Key Names")
print(success_count, " schema retrieved")
logging.debug("Log ended at %s", str(datetime.datetime.now()))
