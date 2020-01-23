import os


class SandBox:
    def __init__(self):
        self.funcs = {"preprocess": {}, "other": {}, "postprocess": {}}
        self.preprocess = {}
        self.other = {}
        self.postprocess = {}
        self.read_funcs("custom_functions/preprocess/", "preprocess")
        self.read_funcs("custom_functions/other/", "other")
        self.read_funcs("custom_functions/postprocess/", "postprocess")

    def read_funcs(self, path, f_dict):
        if not os.path.isdir(path):
            return
        for name in os.listdir(path=path):
            if name.endswith('.fun'):
                file = open(path + name, 'r', encoding="utf8")
                fun = file.read()
                f_name = str(name.split(".")[0])
                try:
                    exec(fun)
                    exec('self.' + f_dict + "[" + f_name + "]=" + f_name)
                except:
                    print("error of function " + path + name)
                description = ""
                with open(path + name, "r", encoding="utf8") as fun:
                    for line in fun:
                        if line.startswith("#"):
                            description += line
                        else:
                            break
                self.funcs[f_dict][f_name] = description

    def run(self, f_dict, name, pcadfile):
        exec('self.' + f_dict + "[" + name + "](pcadfile)")
