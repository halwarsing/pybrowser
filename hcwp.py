
class HCWP:
    def __init__(self):
        self.ver = "0.0.1"

    def decode(self, text, url):
        objs = {}
        settings = {"title": url, "import": []}
        head = text.split("<head>")[1].split("</head>")[0]
        for line in head.split("\n"):
            args = line.split("=")
            if (len(args) > 1):
                if args[0] != "import":
                    settings[args[0]] = args[1]

                else:
                    settings[args[0]].append(args[1])
            
        body = text.split("<body>")[1].split("</body>")[0]
        i = -1
        for line in body.split("\n"):
            if "print(" in line:
                f = line.split("print(")[1].split(")")[0]
                if f != "":
                    typeFun = "lbl"
                    name = "none"
                    content = ""
                    url = ""
                    color = "#000"
                    for args in f.split(";"):
                        arg = args.split("=")
                        typ = arg[0]
                        eql = arg[1]
                        if (typ == "type"):
                            typeFun = eql

                        if (typ == "name"):
                            name = eql

                        if (typ == "content"):
                            content = eql

                        if (typ == "color"):
                            color = eql

                        if (typ == "url"):
                            url = eql

                    if name == "none":
                        name = typeFun

                    if (typeFun == "lbl"):
                        args = {"content": content, "color": color, "type": typeFun}
                        objs[i] = {"name": name, "args": args}
                    elif (typeFun == "img"):
                        args = {"url": url, "type": typeFun}
                        objs[i] = {"name": name, "args": args}
                    elif (typeFun == "url"):
                        args = {"url": url, "type": typeFun, "content": content, "color": color}
                        objs[i] = {"name": name, "args": args}

            i += 1
            
        return objs, settings
