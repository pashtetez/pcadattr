def findAll(a,key,val = None):
    if val:
        return [x for x in a if x[0] == key and x[1] == val ]
    else:
        return [x for x in a if x[0] == key]


def find(a,key,val = None):
    return findAll(a,key,val)[0]


def findPath(a,path,lastval = None):
    b = a
    for x in path[:-1]:
        b = find(b,x)
    return findAll(b,path[-1],lastval)


def mfloat(s):
    if 'mm' in s:
        return float(s.replace('mm',''))/0.0254
    else:
        return float(s)