"""
Some functions we might need like
getting predictors from the data set and
converting them to int64
"""

# get the index of the target var
def GET_TARGET_INDEX(dataset, target):
    columns = dataset.columns.tolist()
    return columns.index(target)

# get predictors and targets for lists gui
def GET_PREDICTORS(dataset):
    predictors = []

    for column in dataset.columns:
        cl_type = dataset[column].dtype.name
        if cl_type == 'float64' or cl_type == 'int64':
            predictors.append(column)

    return predictors
