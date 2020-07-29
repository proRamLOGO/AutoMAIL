import tkinter as tk
import os
import config
import pickle
from PIL import Image, ImageTk

def center_window(root,width=300, height=200):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2) - 30
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

def get_mouse_posn(event):
    global topy, topx

    topx, topy = event.x, event.y

def update_sel_rect(event):
    global rect_id
    global topy, topx, botx, boty

    botx, boty = event.x, event.y
    canvas.coords(rect_id, topx, topy, botx, boty)  # Update selection rect.
    
def resize_image(path) :
    mywidth = 500
    img = Image.open(path)
    ext = path.split('.')[-1]
    wpercent = (mywidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((mywidth,hsize), Image.ANTIALIAS)
    img.save('resized.'+ext)
    return 'resized.'+ext

def save_location(window) :
    DB = {}
    with open('config.dat','rb+') as config :
        DB = pickle.load(config)
    with open('config.dat','wb+') as config :
        DB['X1'] = topx
        DB['X2'] = topy
        DB['Y1'] = botx
        DB['Y2'] = boty
        pickle.dump(DB,config)
    window.destroy()

WIDTH, HEIGHT = 600, 600
topx, topy, botx, boty = 0, 0, 0, 0
rect_id = None
path = os.getcwd() + "/src/Certificate.jpg"
# path = '' 
# with open(os.getcwd()+'/src/config.dat','rb+') as config :
#     DB = pickle.load(config)
#     path = DB['DATA_PATH']

window = tk.Tk()
window.title("Select Area")
window.geometry('%sx%s' % (WIDTH, HEIGHT))
window.configure(background='#fff')
rsImgLoc = resize_image(path)

pad1 = tk.Label(window,height=4)
pad1.pack()

label = tk.Label(window, text="Select the portion where name has to be written.", font=("Helvetica", 18))
label.pack()

img = ImageTk.PhotoImage(Image.open(rsImgLoc))
canvas = tk.Canvas(window, width=img.width(), height=img.height(),
                   borderwidth=0, highlightthickness=0)
canvas.pack(expand=True)
canvas.img = img  # Keep reference in case this code is put into a function.
canvas.create_image(0, 0, image=img, anchor=tk.NW)

# Create selection rectangle (invisible since corner points are equal).
rect_id = canvas.create_rectangle(topx, topy, topx, topy, dash=(2,2), fill='', outline='#000' )

canvas.bind('<Button-1>', get_mouse_posn)
canvas.bind('<B1-Motion>', update_sel_rect)

button = tk.Button(window, text="OK", image=None, command=lambda : save_location(window), height=2, width=14)
button.pack()

pad1 = tk.Label(window,height=2)
pad1.pack()

center_window(window,600,600)

window.mainloop()
