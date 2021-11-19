import config as Config

def column(value):
    return int((Config.windowSize[0] / Config.displayColumns) * value)

def row(value):
    return int((Config.windowSize[1] / Config.displayRows) * value)