import re
from io import StringIO
from processing.find_utils import *
from processing.paddef import PadDef
from processing.compdef import CompDef
from processing.comp import Comp
from svg import Scene

class PcadFile:
    def __init__(self, data=None):
        self.compmap = {}
        self.compdefmap = {}
        self.padmap = {}
        self.m_data = None
        self._write_prev_str = False
        if data:
            self.import_from_str(data)

    def import_from_str(self, rawdata):
        data = [p for p in re.split("(\s|\".*?(?<!\\\\)\"|\)|\()", rawdata) if p and p.strip()]
        self.m_data = [[]]
        for x in data:
            if x == '(':
                self.m_data.append(list())
            elif x == ')':
                d = self.m_data.pop()
                self.m_data[-1].append(d)
            else:
                self.m_data[-1].append(x)
        self.m_data = self.m_data[0]

    def recursive_write(self, data, s, tab_depth, d=0):
        if type(data) == list:
            if d < tab_depth:
                if self._write_prev_str:
                    s.write('\n')
                s.write(' '*2*(d-1))
            if d:
                s.write('(')
            for x in data:
                self.recursive_write(x, s, tab_depth, d + 1)
            if d:
                if d < (tab_depth - 1) and (not self._write_prev_str):
                    s.write(' '*2*(d-1))
                s.write(')')
            if d < tab_depth:
                s.write('\n')
            self._write_prev_str = False
        else:
            s.write(data)
            self._write_prev_str = True
            s.write(' ')

    def export_to_str(self):
        b = StringIO()
        self._write_prev_str = False
        self.recursive_write(self.m_data, b, 6)
        return b.getvalue()

    def preprocess(self):
        # Заменяет в названиях и Value компонентов символы ' /%<>' на '_' и запятые на точки

        replace_map = {}
        replace_symbols = [[" ", "_"], [",", "."], ["/", "_"], ["%", "_"], ["<", "."], [">", "_"]]

        def repl(s):
            if s not in replace_map:
                a = s
                for x in replace_symbols:
                    a = a.replace(x[0], x[1])
                replace_map[s] = a
            return replace_map[s]

        patdef = findPath(self.m_data, ["library", "patternDefExtended"])
        for pd in patdef:
            pd[1] = repl(pd[1])
            orig_name = find(pd, 'originalName')
            orig_name[1] = repl(orig_name[1])
        compdef = findPath(self.m_data, ["library", "compDef"])
        for cd in compdef:
            cd[1] = repl(cd[1])
            orig_name = find(cd, 'originalName')
            orig_name[1] = repl(orig_name[1])
            attached_pat = find(find(cd, 'attachedPattern'), 'patternName')
            attached_pat[1] = repl(attached_pat[1])
        compinst = findPath(self.m_data, ['netlist', 'compInst'])
        for ci in compinst:
            orig_name = find(ci, 'compRef')
            orig_name[1] = repl(orig_name[1])
            orig_name = find(ci, 'originalName')
            orig_name[1] = repl(orig_name[1])
            if len(findAll(ci, 'compValue')):
                orig_name = find(ci, 'compValue')
                orig_name[1] = repl(orig_name[1])
        pats = findPath(self.m_data, ["pcbDesign", "multiLayer", "pattern"])
        for p in pats:
            orig_name = find(p, 'patternRef')
            orig_name[1] = repl(orig_name[1])
            pgr = find(p, "patternGraphicsRef")
            if findAll(pgr, 'attr', '"Value"'):
                orig_name = find(pgr, 'attr', '"Value"')
                orig_name[2] = repl(orig_name[2])
            if findAll(pgr, 'attr', '"Type"'):
                orig_name = find(pgr, 'attr', '"Type"')
                orig_name[2] = repl(orig_name[2])

        # Заменяет refPointSize на 1.0 (размер PNP)
        # и soldeerSwell на 0.01
        pcbDesignHeader = findPath(self.m_data, ["pcbDesign", "pcbDesignHeader"])[0]
        if findAll(pcbDesignHeader, "refPointSize") == []:
            pcbDesignHeader.append(["refPointSize", "1.0"])
        else:
            find(pcbDesignHeader, "refPointSize")[1] = "1.0"
        if findAll(pcbDesignHeader, "solderSwell") == []:
            pcbDesignHeader.append(["solderSwell", "0.01"])
        else:
            find(pcbDesignHeader, "solderSwell")[1] = "0.01"


        # self.checkFunction()
        Asize = 6
        Bsize = 20
        Csize = 45
        Apads = 8
        Bpads = 44
        Cpads = 160
        headers = ["type", "original_name", "smd_pads", "dip_pads", "width", "height", "size", "dipsmd", "group"]

        for pad in findPath(self.m_data, ["library", "padStyleDef"]):
            pd = PadDef(pad)
            self.padmap[pd.name] = pd

        for compdef in findPath(self.m_data, ["library", "patternDefExtended"]):
            cpd = CompDef(compdef, self.padmap)
            self.compdefmap[cpd.name] = cpd

        for comp in findPath(self.m_data, ["pcbDesign", "multiLayer", "pattern"]):
            cp = Comp(comp, self.compdefmap)
            self.compmap[cp.name] = cp

        for (k, v) in self.compdefmap.items():
            scene = Scene(k.replace("\"", ""))
            for element in self.compdefmap[k].get_graphics():
                scene.add(element)
            scene.write_svg()

        # name; orig_name; spads;dpads;width;height;size;dipsmd;group;center_x;center_y;
        # self.ui.compDefTable.setColumnCount(len(headers))
        # for (k, v) in patmap.items():
        #     self.ui.compDefTable.insertRow(0)
        #     self.ui.compDefTable.setItem(0, 0, QTableWidgetItem(k))
        #     for i in range(0, len(headers) - 1):
        #         self.ui.compDefTable.setItem(0, i + 1, QTableWidgetItem(str(v[i])))

    def process(self):
        # Добавляет атрибут DIPSMD
        # Для всех компонентов, аттрибут которых «RefDes» начинается на C, добавляет атрибуты Tolerance, TKE, Voltage.
        # Для всех компонентов, аттрибут которых «RefDes» начинается на R, добавляет аттрибут Tolerance.
        # Для всех SMD компонентов, аттрибут которых «RefDes» начинается на R, добавляет атрибут Value2.
        # Для всех SMD компонентов добавляет атрибут DB_NUMBER.
        def add_attr_if_not_exists(arr, key, val):
            if findAll(arr, 'attr', key) == []:
                desc.append(
                    ['attr', key, val, ['pt', '0.0', '0.0'], ['isVisible', 'False'], ['textStyleRef', '"(Default)"']])

        def process_component(desc, dipsmd, refdes):
            add_attr_if_not_exists(desc, '"DIPSMD"', '"' + dipsmd + '"')
            if dipsmd == 'SMD':
                add_attr_if_not_exists(desc, '"DB_NUMBER"', '"{DB_NUMBER}"')
            if re.match('^"R.*"', refdes):
                add_attr_if_not_exists(desc, '"Tolerance"', '"{Tolerance}"')
            if dipsmd == 'SMD' and re.match('^"R.*"', refdes):
                add_attr_if_not_exists(desc, '"Value2"', '"{Value2}"')
            if re.match('^"C[^E].*"', refdes):
                add_attr_if_not_exists(desc, '"Tolerance"', '"{Tolerance}"')
                add_attr_if_not_exists(desc, '"TKE"', '"{TKE}"')
                add_attr_if_not_exists(desc, '"Voltage"', '"{Voltage}"')

        for (k, v) in self.compmap.items():
            desc = find(v.raw_data, "patternGraphicsRef")
            process_component(desc, v.compdef.dipsmd, v.name)
            try:
                desc = findPath(self.m_data, ['netlist', 'compInst'], v.name)[0]
                process_component(desc, v.compdef.dipsmd, v.name)
            except:
                pass

        # Добавляет PNP в SMD компоненты
        for (k, v) in self.compdefmap.items():
            if v.dipsmd == "SMD":
                mltl = findPath(v.raw_data, ["patternGraphicsDef", "multiLayer"])[0]
                if not findAll(mltl, 'pickpoint'):
                    mltl.append(['pickpoint', ['pt', str(v.center_x), str(v.center_y)]])

        # Укажите mirror_x_top для отражения координат относительно 0 по X в конечном файле для слоя TOP (0,1)
        # Укажите mirror_y_bot для отражения координат относительно 0 по Y в конечном файле для слоя BOTTOM (0,1)
        # Укажите mirror_x_bot для отражения координат относительно 0 по X в конечном файле для слоя BOTTOM (0,1)

        # relative_coord_top = [100.0, 200.0]
        # relative_coord_bot = [100.0, 200.0]
        # output_file_prefix = "test"
        # mirror_y_top = 1
        # mirror_x_top = 0
        # mirror_y_bot = 1
        # mirror_x_bot = 0
        #
        # filehandle_top = open(output_file_prefix + "_top.txt", 'w')
        # filehandle_bot = open(output_file_prefix + "_bottom.txt", 'w')
        # mirror_y_top = -1 * (mirror_y_top * 2 - 1)
        # mirror_x_top = -1 * (mirror_x_top * 2 - 1)
        # mirror_y_bot = -1 * (mirror_y_bot * 2 - 1)
        # mirror_x_bot = -1 * (mirror_x_bot * 2 - 1)
        #
        # for co in self.comps_to_write:
        #     filehandle = ""
        #     relative_coord = ""
        #     mirror_y = 1
        #     mirror_x = 1
        #     if co[4] == "TOP":
        #         filehandle = filehandle_top
        #         relative_coord = relative_coord_top
        #         mirror_y = mirror_y_top
        #         mirror_x = mirror_x_top
        #     else:
        #         filehandle = filehandle_bot
        #         relative_coord = relative_coord_bot
        #         mirror_y = mirror_y_bot
        #         mirror_x = mirror_x_bot
        #     filehandle.write('#' + co[1])
        #     filehandle.write('\r\n')
        #     for pa in co[0]:
        #         filehandle.write('X:' + ("%07.3f" % (mirror_x * (-pa["x"] + co[2] - relative_coord[0]))))
        #         filehandle.write(';Y:' + ("%07.3f" % (mirror_y * (pa["y"] + co[3] - relative_coord[1]))))
        #         filehandle.write(';D:' + str(pa["h"]))
        #         filehandle.write('\r\n')
        # filehandle_top.close()
        # filehandle_bot.close()


PcadFile.findAll = findAll
PcadFile.find = find
PcadFile.findPath = findPath
PcadFile.mfloat = mfloat
