import pandas as pd
import xml.etree.ElementTree as ET
import os

# where to load or save
SCHEMA_DIR = 'OECD_schema'
DATA_DIR = 'OECD_keys'

KEY_NAMES_FILE = os.path.join(DATA_DIR, 'OECD_key_names.csv')
DATA_FILE = os.path.join(DATA_DIR, 'FREQ_key_names.csv')

# performance metrics
dataset_files_cnt = 0
has_datasettype_node_cnt = 0

# data to be collected
usable_datasets = []
frequency_keywords = []

# Load a list of data set ids
dataset_ids_df = pd.read_csv(KEY_NAMES_FILE)
dataset_ids = dataset_ids_df['KeyFamilyId'].tolist()

# go through each data set schema file and see if it
# support the FREQUENCY or FREQ dimension for observations
for dataset_id in dataset_ids:
    try:
        tree = ET.parse(os.path.join(SCHEMA_DIR, dataset_id + '.xml'))
    except FileNotFoundError:
        pass
    else:
        dataset_files_cnt += 1
        root = tree.getroot()

        childIndex = 0
        for rootChild in root:
            rootChildAttrib = rootChild.attrib
            if 'name' in rootChildAttrib:
                attribName = rootChildAttrib['name']
                if attribName == 'DataSetType':
                    # print(dataset_id, 'has DataSetType')
                    has_datasettype_node_cnt += 1
                    dstNode = root[childIndex][0][0]
                    for dstChild in dstNode:
                        dstChildAttrib = dstChild.attrib
                        if 'name' in dstChildAttrib:
                            dimension = dstChildAttrib['name']
                            # print(val2)
                            if dimension == 'FREQUENCY' or dimension == 'FREQ':
                                usable_datasets.append(dataset_id)
                                frequency_keywords.append(dimension)
                                print(dataset_id, 'pandasdmx usable with', dimension)

            childIndex += 1

if len(usable_datasets):
    usableDF = pd.DataFrame({'KeyFamilyId': usable_datasets, 'Dimension': frequency_keywords})
    usableDF.set_index('KeyFamilyId', inplace=True)
    usableDF.to_csv(DATA_FILE)

print()
print('completed ...')
print('Out of', dataset_files_cnt, 'data set files,', len(usable_datasets), 'are usable by pandasdmx.')
print(has_datasettype_node_cnt, 'have DataSetType nodes')
