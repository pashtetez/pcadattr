#Добавляет атрибут DIPSMD
#Для всех компонентов, аттрибут которых «RefDes» начинается на C, добавляет атрибуты Tolerance, TKE, Voltage.
#Для всех компонентов, аттрибут которых «RefDes» начинается на R, добавляет аттрибут Tolerance.
#Для всех SMD компонентов, аттрибут которых «RefDes» начинается на R, добавляет атрибут Value2.
#Для всех SMD компонентов добавляет атрибут DB_NUMBER.
def attr_editing(self):

    def add_attr_if_not_exists(arr,key,val):
        if findAll(attr,'attr',key) == [] :
            desc.append(['attr',key,val,['pt','0.0','0.0'],['isVisible','False'],['textStyleRef','"(Default)"']])

    def process_component(desc, **n):
        add_attr_if_not_exists(desc,'"DIPSMD"','"'+n['dipsmd']+'"')
        if dipsmd == 'SMD':
            add_attr_if_not_exists(desc,'"DB_NUMBER"','"{DB_NUMBER}"')
        if re.match('^"R.*"',n['refdes']):
            add_attr_if_not_exists(desc,'"Tolerance"','"{Tolerance}"')
        if dipsmd == 'SMD' and re.match('^"R.*"',n['refdes']):
            add_attr_if_not_exists(desc,'"Value2"','"{Value2}"')
        if re.match('^"C[^E].*"',n['refdes']):
            add_attr_if_not_exists(desc,'"Tolerance"','"{Tolerance}"')
            add_attr_if_not_exists(desc,'"TKE"','"{TKE}"')
            add_attr_if_not_exists(desc,'"Voltage"','"{Voltage}"')

    pads = findPath(self.fdata,["library","padStyleDef"])
    patdef = findPath(self.fdata,["library","patternDefExtended"])
    pats = findPath(self.fdata,["pcbDesign","multiLayer","pattern"])
    
    for xx in pats:
        b = find(patdef,"patternDefExtended",find(xx,"patternRef")[1])
        spads = 0
        dpads = 0
        pad = findPath(b,["patternGraphicsDef","multiLayer","pad"])
        for p in pad:
            pt = find(p,"pt")
            c = find(p,"padStyleRef")[1]
            dd = find(pads,'padStyleDef',c)
            if mfloat(find(dd,'holeDiam')[1]):
                dpads+=1
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
        
        process_component(desc,dipsmd=dipsmd,refdes=refdes) 
        try:
            desc = findPath(self.fdata,['netlist','compInst'],find(xx,"refDesRef")[1])[0]
            process_component(desc,dipsmd=dipsmd,refdes=refdes) 
        except:
            pass
