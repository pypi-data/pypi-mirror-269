import json
import utils.CONST as C
from numpyencoder import NumpyEncoder

def writeToFile(filename, content):
    try:
        with open(filename, "w", encoding=C.ENCODING) as f:
            f.write(content)
        return True
    except Exception as e:
        return False

def writeJsonToFile(filename, jsonContent):
    try:
        with open(filename, "w", encoding=C.ENCODING) as f:
            f.write(json.dumps(jsonContent, cls=NumpyEncoder))
        return True
    except Exception as e:
        return False

def readJsonFromFile(filename):
    try:
        with open(filename, "r", encoding=C.ENCODING) as f:
            data = json.load(f)
            return data
    except Exception as e:
        return {}
    
def getCLIArgurment(arg, name):
    try:
        return arg[name]
    except:
        return C.NULLSTRING