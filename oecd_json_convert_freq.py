from pandasdmx import Request
import pandas as pd
import os

# Convert all JSON datasets with a frequency domain into multi-indexed CSV files

# where to save or read

JSON_DIR = 'OECD_json_datasets'
CSV_DIR = 'OECD_csv_datasets_A'
DATA_DIR = 'OECD_keys'

FREQ_KEYS_FILE = os.path.join(DATA_DIR, 'FREQ_key_names.csv')
# unicodeErrorFile = 'error_reports/freq_unicode_errors.csv'
# keyErrorFile = 'error_reports/freq_key_errors.csv'

if not os.path.exists(CSV_DIR):
    os.makedirs(CSV_DIR)

# OECD data
oecd = Request('OECD')

# note where pandasdmx fails
unicodeErrors = []
keyErrors = []
missingFiles = []

# Load a list of data set ids which support the frequency domain
dataset_ids_df = pd.read_csv(FREQ_KEYS_FILE)

# iterate through each supporting JSON file and convert it
# NOTE: we are working the the schema list going though frequency supporting data
# however the OECD data warehouse might not have been able to deliver the data, and so doesn't exist

for index, row in dataset_ids_df.iterrows():
    dataset_id = row['KeyFamilyId']
    freq_dim_name = row['Dimension']
    try:
        data_response = oecd.data(fromfile=os.path.join(JSON_DIR, dataset_id + '.json'))
    except FileNotFoundError:
        missingFiles.append(dataset_id)
    except UnicodeDecodeError:
        unicodeErrors.append(dataset_id)
    except KeyError:
        keyErrors.append(dataset_id)
    else:
        oecd_data = data_response.data

        series_list = list(oecd_data.series)
        print(dataset_id, series_list[0].key)

        if freq_dim_name == 'FREQUENCY':
            print(set(s.key.FREQUENCY for s in oecd_data.series))
            annual = (anl for anl in oecd_data.series if anl.key.FREQUENCY == 'A')
        else:
            print(set(s.key.FREQ for s in oecd_data.series))
            annual = (anl for anl in oecd_data.series if anl.key.FREQ == 'A')
        print()

        df = data_response.write(annual)
        df.to_csv(os.path.join(CSV_DIR, dataset_id + '_A.csv'))

print("completed ...")
print(len(missingFiles), 'missing files out of', len(dataset_ids_df.index))
print(len(unicodeErrors), 'UnicodeDecodeError')
print(len(keyErrors), 'KeyError')
print()
