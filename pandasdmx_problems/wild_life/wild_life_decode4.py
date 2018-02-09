import json
import math
import pandas as pd

with open('WILD_LIFE.json') as json_file:
    data = json.load(json_file)

    # observation format 0:0:0 [ 401, null, 0, 0, null]
    # IUCN category : species:  country [ value, ?, ?, ?, ?]

    # extract index column and column names
    structure = data['structure']
    dimensions = structure['dimensions']

    # Uses key position 'id', but could use 'name' instead
    keyNamesList = []
    keysList = []

    structDimObs = dimensions['observation']
    for structDimOb in structDimObs:
        keyPosition = structDimOb['keyPosition']
        keyNamesList.append(structDimOb['name'])
        idList = []
        for structDimObValue in structDimOb['values']:
            idList.append(structDimObValue['id'])
        keysList.append(idList)

    pass

print()
print("completed ...")
