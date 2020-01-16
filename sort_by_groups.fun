#Делит компоненты на группы


def sort_by_groups(self):
    Asize = 6
    Bsize = 20
    Csize = 45
    Apads= 8
    Bpads = 44
    Cpads = 160

    import math
    pads = findPath(self.fdata, ["library", "padStyleDef"])
    patdef = findPath(self.fdata, ["library", "patternDefExtended"])
    pats = findPath(self.fdata, ["pcbDesign", "multiLayer", "pattern"])
    f = open("test_defs.csv", 'w', encoding="cp1251", errors="surrogateescape")
    f.write("type;original_name;smd_pads;dip_pads;width;height;size\r\n")
    patmap = {}
    for xx in patdef:
        b = findPath(xx, ["patternGraphicsDef", "multiLayer", "pad"])
        spads = 0
        dpads = 0
        xmaxl = 0.0
        xmaxr = 0.0
        ymaxb = 0.0
        ymaxt = 0.0
        for p in b:
            pt = find(p, "pt")
            c = find(p, "padStyleRef")[1]
            dd = find(pads, 'padStyleDef', c)

            x = mfloat(pt[1])
            y = mfloat(pt[2])
            if mfloat(find(dd, 'holeDiam')[1]):
                dpads += 1
            else:
                spads += 1
            shape = find(dd, 'padShape', ['layerNumRef', '1'])
            dx = 0.0
            dy = 0.0
            if find(shape, "padShapeType")[1] != "Polygon":
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
            if (spads + dpads) == 1:
                xmaxl = x - dx
                xmaxr = x + dx
                ymaxb = y - dy
                ymaxt = y + dy
            else:
                if xmaxl > x - dx:
                    xmaxl = x - dx
                if xmaxr < x + dx:
                    xmaxr = x + dx
                if ymaxb > y - dy:
                    ymaxb = y - dy
                if ymaxt < y + dy:
                    ymaxt = y + dy
        patmap[xx[1]] = [ find(xx,"originalName")[1], spads, dpads, xmaxr - xmaxl, ymaxt - ymaxb, math.sqrt((ymaxt - ymaxb)*(ymaxt - ymaxb) + (xmaxr - xmaxl)*(xmaxr - xmaxl))]
        f.write("%s;%s;%d;%d;%f;%f;%f\r\n" % (xx[1], find(xx,"originalName")[1], spads, dpads, xmaxr - xmaxl, ymaxt - ymaxb, math.sqrt((ymaxt - ymaxb)*(ymaxt - ymaxb) + (xmaxr - xmaxl)*(xmaxr - xmaxl))))
    f.close()
    comps_to_write = []
    for xx in pats:
        b = find(patdef,"patternDefExtended",find(xx,"patternRef")[1])
        point = [mfloat(find(xx,"pt")[1]),mfloat(find(xx,"pt")[2])]
        rotaion = 0
        try:
            rotaion = math.radians(float(find(xx,"rotation")[1]))
        except:
            pass
        refDesRef = find(xx,"refDesRef")[1][1:-1]
        side = "TOP"
        try:
            if find(xx,"isFlipped"):
                side = "BOTTOM"
        except:
            pass
        one_comp_to_write = {"name":refDesRef,"x":point[0],"y":point[1],"side":side,"pads":[]}
        one_comp_to_write["patternRef"] = find(xx,"patternRef")[1]
        spads = 0
        dpads = 0
        pad = findPath(b,["patternGraphicsDef","multiLayer","pad"])
        for p in pad:
            pt = find(p,"pt")
            c = find(p,"padStyleRef")[1]
            dd = find(pads,'padStyleDef',c)
            hole_diam = mfloat(find(dd,'holeDiam')[1])
            if hole_diam:
                dpads+=1
                x_relative = mfloat(pt[1])*math.cos(rotaion)-mfloat(pt[2])*math.sin(rotaion)
                y_relative = mfloat(pt[2])*math.cos(rotaion)+mfloat(pt[1])*math.sin(rotaion)
                one_comp_to_write["pads"].append({"x":x_relative,"y":y_relative,"h":hole_diam})
            else:
                spads+=1
        desc = find(xx,"patternGraphicsRef")
        refdes = find(xx,'refDesRef')[1]
        dipsmd = ''
        if spads>1 and spads+dpads>0 :
            dipsmd = 'SMD'
        elif spads+dpads>1:
            dipsmd = 'DIP'
        else:
            dipsmd = 'XX'
        one_comp_to_write["dipsmd"] = dipsmd
        comps_to_write.append(one_comp_to_write)
    f1 = open("test_comps.csv", 'w', encoding="cp1251", errors="surrogateescape")
    f1.write("name;pattern;original_name;dipsmd;x;y;side;pads_count;smd_pads;dip_pads;width;height;size;group\r\n")
    for c in comps_to_write:
        f1.write("%s;" % c["name"])
        f1.write("%s;" % c["patternRef"][1:-1])
        f1.write("%s;" % patmap[c["patternRef"]][0])
        f1.write("%s;" % c["dipsmd"])
        f1.write("%f;" % c["x"])
        f1.write("%f;" % c["y"])
        f1.write("%s;" % c["side"])
        f1.write("%d;" % (patmap[c["patternRef"]][1] + patmap[c["patternRef"]][2]))
        f1.write("%d;" % patmap[c["patternRef"]][1])
        f1.write("%d;" % patmap[c["patternRef"]][2])
        f1.write("%f;" % patmap[c["patternRef"]][3])
        f1.write("%f;" % patmap[c["patternRef"]][4])
        f1.write("%f;" % patmap[c["patternRef"]][5])
        grtype = ""
        if (patmap[c["patternRef"]][5] < Asize) and ((patmap[c["patternRef"]][1] + patmap[c["patternRef"]][2]) < Apads):
            grtype = "Atype"
        elif (patmap[c["patternRef"]][5] < Bsize) and ((patmap[c["patternRef"]][1] + patmap[c["patternRef"]][2]) < Bpads):
            grtype = "Btype"
        elif (patmap[c["patternRef"]][5] < Csize) and ((patmap[c["patternRef"]][1] + patmap[c["patternRef"]][2]) < Cpads):
            grtype = "Ctype"
        else:
            grtype = "Dtype"
        f1.write("%s" % grtype)
        f1.write("\r\n")
    f1.close()