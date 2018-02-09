from pandasdmx import Request
import pandas as pd
from collections import OrderedDict


# generator of empty lists
def create(n, constructor=list):
    for _ in range(n):
        yield constructor()


# use abbreviated column names or not
abbreviatedColumnNames = False

# data set ID
dataset_id = 'AMNE_IN'
# dataset_id = 'FFS_IND'
# dataset_id = 'AEO11_INDEPTH_CHAPTER6_TAB2_EN'

# set-up data source
oecd = Request('OECD')

print(dataset_id, 'data set loading ...')
try:
    data_response = oecd.data(resource_id=dataset_id, key='all/all')
except UnicodeDecodeError:
    print(dataset_id, 'load failed with UnicodeDecodeError')
except KeyError:
    print(dataset_id, 'load failed with KeyError')
else:
    print(dataset_id, 'loaded successfully')
    oecd_data = data_response.data

    if oecd_data.dim_at_obs == 'TIME_PERIOD':
        series_list = list(oecd_data.series)
        print(dataset_id, 'has', len(series_list), 'entries')
        print()

        # variable series key columns for the data set
        # list of empty lists
        key_columns = list(create(oecd_data._reader._key_len))

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
                for entry_dict in keys_list:
                    if entry_dict['id'] == key_code:
                        key_col_codes.append(entry_dict['name'])

            obs_dict = s_elem_dict['observations']
            for key, val_list in sorted(obs_dict.items()):
                value_col.append(val_list[0])
                yr = obs_dim_dict[int(key)]['name']
                time_period_col.append(yr)
                for ky in range(oecd_data._reader._key_len):
                    key_columns[ky].append(key_col_codes[ky])

        pandasdict = OrderedDict()

        tp = 'Time Period'
        ob = 'Observation'
        if abbreviatedColumnNames:
            tp = 'TIME_PERIOD'
            ob = 'OBS'

        pandasdict[tp] = time_period_col
        pandasdict[ob] = value_col

        for t in range(oecd_data._reader._key_len):
            if abbreviatedColumnNames:
                # use this for abbreviated column names
                pandasdict[s_key_tuple._fields[t]] = key_columns[t]
            else:
                # use this for un-abbreviated column names
                pandasdict[s_reader._series_dim[t]['name']] = key_columns[t]

        oecdDF = pd.DataFrame(pandasdict)
        oecdDF.set_index(tp, inplace=True)
        oecdDF.to_csv(dataset_id + '.csv')
        print('Successfully saved data frame to', dataset_id, '.csv')
    else:
        print(dataset_id, 'data set has no time period observations.')

print()
print("completed ...")
