from pandasdmx import Request
import pandas as pd

# Convert all JSON datasets with a frequency domain into multi-indexed CSV files

# where to save or read
jsonDir = 'OECD_json_datasets/'
csvDir = 'OECD_csv_datasets_A/'
freqKeysFile = 'OECD_keys/FREQ_key_names.csv'
unicodeErrorFile = 'error_reports/freq_unicode_errors.csv'
keyErrorFile = 'error_reports/freq_key_errors.csv'

# OECD data
oecd = Request('OECD')

# note where pandasdmx fails
unicodeErrors = []
keyErrors = []
missingFiles = []

# Load a list of data set ids which support the frequency domain
dataset_ids_df = pd.read_csv(freqKeysFile)

# iterate through each supporting JSON file and convert it
# NOTE: we are working the the schema list going though frequency supporting data
# however the OECD data warehouse might not have been able to deliver the data, and so doesn't exist

for index, row in dataset_ids_df.iterrows():
    dataset_id = row['KeyFamilyId']
    freq_dim_name = row['Dimension']
    try:
        data_response = oecd.data(fromfile=jsonDir + dataset_id + '.json')
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
        df.to_csv(csvDir + dataset_id + '_A.csv')

print("completed ...")
print(len(missingFiles), 'missing files out of', len(dataset_ids_df.index))
print(len(unicodeErrors), 'UnicodeDecodeError')
print(len(keyErrors), 'KeyError')
print()
