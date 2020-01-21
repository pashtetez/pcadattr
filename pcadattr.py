#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from json import loads, dumps
from datetime import datetime
import re, os, sys
from io import StringIO
import contextlib

from ui_main import Ui_MainWindow

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *
#from PyQt5.QtSvg import *
from PyQt5 import uic

#pyinstaller pcadattr.py --add-data "main.ui;." -y --onefile --windowed

try:
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.dirname(os.path.realpath(__file__))

def Sandbox(code,obj):
    old_stdout = sys.stdout
    old_stderr = sys.stderr
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()

    ns_globals = {}
    ns_locals = {}
    out, err, exc = None, None, None

    try:
        #print(code)
        exec(code, ns_globals, ns_locals)
    except:
        import traceback
        exc = traceback.format_exc()

    out = redirected_output.getvalue()
    err = redirected_error.getvalue()

    # reset outputs to the original values
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    print(out)

    return out, err, exc

def findAll(a,key,val = None):
    if val:
        return [x for x in a if x[0] == key and x[1] == val ]
    else:
        return [x for x in a if x[0] == key]


def find(a,key,val = None):
    return findAll(a,key,val)[0]


def findPath(a,path,lastval = None):
    b = a
    for x in path[:-1]:
        b = find(b,x)
    return findAll(b,path[-1],lastval)

def mfloat(s):
    if 'mm' in s:
        return float(s.replace('mm',''))/0.0254
    else:
        return float(s)

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        ui_main_window, qt_base_class = uic.loadUiType(os.path.join(base_path, "main.ui"))
        self.ui = ui_main_window()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.fdata = []  # read array
        self.ui.listWidget.itemClicked.connect(self.showComent)
        self.execfuncs()

    def pdata(self,data,s,tabdepth,d=0):
        if type(data)==list:
            if d<tabdepth:
                if self.prev_str:
                    s.write('\n')
                s.write(' '*2*(d-1))
            if d:
                s.write('(')
            for x in data:
                self.pdata(x,s,tabdepth,d+1)
            if d:
                if d<(tabdepth-1) and (not self.prev_str ):
                    s.write(' '*2*(d-1))
                s.write(')')
            if d<tabdepth:
                s.write('\n')
            self.prev_str = False
        else:
            s.write(data)
            self.prev_str = True
            s.write(' ')

    @pyqtSlot()
    def on_pushButton_in_clicked(self):
        self.ui.lineEdit_in.setText(QFileDialog.getOpenFileName(self,"Open pcad file", QFileInfo(self.ui.lineEdit_in.text()).filePath(), "PCAD Files (*.pcb *.PCB)")[0])
        if self.ui.lineEdit_in.text() != "" :
            self.ui.lineEdit_out.setText(self.ui.lineEdit_in.text())
            finf = QFileInfo(self.ui.lineEdit_out.text())
            self.ui.lineEdit_out.setText(finf.path()+"/"+''.join(finf.fileName().split(".")[:-1])+"_SB.pcb")

    @pyqtSlot()
    def on_pushButton_out_clicked(self):
        fileDialog = QFileDialog()
        fileDialog.setDefaultSuffix("pcb")
        self.ui.lineEdit_out.setText(fileDialog.getSaveFileName(self, "Save pcad file", QFileInfo(self.ui.lineEdit_out.text()).filePath(), "PCAD Files (*.pcb)")[0]);

    @pyqtSlot()
    def on_pushButton_clicked(self):
        if not self.ui.lineEdit_out.text() or not self.ui.lineEdit_in.text():
            print("empty")
            return
        new_file = QFileInfo(self.ui.lineEdit_out.text())
        if new_file.exists():
            if(QMessageBox.information(self, "Converter","Output file already exists. Are you sure you want to continue?", QMessageBox.Ok|QMessageBox.Cancel)==QMessageBox.Cancel):
                return
        if not self.readfile():
            if (QMessageBox.warning(self, "Converter",
                                        "Given file is not in ASCII format. Please select another file",
                                        QMessageBox.Ok)):
                return













        replace_map = {}
        replace_symbols = [[" ", "_"], [",", "."], ["/", "_"], ["%", "_"], ["<", "."], [">", "_"]]

        def repl(s):
            if s not in replace_map:
                a = s
                for x in replace_symbols:
                    a = a.replace(x[0], x[1])
                replace_map[s] = a
            return replace_map[s]

        patdef = findPath(self.fdata, ["library", "patternDefExtended"])
        for pd in patdef:
            pd[1] = repl(pd[1])
            orig_name = find(pd, 'originalName')
            orig_name[1] = repl(orig_name[1])
        compdef = findPath(self.fdata, ["library", "compDef"])
        for cd in compdef:
            cd[1] = repl(cd[1])
            orig_name = find(cd, 'originalName')
            orig_name[1] = repl(orig_name[1])
            attached_pat = find(find(cd, 'attachedPattern'), 'patternName')
            attached_pat[1] = repl(attached_pat[1])
        compinst = findPath(self.fdata, ['netlist', 'compInst'])
        for ci in compinst:
            orig_name = find(ci, 'compRef')
            orig_name[1] = repl(orig_name[1])
            orig_name = find(ci, 'originalName')
            orig_name[1] = repl(orig_name[1])
            if len(findAll(ci, 'compValue')):
                orig_name = find(ci, 'compValue')
                orig_name[1] = repl(orig_name[1])
        pats = findPath(self.fdata, ["pcbDesign", "multiLayer", "pattern"])
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










        # self.checkFunction()
        self.common_parse()




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

        for xx in self.comps_to_write:
            desc = find(xx[-1], "patternGraphicsRef")
            process_component(desc, self.patmap[xx[5]][6], xx[1])
            try:
                desc = findPath(self.fdata, ['netlist', 'compInst'], xx[1])[0]
                process_component(desc, self.patmap[xx[5]][6], xx[1])
            except:
                pass




        relative_coord_top = [100.0, 200.0]
        relative_coord_bot = [100.0, 200.0]
        output_file_prefix = "test"
        mirror_y_top = 1
        mirror_x_top = 0
        mirror_y_bot = 1
        mirror_x_bot = 0

        filehandle_top = open(output_file_prefix + "_top.txt", 'w')
        filehandle_bot = open(output_file_prefix + "_bottom.txt", 'w')
        mirror_y_top = -1 * (mirror_y_top * 2 - 1)
        mirror_x_top = -1 * (mirror_x_top * 2 - 1)
        mirror_y_bot = -1 * (mirror_y_bot * 2 - 1)
        mirror_x_bot = -1 * (mirror_x_bot * 2 - 1)

        for co in self.comps_to_write:
            filehandle = ""
            relative_coord = ""
            mirror_y = 1
            mirror_x = 1
            if co[4] == "TOP":
                filehandle = filehandle_top
                relative_coord = relative_coord_top
                mirror_y = mirror_y_top
                mirror_x = mirror_x_top
            else:
                filehandle = filehandle_bot
                relative_coord = relative_coord_bot
                mirror_y = mirror_y_bot
                mirror_x = mirror_x_bot
            filehandle.write('#' + co[1])
            filehandle.write('\r\n')
            for pa in co[0]:
                filehandle.write('X:' + ("%07.3f" % (mirror_x * (-pa["x"] + co[2] - relative_coord[0]))))
                filehandle.write(';Y:' + ("%07.3f" % (mirror_y * (pa["y"] + co[3] - relative_coord[1]))))
                filehandle.write(';D:' + str(pa["h"]))
                filehandle.write('\r\n')
        filehandle_top.close()
        filehandle_bot.close()





        for (k, v) in self.patmap.items():
            if v[1] > 1 and  v[1] +  v[2] > 0:
                pickpoint = ['pickpoint', ['pt', v[-3], v[-2]]]
                mltl = findPath(v[-1], ["patternGraphicsDef", "multiLayer"])[0]
                if findAll(mltl, 'pickpoint') == []:
                    mltl.append(pickpoint)




        pcbDesignHeader = findPath(self.fdata, ["pcbDesign", "pcbDesignHeader"])[0]
        if findAll(pcbDesignHeader, "refPointSize") == []:
            pcbDesignHeader.append(["refPointSize", "1.0"])
        else:
            find(pcbDesignHeader, "refPointSize")[1] = "1.0"
        if findAll(pcbDesignHeader, "solderSwell") == []:
            pcbDesignHeader.append(["solderSwell", "0.01"])
        else:
            find(pcbDesignHeader, "solderSwell")[1] = "0.01"




        self.writefile()
        if (QMessageBox.information(self, "Converter",
                                "File generated successfully",
                                QMessageBox.Ok)):
            return
        
    def writefile(self):
        self.prev_str = False #thing for writing
        b = StringIO()
        self.pdata(self.fdata,b,6)
        with open(self.ui.lineEdit_out.text(),'w', encoding="cp1251", errors="surrogateescape") as f:
            f.write(b.getvalue())
        #sys.stdout.write(b.getvalue())

    def readfile(self):
        self.fdata = []
        try:
            with open(str(self.ui.lineEdit_in.text()), 'r', encoding="cp1251") as fl:
                if fl.read().find("ACCEL_ASCII")!=0 :
                    return False
        except:
            return False
        with open(str(self.ui.lineEdit_in.text()),'r',encoding="cp1251") as fl:
            data = fl.read()#.decode("utf-8", "replace")
            data = [p for p in re.split("(\s|\".*?(?<!\\\\)\"|\)|\()", data) if p and p.strip()]
            self.fdata.append(list())
            for x in data:
                if x == '(':
                    self.fdata.append(list())
                elif x == ')':
                    d = self.fdata.pop()
                    self.fdata[-1].append(d)
                else:
                    self.fdata[-1].append(x)
        self.fdata = self.fdata[0]
        return True

    def execfuncs(self):
        global fdata 
        fdata = self.fdata
        for name in os.listdir(path="."): 
            if name.endswith('.fun'):
                file = open (name, 'r', encoding="utf8")
                fun=file.read()
                try:
                    exec(fun)
                    exec('self.'+name.split(".")[0]+"="+name.split(".")[0])
                    #try:
                    #    exec(name.split(".")[0]+"()")
                    #except:
                    #    print ("error of result")
                except:
                    print ("error of function")
                #add CheckBox
                item = QListWidgetItem(name.split(".")[0])
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                self.ui.listWidget.addItem(item)
        self.fdata = fdata

    def checkFunction (self):
        for x in range(self.ui.listWidget.count()):
            fun = self.ui.listWidget.item(x)
            if fun.checkState() == Qt.Checked:
                exec('self.'+fun.text()+"(self)")
                #Sandbox('obj.'+fun.text()+"(obj)",self)

    def addTable(self, a, tabname = "", columnName=[],rowName=[]):
        # Create table
        table    = QTableWidget()
        # Add table
        self.ui.tabWidget.addTab(table,tabname)
        # a = ([["1","2","3"],["4","5","6"]])
        table.setRowCount(len(a))
        table.setColumnCount(len(a[0]))
        # Hide row
        if columnName == []:
            table.horizontalHeader().hide()
        else:
            table.setHorizontalHeaderLabels(columnName)
        # Hide column
        if rowName == []: 
            table.verticalHeader().hide()
        else:
            table.setVerticalHeaderLabels(rowName)
        for row in range(len(a)):
            for element in range(len(a[row])):
                table.setItem(row,element, QTableWidgetItem(a[row][element]))

    @pyqtSlot(QListWidgetItem)
    def showComent (self, item):
        self.ui.plainTextEdit.clear()
        fun=open(item.text()+'.fun',"r", encoding="utf8")
        for line in fun:
            if line.startswith("#"):
                self.ui.plainTextEdit.setPlainText(self.ui.plainTextEdit.toPlainText()+line)
            else:
                return

    def common_parse(self):
        Asize = 6
        Bsize = 20
        Csize = 45
        Apads = 8
        Bpads = 44
        Cpads = 160

        headers = ["type", "original_name", "smd_pads", "dip_pads", "width", "height", "size", "dipsmd", "group"]

        import math
        pads = findPath(self.fdata, ["library", "padStyleDef"])
        patdef = findPath(self.fdata, ["library", "patternDefExtended"])
        pats = findPath(self.fdata, ["pcbDesign", "multiLayer", "pattern"])
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
            patmap[xx[1]] = [find(xx, "originalName")[1], spads, dpads, xmaxr - xmaxl, ymaxt - ymaxb,
                             math.sqrt((ymaxt - ymaxb) * (ymaxt - ymaxb) + (xmaxr - xmaxl) * (xmaxr - xmaxl))]
            grtype = ""
            dipsmd = ''
            if spads > 1 and spads + dpads > 0:
                dipsmd = 'SMD'
            elif spads + dpads > 1:
                dipsmd = 'DIP'
            else:
                dipsmd = 'XX'
            patmap[xx[1]].append(dipsmd)
            if (patmap[xx[1]][5] < Asize) and (
                    (patmap[xx[1]][1] + patmap[xx[1]][2]) < Apads):
                grtype = "Atype"
            elif (patmap[xx[1]][5] < Bsize) and (
                    (patmap[xx[1]][1] + patmap[xx[1]][2]) < Bpads):
                grtype = "Btype"
            elif (patmap[xx[1]][5] < Csize) and (
                    (patmap[xx[1]][1] + patmap[xx[1]][2]) < Cpads):
                grtype = "Ctype"
            else:
                grtype = "Dtype"
            patmap[xx[1]].append(grtype)
            patmap[xx[1]].append(str((xmaxl + xmaxr) / 2))
            patmap[xx[1]].append(str((ymaxt + ymaxb) / 2))
            patmap[xx[1]].append(xx)

        self.ui.compDefTable.setColumnCount(len(headers))
        for (k, v) in patmap.items():
            self.ui.compDefTable.insertRow(0)
            self.ui.compDefTable.setItem(0, 0, QTableWidgetItem(k))
            for i in range(0, len(headers)-1):
                self.ui.compDefTable.setItem(0, i+1, QTableWidgetItem(str(v[i])))

        comps_to_write = []
        for xx in pats:
            b = find(patdef, "patternDefExtended", find(xx, "patternRef")[1])
            point = [mfloat(find(xx, "pt")[1]), mfloat(find(xx, "pt")[2])]
            rotaion = 0
            try:
                rotaion = math.radians(float(find(xx, "rotation")[1]))
            except:
                pass
            refDesRef = find(xx, "refDesRef")[1]
            side = "TOP"
            try:
                if find(xx, "isFlipped"):
                    side = "BOTTOM"
            except:
                pass

            one_comp_to_write = [[], refDesRef, point[0], point[1], side, find(xx, "patternRef")[1]]
            pad = findPath(b, ["patternGraphicsDef", "multiLayer", "pad"])
            for p in pad:
                pt = find(p, "pt")
                c = find(p, "padStyleRef")[1]
                dd = find(pads, 'padStyleDef', c)
                hole_diam = mfloat(find(dd, 'holeDiam')[1])
                if hole_diam:
                    x_relative = mfloat(pt[1]) * math.cos(rotaion) - mfloat(pt[2]) * math.sin(rotaion)
                    y_relative = mfloat(pt[2]) * math.cos(rotaion) + mfloat(pt[1]) * math.sin(rotaion)
                    one_comp_to_write[0].append({"x": x_relative, "y": y_relative, "h": hole_diam})
            one_comp_to_write.append(xx)
            comps_to_write.append(one_comp_to_write)

        self.patmap = patmap
        self.comps_to_write = comps_to_write
        # f1 = open("test_comps.csv", 'w', encoding="cp1251", errors="surrogateescape")
        # f1.write("name;pattern;original_name;dipsmd;x;y;side;pads_count;smd_pads;dip_pads;width;height;size;group\r\n")
        # for c in comps_to_write:
        #     grtype = ""
        #     if (patmap[c["patternRef"]][5] < Asize) and (
        #             (patmap[c["patternRef"]][1] + patmap[c["patternRef"]][2]) < Apads):
        #         grtype = "Atype"
        #     elif (patmap[c["patternRef"]][5] < Bsize) and (
        #             (patmap[c["patternRef"]][1] + patmap[c["patternRef"]][2]) < Bpads):
        #         grtype = "Btype"
        #     elif (patmap[c["patternRef"]][5] < Csize) and (
        #             (patmap[c["patternRef"]][1] + patmap[c["patternRef"]][2]) < Cpads):
        #         grtype = "Ctype"
        #     else:
        #         grtype = "Dtype"
        #     f1.write("%s" % grtype)
        #
        #     self.ui.compTable.insertRow(0)
        #     self.ui.compTable.setItem(0,0,QTableWidgetItem(c["name"]))
        #     f1.write("\r\n")
        #
        # f1.close()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
