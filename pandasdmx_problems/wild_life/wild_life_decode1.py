import json

with open('WILD_LIFE_AUS.json') as json_file:
    data = json.load(json_file)

    # observations
    dataSets = data['dataSets']

    action = dataSets[0]['action']
    print('dataSets: action:', action)

    print('dataSets: observations')
    observations = dataSets[0]['observations']
    for obs, obsList in observations.items():
        print(obs, obsList)

    # structure
    structure = data['structure']

    name = structure['name']
    print('structure: name:', name)
    description = structure['description']
    print('structure: description:', description)

    # structure: dimensions
    print()
    print('structure: dimensions')
    dimensions = structure['dimensions']
    structDimObs = dimensions['observation']
    for structDimOb in structDimObs:
        print()
        print('keyPosition:', structDimOb['keyPosition'], 'id:', structDimOb['id'], 'name:', structDimOb['name'])
        structDimObValues = structDimOb['values']
        for structDimObValue in structDimObValues:
            print(structDimObValue['id'], structDimObValue['name'])

    # structure: attributes
    print()
    print('structure: attributes')
    attributes = structure['attributes']
    structAttObs = attributes['observation']
    for structAttOb in structAttObs:
        print('id:', structAttOb['id'], 'name:', structAttOb['name'])
        structAttOnValues = structAttOb['values']
        for structAttOnValue in structAttOnValues:
            print(structAttOnValue['id'], structAttOnValue['name'])

    print()

print('completed ...')
