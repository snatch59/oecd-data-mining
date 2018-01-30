from pandasdmx import Request
import pandas as pd
from collections import OrderedDict
import os

# Convert all JSON datasets into multi-indexed CSV files


# generator of empty lists
def create(n, constructor=list):
    for _ in range(n):
        yield constructor()


# note this function extracts annual data
# DataFrame in long format
def createDF(sdmx_data, useIDs=False):

    series_list = list(sdmx_data.series)

    # does it have a frequency dimension?
    # if only use the annual data
    keycheck_tuple = series_list[0].key._fields
    for keycheck in keycheck_tuple:
        if keycheck == 'FREQUENCY':
            series_list = (anl for anl in sdmx_data.series if anl.key.FREQUENCY == 'A')
            break
        elif keycheck == 'FREQ':
            series_list = (anl for anl in sdmx_data.series if anl.key.FREQ == 'A')
            break

    # variable series key columns for the data set
    # list of empty lists
    key_columns = list(create(sdmx_data._reader._key_len))

    # fixed columns for time period and values
    time_period_col = []
    value_col = []

    for s in series_list:
        s_key_tuple = s.key
        s_elem_dict = s._elem
        s_reader = s._reader

        obs_dim_dict = s_reader._obs_dim[0]['values']

        total_keys = s_reader._key_len
        key_col_codes = []

        for key in range(total_keys):
            keys_list = s_reader._series_dim[key]['values']
            key_field_abbrev = s_key_tuple._fields[key]
            key_code = s_key_tuple[key_field_abbrev]
            if useIDs:
                key_col_codes.append(key_code)
            else:
                for entry_dict in keys_list:
                    if entry_dict['id'] == key_code:
                        key_col_codes.append(entry_dict['name'])

        obs_dict = s_elem_dict['observations']
        for key, val_list in sorted(obs_dict.items()):
            value_col.append(val_list[0])
            yr = obs_dim_dict[int(key)]['name']
            time_period_col.append(yr)
            for ky in range(sdmx_data._reader._key_len):
                key_columns[ky].append(key_col_codes[ky])

    pandasdict = OrderedDict()

    tp = 'Time Period'
    ob = 'Observation'
    if useIDs:
        tp = 'TIME_PERIOD'
        ob = 'OBS'

    pandasdict[tp] = time_period_col
    pandasdict[ob] = value_col

    for t in range(sdmx_data._reader._key_len):
        if useIDs:
            # use this for abbreviated column names
            pandasdict[s_key_tuple._fields[t]] = key_columns[t]
        else:
            # use this for un-abbreviated column names
            pandasdict[s_reader._series_dim[t]['name']] = key_columns[t]

    oecdDF = pd.DataFrame(pandasdict)
    oecdDF.set_index(tp, inplace=True)

    return oecdDF


# where to save or read
jsonDir = 'OECD_json_datasets'
csvDir = 'OECD_csv_datasets/'
unicodeErrorFile = 'error_reports/unicode_errors.csv'
keyErrorFile = 'error_reports/key_errors.csv'
noTimePeriodFile = 'error_reports/no_time_period.csv'

# OECD data
oecd = Request('OECD')

# note where pandasdmx fails
unicodeErrors = []
keyErrors = []
noTimePeriod = []

# iterate through each JSON file in the directory and convert it
for filename in os.listdir(jsonDir):
    if filename.endswith(".json"):
        fname = os.path.splitext(filename)[0]
        try:
            data_response = oecd.data(fromfile=os.path.join(jsonDir, filename))
        except UnicodeDecodeError:
            unicodeErrors.append(fname)
        except KeyError:
            keyErrors.append(fname)
        else:
            data = data_response.data

            if data.dim_at_obs == 'TIME_PERIOD':
                df = createDF(data, useIDs=False)
                df.to_csv(csvDir + fname + '.csv')
            else:
                noTimePeriod.append(fname)

# log the issues
unicodeErrorsDF = pd.DataFrame({'UnicodeErrors': unicodeErrors})
unicodeErrorsDF.set_index('UnicodeErrors', inplace=True)
unicodeErrorsDF.to_csv(unicodeErrorFile)

keyErrorsDF = pd.DataFrame({'KeyErrors': keyErrors})
keyErrorsDF.set_index('KeyErrors', inplace=True)
keyErrorsDF.to_csv(keyErrorFile)

noTimePeriodDF= pd.DataFrame({'NoTimePeriod': noTimePeriod})
noTimePeriodDF.set_index('NoTimePeriod', inplace=True)
noTimePeriodDF.to_csv(noTimePeriodFile)

print("completed ...")
print(len(unicodeErrors), 'UnicodeDecodeError')
print(len(keyErrors), 'KeyError')
print(len(noTimePeriod), 'NoTimePeriod')
