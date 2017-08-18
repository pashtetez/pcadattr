#Заменяет refPointSize на 1.0 (размер PNP)
#и soldeerSwell на 0.01

def refPointSize_and_soldeerSwell(self):
    pcbDesignHeader = findPath(self.fdata, ["pcbDesign", "pcbDesignHeader"])[0]
    if findAll(pcbDesignHeader,"refPointSize") == []:
        pcbDesignHeader.append(["refPointSize","1.0"])
    else:
        find(pcbDesignHeader,"refPointSize")[1]="1.0"
    if findAll(pcbDesignHeader,"solderSwell") == []:
        pcbDesignHeader.append(["solderSwell","0.01"])
    else:
        find(pcbDesignHeader,"solderSwell")[1]="0.01"
