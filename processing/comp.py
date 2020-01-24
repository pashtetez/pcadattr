from processing.find_utils import *
import math


class Comp:
    def __init__(self, data=None, compdefmap=None):
        self.raw_data = data
        self.name = find(data, "refDesRef")[1]
        self.compdefname = find(data, "patternRef")[1]
        self.point_x, self.point_y = mfloat(find(data, "pt")[1]), mfloat(find(data, "pt")[2])
        self.rotaion = 0
        try:
            self.rotaion = math.radians(float(find(data, "rotation")[1]))
        except:
            pass
        self.compdef = compdefmap[self.compdefname]
        self.side = "TOP"
        try:
            if find(data, "isFlipped"):
                self.side = "BOTTOM"
        except:
            pass
        self.pads = []
        for p in compdefmap[self.compdefname].pads:
            x_relative = p[0] * math.cos(self.rotaion) - p[1] * math.sin(self.rotaion)
            y_relative = p[1] * math.cos(self.rotaion) + p[0] * math.sin(self.rotaion)
            self.pads.append({"x": x_relative, "y": y_relative, "h": p[2].hole_diam})

