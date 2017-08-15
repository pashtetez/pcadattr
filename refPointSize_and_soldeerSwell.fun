#Заменяет refPointSize на 1.0 (размер PNP)
#и soldeerSwell на 0.01

def refPointSize_and_soldeerSwell(self):
    findPath(self.fdata, ["pcbDesign", "pcbDesignHeader","refPointSize"])[0][1]="1.0"
    findPath(self.fdata, ["pcbDesign", "pcbDesignHeader","solderSwell"])[0][1]="0.01"
