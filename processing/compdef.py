from processing.find_utils import *
import math


class CompDef:
    def __init__(self, data=None, padmap=None):
        self.raw_data = data
        self.name = data[1]
        self.original_name = find(data, "originalName")[1]
        self.spads = 0
        self.dpads = 0
        self.xmaxl = 0.0
        self.xmaxr = 0.0
        self.ymaxb = 0.0
        self.ymaxt = 0.0
        self.pads = []
        for p in findPath(data, ["patternGraphicsDef", "multiLayer", "pad"]):
            pt = find(p, "pt")
            c = find(p, "padStyleRef")[1]
            dd = padmap[c]

            x = mfloat(pt[1])
            y = mfloat(pt[2])
            if dd.hole_diam:
                self.dpads += 1
            else:
                self.spads += 1
            if (self.spads + self.dpads) == 1:
                self.xmaxl = x - dd.dx
                self.xmaxr = x + dd.dx
                self.ymaxb = y - dd.dy
                self.ymaxt = y + dd.dy
            else:
                if self.xmaxl > x - dd.dx:
                    self.xmaxl = x - dd.dx
                if self.xmaxr < x + dd.dx:
                    self.xmaxr = x + dd.dx
                if self.ymaxb > y - dd.dy:
                    self.ymaxb = y - dd.dy
                if self.ymaxt < y + dd.dy:
                    self.ymaxt = y + dd.dy
            self.pads.append((x, y, dd))
        self.width = self.xmaxr - self.xmaxl
        self.height = self.ymaxt - self.ymaxb
        self.size = math.sqrt(self.width * self.width + self.height * self.height)
        if self.spads > 1 and self.spads + self.dpads > 0:
            self.dipsmd = 'SMD'
        elif self.spads + self.dpads > 1:
            self.dipsmd = 'DIP'
        else:
            self.dipsmd = 'XX'
        self.center_x = (self.xmaxl + self.xmaxr) / 2
        self.center_y = (self.ymaxt + self.ymaxb) / 2

    def group(self, settings):
        if (self.size < settings.Asize) and (self.spads + self.dpads < settings.Apads):
            return "Atype"
        elif (self.size < settings.Bsize) and (self.spads + self.dpads < settings.Bpads):
            return "Btype"
        elif (self.size < settings.Csize) and (self.spads + self.dpads < settings.Cpads):
            return "Ctype"
        else:
            return "Dtype"