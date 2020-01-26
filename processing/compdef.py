from processing.find_utils import *
import math
from svg import *
import copy


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
        self.draw(self.raw_data, padmap)

    def group(self, settings):
        if (self.size < settings.Asize) and (self.spads + self.dpads < settings.Apads):
            return "Atype"
        elif (self.size < settings.Bsize) and (self.spads + self.dpads < settings.Bpads):
            return "Btype"
        elif (self.size < settings.Csize) and (self.spads + self.dpads < settings.Cpads):
            return "Ctype"
        else:
            return "Dtype"

    def draw(self, file_part,pad_map):
        self.raw = file_part
        b = findPath(file_part, ["patternGraphicsDef", "multiLayer", "pad"])
        lays = findPath(file_part, ["patternGraphicsDef", "layerContents"])
        self.graphics = []
        self.p_c = (0 ,0)
        self.is_symmetric=False
        for l in lays:
            mylay = find(l, "layerNumRef")[1]
            for li in findAll(l, "line"):
                self.graphics.append(Line((mfloat(findAll(li, "pt")[0][1]), mfloat(findAll(li, "pt")[0][2])),
                               (mfloat(findAll(li, "pt")[1][1]), mfloat(findAll(li, "pt")[1][2])),
                               mfloat(findAll(li, "width")[0][1])).layer(mylay))
            for li in findAll(l, "triplePointArc"):
                self.graphics.append(TriplePointArc((mfloat(findAll(li, "pt")[1][1]), mfloat(findAll(li, "pt")[1][2])),
                                         (mfloat(findAll(li, "pt")[2][1]), mfloat(findAll(li, "pt")[2][2])),
                                         (mfloat(findAll(li, "pt")[0][1]), mfloat(findAll(li, "pt")[0][2])),
                                         mfloat(findAll(li, "width")[0][1])).layer(mylay))
            for li in findAll(l, "arc"):
                self.graphics.append(Arc((mfloat(findAll(li, "pt")[0][1]), mfloat(findAll(li, "pt")[0][2])),
                                         mfloat(findAll(li, "startAngle")[0][1]),
                                         mfloat(findAll(li, "sweepAngle")[0][1]),
                                         mfloat(findAll(li, "radius")[0][1]),
                                         mfloat(findAll(li, "width")[0][1])).layer(mylay))
            for li in findAll(l, "pcbPoly"):
                pds = findAll(li, 'pt')
                self.graphics.append(Polygon([(mfloat(x[1]), mfloat(x[2])) for x in pds], 0,
                                  (0, 0)).layer(mylay))
        for p in b:
            pt = find(p, "pt")
            angle = 0
            if len(findAll(p, 'rotation')):
                angle = findAll(p, 'rotation')[0][1]
            c = find(p, "padStyleRef")[1]
            pad_map[c].get_graphics()
            for pad in pad_map[c].get_graphics():
                self.graphics.append(copy.deepcopy(pad).rotate(float(angle)).move((mfloat(pt[1]), mfloat(pt[2]))))

        #symmetry calc
        if (len(b)==2) and (find(b[0], "padStyleRef")[1] == find(b[1], "padStyleRef")[1]):
            pt1 = find(b[0], "pt")
            pt2 = find(b[1], "pt")
            p_c = (truncate((mfloat(pt1[1])+mfloat(pt2[1]))/2),truncate((mfloat(pt1[2])+mfloat(pt2[2]))/2))
            self.p_c = (round((mfloat(pt1[1])+mfloat(pt2[1]))/2,6),round((mfloat(pt1[2])+mfloat(pt2[2]))/2,6))
            self.is_symmetric = True
            for l in lays:
                for li in findAll(l, "line"):
                    real_pts = []
                    for li1 in findAll(l, "line"):
                        for pts in findAll(li1, "pt"):
                            real_pts.append((mfloat(pts[1]),mfloat(pts[2])))
                    prob_pts = []
                    prob_pts1 = []
                    for pt in real_pts:
                        prob_pts.append((truncate((pt[0]+mfloat(findAll(li, "pt")[0][1]))/2),truncate((pt[1]+mfloat(findAll(li, "pt")[0][2]))/2)))
                        prob_pts1.append((truncate((pt[0] + mfloat(findAll(li, "pt")[1][1])) / 2),
                                          truncate((pt[1] + mfloat(findAll(li, "pt")[1][2])) / 2)))
                    if p_c not in prob_pts :
                        self.is_symmetric = False
                    if p_c not in prob_pts1:
                        self.is_symmetric = False
                for li in findAll(l, "triplePointArc"):
                    real_pts = []
                    for li1 in findAll(l, "triplePointArc"):
                        for pts in findAll(li1, "pt"):
                            real_pts.append((mfloat(pts[1]), mfloat(pts[2])))
                    prob_pts = []
                    for pt in real_pts:
                        prob_pts.append((truncate((pt[0] + mfloat(findAll(li, "pt")[0][1])) / 2),
                                         truncate((pt[1] + mfloat(findAll(li, "pt")[0][2])) / 2)))
                    if p_c not in prob_pts :
                        self.is_symmetric = False
                for li in findAll(l, "arc"):
                    real_pts = []
                    for li1 in findAll(l, "triplePointArc"):
                        for pts in findAll(li1, "pt"):
                            real_pts.append((mfloat(pts[1]), mfloat(pts[2])))
                    prob_pts = []
                    for pt in real_pts:
                        prob_pts.append((truncate((pt[0] + mfloat(findAll(li, "pt")[0][1])) / 2),
                                         truncate((pt[1] + mfloat(findAll(li, "pt")[0][2])) / 2)))
                    if p_c not in prob_pts :
                        self.is_symmetric = False
                # for li in findAll(l, "pcbPoly"):
                #     real_pts = []
                #     for li1 in findAll(l, "pcbPoly"):
                #         for pts in findAll(li1, "pt"):
                #             real_pts.append((mfloat(pts[1]), mfloat(pts[2])))
                #     for pts in findAll(li, "pt"):
                #         if (-mfloat(pts[1]), -mfloat(pts[2])) not in real_pts:
                #             self.is_symmetric = False





    def get_graphics(self):
        return self.graphics