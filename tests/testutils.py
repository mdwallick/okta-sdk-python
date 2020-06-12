# helper function to compare JSON documents
def json_compare(data1, data2):
    for key in data1.keys():
        if key in data2.keys():
            if type(data1[key]) == dict:
                if not json_compare(data1[key], data2[key]):
                    return False
        else:
            print("{0} not in data2.keys()...".format(key))
            return False
    return True
