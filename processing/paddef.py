from processing.find_utils import *


class PadDef:
    def __init__(self, data=None):
        self.raw_data = data
        self.name = data[1]
        shape = find(data, 'padShape', ['layerNumRef', '1'])
        dx = 0.0
        dy = 0.0
        self.shapeType = find(shape, "padShapeType")[1]

        if self.shapeType != "Polygon":
            if findAll(shape, "shapeWidth"):
                dx = mfloat(find(shape, "shapeWidth")[1]) / 2
                dy = mfloat(find(shape, "shapeHeight")[1]) / 2
            elif findAll(shape, "outsideDiam"):
                dx = mfloat(find(shape, "outsideDiam")[1]) / 2
                dy = mfloat(find(shape, "outsideDiam")[1]) / 2
            else:
                dx = 0
                dy = 0
        else:
            outline = find(shape, "shapeOutline")[1:]
            dx = (max([mfloat(a[1]) for a in outline]) - min([mfloat(a[1]) for a in outline])) / 2
            dy = (max([mfloat(a[2]) for a in outline]) - min([mfloat(a[2]) for a in outline])) / 2
        self.hole_diam = mfloat(find(data, 'holeDiam')[1])
        self.dx = dx
        self.dy = dy
