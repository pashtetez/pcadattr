#Test other function like refpointsize function


def test(pcad_file):
    s = open("other.txt", 'w')
    s.write('other')
    s.close()
    pcbDesignHeader = findPath(pcad_file.m_data, ["pcbDesign", "pcbDesignHeader"])[0]
    if findAll(pcbDesignHeader,"refPointSize") == []:
        pcbDesignHeader.append(["refPointSize","1.0"])
    else:
        find(pcbDesignHeader,"refPointSize")[1]="1.0"
    if findAll(pcbDesignHeader,"solderSwell") == []:
        pcbDesignHeader.append(["solderSwell","0.01"])
    else:
        find(pcbDesignHeader,"solderSwell")[1]="0.01"
