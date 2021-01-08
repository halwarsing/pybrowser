class HALS:
    def __init__(self):
        self.ver = "0.0.1"

    def decode(self, text, objs):
        for i in range(int(len(text.split("<")) / 2)):
            name, args = text.split("<")[i].replace(" ",""), text.split("<")[i + 1].split(">")[0]
            for elem in args.split("\n"):
                if (elem.replace(" ","") != ""):
                    arg, val = args.split("=")
                    for key, value in objs.items():
                        if objs[key]["name"] == name:
                            objs[key]["args"][arg.replace(" ","").replace("\n","")] = val.replace("\n","")

        return objs
