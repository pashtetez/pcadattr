#Заменяет в названиях и Value компонентов символы ' /%<>' на '_' и запятые на точки

def symbols_replacement(self):
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
