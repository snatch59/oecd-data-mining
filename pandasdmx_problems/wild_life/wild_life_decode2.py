import json
import math
import pandas as pd

with open('WILD_LIFE_AUS.json') as json_file:
    data = json.load(json_file)

    # observation format 0:0:0 [ 401, null, 0, 0, null]
    # IUCN category : species:  country [ value, ?, ?, ?, ?]

    # extract index column and column names
    structure = data['structure']
    dimensions = structure['dimensions']

    keyNamesList = []   # key position names ['IUCN category', 'species',  'country'] for 0, 1, 2
    indexRowsList = []  # IUCN category values, unique, one per row, which will be the index column
    colNamesList = []   # names of the columns ['Mammals', 'Birds', 'Reptiles', 'Amphibians', etc ]
    countryList = []    # names of the countries

    structDimObs = dimensions['observation']
    for structDimOb in structDimObs:
        keyPosition = structDimOb['keyPosition']
        keyNamesList.append(structDimOb['name'])
        if keyPosition == 0:
            for structDimObValue in structDimOb['values']:
                indexRowsList.append(structDimObValue['name'])
        elif keyPosition == 1:
            for structDimObValue in structDimOb['values']:
                colNamesList.append(structDimObValue['name'])
        elif keyPosition == 2:
            for structDimObValue in structDimOb['values']:
                countryList.append(structDimObValue['name'])

    # create the initial data frame
    indexDict = dict([(keyNamesList[0], indexRowsList)])

    colDictsList = []
    colDictsList.append(indexDict)

    # extract data for each column in order
    dataSets = data['dataSets']
    obsDict = dataSets[0]['observations']

    # one country at the moment
    totRows = len(indexRowsList)
    totCols = len(colNamesList)
    country = 0
    # emptyCol = [None] * len(indexRows)

    for c in range(totCols):
        colValsList = []
        for r in range(totRows):
            oKey = "%d:%d:%d" % (r, c, country)
            try:
                colValsList.append(obsDict[oKey][0])
            except KeyError:
                colValsList.append(math.nan)
        colDict = dict([(colNamesList[c], colValsList)])
        colDictsList.append(colDict)

    indx = list(indexDict.keys())[0]
    table = {}
    for elem in colDictsList:
        table.update(elem)

    df = pd.DataFrame(table)
    df.set_index(indx, inplace=True)
    print(df)
    # df.to_csv('WILD_LIFE_AUS.csv')

print()
print("completed ...")
