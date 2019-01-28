#Создаёт файл со списком DIP компонентов и их координатами
#Укажите relative_coord_top для установки нуля слоя TOP относитльно нуля pcad
#Укажите relative_coord_bot для установки нуля слоя BOTTOM относитльно нуля pcad
#Укажите output_file_prefix -  префикс файла в текушей директории
#Укажите mirror_y_top для отражения координат относительно 0 по Y в конечном файле для слоя TOP (0,1)
#Укажите mirror_x_top для отражения координат относительно 0 по X в конечном файле для слоя TOP (0,1)
#Укажите mirror_y_bot для отражения координат относительно 0 по Y в конечном файле для слоя BOTTOM (0,1)
#Укажите mirror_x_bot для отражения координат относительно 0 по X в конечном файле для слоя BOTTOM (0,1)

def components_location_report(self):

    relative_coord_top = [ 100.0 , 200.0 ]
    relative_coord_bot = [ 100.0 , 200.0 ]
    output_file_prefix = "test"
    mirror_y_top = 1
    mirror_x_top = 0
    mirror_y_bot = 1
    mirror_x_bot = 0


    filehandle_top = open(output_file_prefix+"_top.txt", 'w')
    filehandle_bot = open(output_file_prefix+"_bottom.txt", 'w')
    mirror_y_top = -1*(mirror_y_top*2-1)
    mirror_x_top = -1*(mirror_x_top*2-1)
    mirror_y_bot = -1*(mirror_y_bot*2-1)
    mirror_x_bot = -1*(mirror_x_bot*2-1)
    import math
    pads = findPath(self.fdata,["library","padStyleDef"])
    patdef = findPath(self.fdata,["library","patternDefExtended"])
    pats = findPath(self.fdata,["pcbDesign","multiLayer","pattern"])

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

        if dipsmd == 'DIP':
            comps_to_write.append(one_comp_to_write)
    print(comps_to_write)
    for co in comps_to_write:
        filehandle = ""
        relative_coord = ""
        mirror_y = 1
        mirror_x = 1
        if co["side"] == "TOP":
            filehandle = filehandle_top
            relative_coord = relative_coord_top
            mirror_y = mirror_y_top
            mirror_x = mirror_x_top
        else:
            filehandle = filehandle_bot
            relative_coord = relative_coord_bot
            mirror_y = mirror_y_bot
            mirror_x = mirror_x_bot
        filehandle.write('#'+co["name"])
        filehandle.write('\r\n')
        for pa in co["pads"]:
            filehandle.write('X:'+ ("%07.3f" % (mirror_x*(-pa["x"] + co["x"] -relative_coord[0]))))
            filehandle.write(';Y:'+ ("%07.3f" % (mirror_y*(pa["y"] + co["y"]-relative_coord[1]))))
            filehandle.write(';D:'+str(pa["h"]))
            filehandle.write('\r\n')
    filehandle_top.close()
    filehandle_bot.close()

