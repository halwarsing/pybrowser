import socket
from hcwp import HCWP
from tkinter import *
from PIL import Image, ImageTk
import ssl
from hals import HALS
root = Tk()
root.title("HaloseR")
root.geometry("1920x1080")
elementsFrame = Frame(root,height=50,width=1920)
elementsFrame.place(x=0,y=0)
windowBrow = Frame(root,width=1900,height=900,bg="white")
windowBrow.place(x=10,y=50)
hcwp = HCWP()
hals = HALS()
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ssl_s = ssl.create_default_context()
ssl_sock = ""
elements = []
request = """"""
def refresh():
    for child in windowBrow.winfo_children():
        child.destroy() 
    ssl_sock.sendall(request.encode())
    data = ssl_sock.recv(100000)
    print(data)
    
        
    def add_lbl(text, col, row, color):
        lbl = Label(windowBrow, text=text, fg=color, bg="white")
        lbl.place(x=0, y=row*20)

    def add_img(url, col, row):
        req = """GET /{0} HTTP/1.1
Host: {1}
Accept: text/png

""".format(url,urlEn.get().split("://")[1].split("/")[0])
        ssl_sock.sendall(req.encode())
        data = ssl_sock.recv(100000000)
        open("test.png","wb").write(data.split(b"bytes\r\n\r\n")[1])
        
        pil_image = Image.open("test.png")
        image = ImageTk.PhotoImage(pil_image)
        img = Label(windowBrow, text="")
        print(pil_image.size)
        img.place(x=0, y=row*20+pil_image.size[1]/2)
        img.config(image=image)
        img.image = image

    def add_url(text, url, col, row, color):
        link = Label(windowBrow, text=text, cursor="hand2", fg=color)
        link.place(x=50, y=0)
        link.bind("<Button-1>", lambda e: gourl(url))

    root.title(urlEn.get())
    
    try:
        data = data.decode().split("<hcwp>")[1].split("</hcwp>")[0]
        dec, settings = hcwp.decode(data, urlEn.get())
        
        
        for key, value in settings.items():
            if (key == "title"):
                if value != "":
                    root.title(value)
                else:
                    root.title(urlEn.get())

            if (key == "import"):
                for v in value:
                    re = """GET /{0} HTTP/1.1
Host: {1}

""".format(v,urlEn.get().split("://")[1].split("/")[0])
                    ssl_sock.sendall(re.encode())
                    text = ssl_sock.recv(1000000)
                    dec = hals.decode(text.decode().split("bytes\r\n\r\n")[1],dec)
                    print(dec)
                    
        for i in range(len(dec)):
            if (dec[i]["args"]["type"] == "lbl"):
                add_lbl(dec[i]["args"]["content"],0,i+1,dec[i]["args"]["color"])

            elif (dec[i]["args"]["type"] == "img"):
                add_img(dec[i]["args"]["url"],0,i+1)

            elif (dec[i]["args"]["type"] == "url"):
                add_url(dec[i]["args"]["content"], dec[i]["args"]["url"], 0, i+1, dec[i]["args"]["color"])

    except:
        error = Label(windowBrow,fg="red",text="Error 1 - not supported web-page")
        error.place(x=0,y=0)

urlEn = Entry(elementsFrame, width=100)
urlEn.pack(side=LEFT)
urlEn.insert(0,"https://halhub.peopletok.ru/f.hcwp")

def gourl(urli):
    global sock
    global ssl_sock
    sock.close()
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    global request
    url = urli
    if "://" in url:
        url = urlEn.get() + urli
    else:
        url = "https://"+urli
        print(url)
    
    ssl_sock = ssl_s.wrap_socket(sock, server_hostname=url.split("://")[1].split("/")[0])
    if url.split("://")[0] == "https":
        ssl_sock.connect((url.split("://")[1].split("/")[0],443))
    else:
        ssl_sock.connect((url.split("://")[1].split("/")[0],80))

    file = url.split("://")[1].split("/")
    if (len(file) < 1):
        file = "/"

    else:
        file = file[1]
        
    request = """GET /{0} HTTP/1.1
Host: {1}

""".format(file,url.split("://")[1].split("/")[0])
    urlEn.delete(0,"end")
    urlEn.insert(0, url)
    refresh()

def go():
    global sock
    global ssl_sock
    sock.close()
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    global request
    url = urlEn.get()
    ssl_sock = ssl_s.wrap_socket(sock, server_hostname=url.split("://")[1].split("/")[0])
    if url.split("://")[0] == "https":
        ssl_sock.connect((url.split("://")[1].split("/")[0],443))
    else:
        ssl_sock.connect((url.split("://")[1].split("/")[0],80))
    
    request = """GET /{0} HTTP/1.1
Host: {1}

""".format(url.split("://")[1].split("/")[1],url.split("://")[1].split("/")[0])
    
    refresh()
    
btnGo = Button(elementsFrame, text="Go",command=go)
btnGo.pack(side=LEFT)
btnRef = Button(elementsFrame, text="Refresh",command=refresh)
btnRef.pack(side=LEFT)
root.mainloop()
    
    
