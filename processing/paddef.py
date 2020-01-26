from processing.find_utils import *
from svg import *


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
        self.draw(self.raw_data)

    def draw(self, file_part):
        self.raw = file_part
        holeDiam = mfloat(find(file_part, "holeDiam")[1])
        holeOffset = (0, 0);
        if len(findAll(file_part, 'holeOffset')):
            holeOffset = (mfloat(findAll(file_part, 'holeOffset')[0][1]), mfloat(findAll(file_part, 'holeOffset')[0][2]))
        self.graphics = []
        for li in findAll(file_part, "padShape"):
            if len(findAll(li, 'layerNumRef')):
                mylay = findAll(li, 'layerNumRef')[0][1]
                if find(li, 'padShapeType')[1] == 'Polygon':
                    pds = findAll(find(li, 'shapeOutline'), 'pt')
                    self.graphics.append(Polygon([(mfloat(x[1]), mfloat(x[2])) for x in pds], holeDiam, holeOffset).layer(mylay))
                if find(li, 'padShapeType')[1] == 'Rect':
                    self.graphics.append(Rect(mfloat(find(li, 'shapeWidth')[1]), mfloat(find(li, 'shapeHeight')[1]), holeDiam, holeOffset).layer(mylay))
                if find(li, 'padShapeType')[1] == 'Oval':
                    self.graphics.append(Oval(mfloat(find(li, 'shapeWidth')[1]), mfloat(find(li, 'shapeHeight')[1]), holeDiam, holeOffset).layer(mylay))
                if find(li, 'padShapeType')[1] == 'Target':
                    self.graphics.append(Target(mfloat(find(li, 'shapeWidth')[1]), mfloat(find(li, 'shapeHeight')[1])).layer(mylay))
                if find(li, 'padShapeType')[1] == 'Ellipse':
                    self.graphics.append(Ellipse(mfloat(find(li, 'shapeWidth')[1]), mfloat(find(li, 'shapeHeight')[1]), holeDiam, holeOffset).layer(mylay))
                if find(li, 'padShapeType')[1] == 'RndRect':
                    self.graphics.append(RndRect(mfloat(find(li, 'shapeWidth')[1]), mfloat(find(li, 'shapeHeight')[1]), holeDiam, holeOffset).layer(mylay))
                if find(li, 'padShapeType')[1] == 'MtHole':
                    self.graphics.append(MtHole(mfloat(find(li, 'shapeWidth')[1]), mfloat(find(li, 'shapeHeight')[1])).layer(mylay))

    def get_graphics(self):
        return self.graphics