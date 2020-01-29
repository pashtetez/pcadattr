from math import *
import os
class Scene:
    def __init__(self,name="svg",height=400,width=400):
        self.name = name
        self.items = []
        self.height = height
        self.width = width
        return

    def add(self,item): self.items.append(item)

    def strarray(self):
        xMin=min([item.origin[0]+item.minP[0] for item in self.items])
        yMin=min([item.origin[1]+item.minP[1] for item in self.items])
        xMax=max([item.origin[0]+item.maxP[0] for item in self.items])
        yMax=max([item.origin[1]+item.maxP[1] for item in self.items])
        sizespace = 3
        var = ["<?xml version=\"1.0\"?>\n",
               "<svg height=\"{0}\" width=\"{1}\" viewBox=\"{2} {3} {4} {5}\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\">\n".format(
               self.height,self.width,xMin-sizespace,-yMax-sizespace,xMax-xMin+sizespace*2,yMax-yMin+sizespace*2),
               "    <defs>\n",
               "        <pattern id=\"back\" x=\"0\" y=\"0\" width=\"0.5\" height=\"0.5\" patternUnits=\"userSpaceOnUse\">\n",
               "            <rect fill=\"#000\" x=\"0\" y=\"0\" width=\"1\" height=\"1\"/>\n",
               "            <circle cx=\"0.5\" cy=\"0.5\" r=\"0.02\" style=\"stroke: none; fill: #00FFFF\" />\n",
               "            <circle cx=\"0.0\" cy=\"0.5\" r=\"0.02\" style=\"stroke: none; fill: #00FFFF\" />\n",
               "            <circle cx=\"0.5\" cy=\"0.0\" r=\"0.02\" style=\"stroke: none; fill: #00FFFF\" />\n",
               "            <circle cx=\"0.0\" cy=\"0.0\" r=\"0.02\" style=\"stroke: none; fill: #00FFFF\" />\n",
               "        </pattern>\n",
               "    </defs>\n",
               "    <rect fill=\"url(#back)\" x=\"-30\" y=\"-30\" width=\"60\" height=\"60\"/>\n",
               "    <g transform=\"scale(1,-1)\">\n"]
        layers = ['10', '6', '8', '4', '1', '2', '5', '9', '7', '11', '3', '12']
        for l in layers:
            var+=["        <g style=\"display:none;\">\n"]
            var+=["            <g id=\"%s\" >\n" % l]
            for item in self.items:
                if item.lay == l:
                    var += item.resalt()
            var+=["            </g>\n"]
            var+=["        </g>\n"]
        layersdef = {"1":"style=\"fill:#C0C0C0;stroke:#C0C0C0;\"",
                     "2": "style=\"fill:#C0C000;stroke:#C0C000;\"",
                     "3": "style=\"fill:#C000C0;stroke:#C000C0;\"",
                     "4": "style=\"fill:#00C0C0;stroke:#00C0C0;\"",
                     "5": "style=\"fill:#00C000;stroke:#00C000;\"",
                     "6": "style=\"fill:#FFFFFF;stroke:#FFFFFF;\"",
                     "7": "style=\"fill:#C00000;stroke:#C00000;\"",
                     "8": "style=\"fill:#0000C0;stroke:#0000C0;\"",
                     "9": "style=\"fill:#C0C0C0;stroke:#C0C0C0;\"",
                     "10": "style=\"fill:#C0C0C0;stroke:#C0C0C0;\"",
                     "11": "style=\"fill:#C0C0C0;stroke:#C0C0C0;\"",
                     "12": "style=\"fill:#C0C0C0;stroke:#C0C0C0;\"",
                     "13": "style=\"fill:#C0C0C0;stroke:#C0C0C0;\""}
        for l in layers:
            var += ["        <use xlink:href=\"#%s\" %s/>\n" % (l,layersdef[l])]
        var+=["    </g>\n"]
        var += ["</svg>\n"]
        #for item in self.items: print(item.resalt())
        return var

    def write_svg(self,filename=None):
        if filename:
            self.svgname = filename
        else:
            self.svgname = self.name + ".svg"
        file = open("comps/"+self.svgname,'w')
        file.writelines(self.strarray())
        file.close()
        return



class Base:
    def __init__(self):
        self.st = []
        self.en = []
        self.lay = ""
        self.origin=(0,0)
        self.minP = (0, 0)
        self.maxP = (0, 0)
        return

    def rotate(self, degree):
        self.st = ["<g transform=\"rotate(%f)\">\n"%(degree)] + self.st
        self.en = self.en+["</g>\n"]
        return self

    def move(self, point):
        self.origin = point
        self.st = ["<g transform=\"translate(%f, %f)\">\n"%(point[0],point[1])] + self.st
        self.en = self.en + ["</g>\n"]
        return self

    def resalt(self):
        return self.st+self.strarray()+self.en

    def layer(self, number):
        self.lay = number
        return self

    def strarray(self):
        return []


class Line(Base):
    def __init__(self,start,end,width=0.4):
        Base.__init__(self)
        self.start = start
        self.end = end
        self.width = width
        self.minP = (min(end[0],start[0]),min(end[1],start[1]))
        self.maxP = (max(end[0], start[0]), max(end[1], start[1]))
        return

    def strarray(self):
        return ["<line x1=\"%f\" y1=\"%f\" x2=\"%f\" y2=\"%f\" " %\
                (self.start[0],self.start[1],self.end[0],self.end[1]),
                "style=\"fill:none; stroke-linecap:round; stroke-width:{0}\"/>\n".format(self.width)]


class TriplePointArc(Base):
    def __init__(self,start,end,centr,width=0.4):
        Base.__init__(self)
        self.start = start
        self.end = end
        self.centr = centr
        self.width = width
        self.rad = sqrt((self.centr[0] - self.end[0]) * (self.centr[0] - self.end[0]) + (self.centr[1] - self.end[1]) * (self.centr[1] - self.end[1]))
        self.minP = (centr[0]-self.rad,centr[1]-self.rad)
        self.maxP = (centr[0]+self.rad,centr[1]+self.rad)
        return

    def strarray(self):
        xs = self.start[0]  - self.centr[0]
        ys = self.start[1]  - self.centr[1]
        xe = self.end[0] - self.centr[0]
        ye = self.end[1] - self.centr[1]
        if ((xs*ye-ys*xe)>0):
            largeArcFlag=0
        else:
            largeArcFlag=1
        rad = self.rad
        if self.start == self.end:
            return ["<circle cx=\"{0}\" cy=\"{1}\" r=\"{2}\" ".format(self.centr[0],self.centr[1],rad),
                "style=\"fill:none;  stroke-linecap:round; stroke-width:{0}\"/>\n".format(self.width)]
        return ["<path d=\"M%f %f A%f,%f 0  %d 1 %f,%f \" " %\
                (self.start[0],self.start[1],rad,rad, largeArcFlag,self.end[0],self.end[1]),
                "style=\"fill:none;  stroke-linecap:round; stroke-width:{0}\"/>\n".format(self.width)]



class Arc(Base):
    def __init__(self,centr,startAngle,sweepAngle, radius,width=0.4):
        Base.__init__(self)
        self.startAngle = startAngle
        self.sweepAngle = sweepAngle
        self.radius = radius
        self.centr = centr
        self.width = width

        self.start = self.polarToCartesian(self.centr, self.radius, self.startAngle);
        self.end = self.polarToCartesian(self.centr, self.radius, self.startAngle+self.sweepAngle)
        self.minP = (centr[0]-self.radius,centr[1]-self.radius)
        self.maxP = (centr[0]+self.radius,centr[1]+self.radius)
        return

    def polarToCartesian(self, center, radius, angleInDegrees):
        angleInRadians = (angleInDegrees - 90) * pi / 180.0;
        return (center[0] + (radius * sin(angleInRadians)),center[1] + (radius * cos(angleInRadians)))


    def strarray(self):
        xs = self.start[0]  - self.centr[0]
        ys = self.start[1]  - self.centr[1]
        xe = self.end[0] - self.centr[0]
        ye = self.end[1] - self.centr[1]
        if ((xs*ye-ys*xe)>0):
            largeArcFlag=0
        else:
            largeArcFlag=1
        rad = self.radius
        if self.sweepAngle == 360:
            return ["<circle cx=\"{0}\" cy=\"{1}\" r=\"{2}\" ".format(self.centr[0],self.centr[1],rad),
                "style=\"fill:none;  stroke-linecap:round; stroke-width:{0}\"/>\n".format(self.width)]
        return ["<path d=\"M%f %f A%f,%f 0  %d 1 %f,%f \" " %\
                (self.start[0],self.start[1],rad,rad, largeArcFlag,self.end[0],self.end[1]),
                "style=\"fill:none;  stroke-linecap:round; stroke-width:{0}\"/>\n".format(self.width)]


class Rect(Base):
    def __init__(self,width,height,D, shift):
        Base.__init__(self)
        self.height = height
        self.width = width
        self.D = D
        self.shift = shift
        self.minP = (0-self.width/2,0-self.height/2)
        self.maxP = (self.width/2,self.height/2)
        return

    def strarray(self):
        return ["<path d=\"M%f %f H %f V %f H %f L %f %f " % \
                (0-self.width/2, self.height/2,  self.width/2, 0-self.height/2,
                0 - self.width / 2, 0-self.width/2, self.height/2),
                "M %f,%fa%f,%f 0 1,0 %f,0a%f,%f 0 1,0 %f,0 \" " %
                (0-self.D/2+self.shift[0], 0+self.shift[1], self.D/2, self.D/2, self.D, self.D/2, self.D/2, 0-self.D),
                "style=\"stroke-width:0; fill-rule:evenodd;\"/>\n"]


class RndRect(Base):
    def __init__(self,width,height, D, shift,curvature=0.5):
        Base.__init__(self)
        self.height = height
        self.width = width
        self.curvature = curvature
        self.D = D
        self.shift = shift
        self.minP = (0-self.width/2,0-self.height/2)
        self.maxP = (self.width/2,self.height/2)
        return

    def strarray(self):
        return ["<path d=\"M%f %f H %f a%f,%f 0 0 0 %f, %f V %f a%f,%f 0 0 0 %f,%f H %f a%f,%f 0 0 0 %f,%f  L %f %f a%f,%f 0 0 0 %f,%f " % \
                (0-self.width/2+self.curvature, self.height/2,  self.width/2-self.curvature, self.curvature,
                self.curvature, self.curvature, -self.curvature, 0-self.height/2+self.curvature, self.curvature,self.curvature, -self.curvature, -self.curvature,
                0 - self.width/2+self.curvature, self.curvature,self.curvature, -self.curvature, self.curvature,
                0-self.width/2, self.height/2-self.curvature, self.curvature,self.curvature, self.curvature, self.curvature),
                " M %f,%fa%f,%f 0 1,0 %f,0a%f,%f 0 1,0 %f,0 \" " %
                (0-self.D/2+self.shift[0], 0+self.shift[1], self.D/2, self.D/2, self.D, self.D/2, self.D/2, 0-self.D),
                "style=\"stroke-width:0; fill-rule:evenodd;\"/>\n"]


class Oval(Base):
    def __init__(self,width,height,D,shift):
        Base.__init__(self)
        self.height = height
        self.width = width
        self.D = D
        self.shift = shift
        self.minP = (0-self.width/2,0-self.height/2)
        self.maxP = (self.width/2,self.height/2)
        return

    def strarray(self):
        if (self.height<self.width):
            self.curvature=self.height/2
        else:
            self.curvature=self.width/2
        return ["<path d=\"M%f %f H %f a%f,%f 0 0 0 %f, %f V %f a%f,%f 0 0 0 %f,%f H %f a%f,%f 0 0 0 %f,%f  L %f %f a%f,%f 0 0 0 %f,%f " % \
                    (0-self.width/2+self.curvature, self.height/2,  self.width/2-self.curvature, self.curvature,
                    self.curvature, self.curvature, -self.curvature, 0-self.height/2+self.curvature, self.curvature,self.curvature, -self.curvature, -self.curvature,
                    0 - self.width/2+self.curvature, self.curvature,self.curvature, -self.curvature, self.curvature,
                    0-self.width/2, self.height/2-self.curvature, self.curvature,self.curvature, self.curvature, self.curvature),
                    " M %f,%fa%f,%f 0 1,0 %f,0a%f,%f 0 1,0 %f,0 \" " %
                    (0-self.D/2+self.shift[0], 0+self.shift[1], self.D/2, self.D/2, self.D, self.D/2, self.D/2, 0-self.D),
                    "style=\"stroke-width:0; fill-rule:evenodd; \"/>\n"]


class Ellipse(Base):
    def __init__(self,width,height,D,shift):
        Base.__init__(self)
        self.height = height
        self.width = width
        self.D = D
        self.shift = shift
        self.minP = (0-self.width/2,0-self.height/2)
        self.maxP = (self.width/2,self.height/2)
        return


    def strarray(self):
        return["<path d=\"    M %f,%fa%f,%f 0 1,0 %f,0a%f,%f 0 1,0 %f,0 " % \
                (0-self.height/2, 0, self.height/2, self.width/2, self.height, self.height/2, self.width/2, 0-self.height),
                " M %f,%fa%f,%f 0 1,0 %f,0a%f,%f 0 1,0 %f,0 \" " %
                (0-self.D/2+self.shift[0],0+self.shift[1], self.D/2, self.D/2, self.D, self.D/2, self.D/2, 0-self.D),
                "style=\"stroke-width:0; fill-rule:evenodd; \"/>\n"]


class MtHole(Base):
    def __init__(self,width,height):
        Base.__init__(self)
        self.height = height
        self.width = width
        self.minP = (0-self.width/2,0-self.height/2)
        self.maxP = (self.width/2,self.height/2)
        return

    def strarray(self):
        return["<path d=\"M %f %f L %f %f " % \
            (0-self.height/2, 0, self.height/2,0),
            "M %f  %f L %f %f " % \
            (0, 0-self.width/2, 0, self.width/2),
            "M %f,%fa%f,%f 0 1,0 %f,0a%f,%f 0 1,0 %f,0 \" " % \
            (0-self.height/2, 0, self.height/2, self.height/2, self.height, self.height/2, self.height/2, 0-self.height),
            "style=\"fill:none; stroke-width:0.05; \"/>\n"]


class Target(Base):
    def __init__(self,width,height):
        Base.__init__(self)
        self.height = height
        self.width = width
        self.minP = (0-self.width/2,0-self.height/2)
        self.maxP = (self.width/2,self.height/2)
        return

    def strarray(self):
        return[   "<path d=\"M %f %f L %f %f " % \
            (0-self.height/2, 0, self.height/2,0),
            "M %f  %f L %f %f \n" % \
            (0, 0-self.width/2, 0, self.width/2),
            "M %f,%f a%f,%f 0 1,0 %f,0a%f,%f 0 1,0 %f,0 " % \
            (0-2*self.height/5, 0, 2*self.height/5, 2*self.height/5, 4*self.height/5, 2*self.height/5, 2*self.height/5, 0-4*self.height/5),
            "M %f,%f a%f,%f 0 1,0 %f,0a%f,%f 0 1,0 %f,0 " % \
            (0-self.height/5, 0, self.height/5, self.height/5, 2*self.height/5, self.height/5, self.height/5, 0-2*self.height/5),
            "M %f,%f a%f,%f 0 1,0 %f,0a%f,%f 0 1,0 %f,0 " % \
            (0-3*self.height/10, 0, 3*self.height/10, 3*self.height/10, 3*self.height/5, 3*self.height/10, 3*self.height/10, 0-3*self.height/5),
            "M %f,%f a%f,%f 0 1,0 %f,0a%f,%f 0 1,0 %f,0 \" " % \
            (0-self.height/10, 0, self.height/10, self.height/10, self.height/5, self.height/10, self.height/10, 0-self.height/5),
            "style=\"fill:none; stroke-width:0.05; \"/>\n"]


class Polygon(Base):
    def __init__(self,points,D,shift):
        Base.__init__(self)
        self.points = points
        self.D=D
        self.shift = shift
        self.minP = (min([x[0] for x in self.points]),min([x[1] for x in self.points]))
        self.maxP = (max([x[0] for x in self.points]),max([x[1] for x in self.points]))
        return

    def strarray(self):
        return[   "<path d=\"M %f %f "% (self.points[-1][0], self.points[-1][1])]+\
            ["L"+str(x[0]) + " " + str(x[1]) + " " for x in self.points]+\
            [" M %f,%fa%f,%f 0 1,0 %f,0a%f,%f 0 1,0 %f,0 \" " %
            (0-self.D/2+self.shift[0], 0+self.shift[1], self.D/2, self.D/2, self.D, self.D/2, self.D/2, 0-self.D)] +\
            ["style=\"stroke-width:0; \"/>\n"]


class Text(Base):
    def __init__(self,text,size=8):
        Base.__init__(self)
        self.text = text
        self.size = size
        return

    def strarray(self):
        return ["<text x=\"%f\" y=\"%f\" font-size=\"%f\">" %\
                (0,self.point[1],self.size),
                "%s" % self.text,
                "</text>\n"]