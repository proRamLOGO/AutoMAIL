import tkinter as tk
import tkinter.filedialog
import pandas as pd
import time, os
import pickle
# import imagecrop
from PIL import ImageTk ,Image
import pandas._libs.ops_dispatch
dir_path = os.getcwd()
tk.NoDefaultRoot()

def center_window(root,width=300, height=200):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2) - 30
    root.geometry('%dx%d+%d+%d' % (width, height, x, y))

print("hey")
root = tk.Tk()
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
root.title("AutoMail")
center_window(root,800, 600)

config = open(os.getcwd() + "/src/config.dat",'wb+')
pickle.dump({ 'SENDER_EMAIL' : None, 
              'SENDER_PASSWORD' : None,
              'DATA_PATH' : None,
              'CERTIFICATE_PATH' : None,
              'MAIL_SUBJECT' : None,
              'MAIL_CONTENT' : None,
              'X1': 0,
              'X2': 0,
              'Y1': 0,
              'Y2': 0 }, config)
config.close()

class Frame2(object) :

    def __init__(self, root) :
        self.root = root

    def load(self) :
        self.frame = tk.Frame(self.root,width=self.root.winfo_screenwidth()-400,height=self.root.winfo_screenheight(),bg="#fff")
        self.frame.pack(anchor=tk.N, fill=tk.X, expand=True, side=tk.TOP )
        # self.frame.grid(row=2, column=0)

        self.stepname = tk.Label(self.frame, text="2.Upload the Certificate.", font=("Helvetica", 36), fg="#4f4f4f" )
        self.stepname['bg'] = self.stepname.master['bg']
        self.stepname.pack(side=tk.TOP)

        self.pad1 = tk.Label(self.frame,height=2)
        self.pad1.pack()

        self.desc_1_1 = tk.Label(self.frame, text="Attach an image file",font=("Helvetica", 18), fg="#4f4f4f", height=2, bg=None )
        self.desc_1_1.pack(side=tk.TOP)

        # img=ImageTk.PhotoImage(Image.open(dir_path+"/src/assets/button_1_1.png"))
        self.button1_1 = tk.Button(self.frame, text="Upload Certificate", image=None, command = self.fetchfile, height=2, width=14)
        self.button1_1.pack()

        self.desc_1_2 = tk.Label(self.frame, text='No File Choosen', font=("Helvetica", 12), fg="#4f4f4f", height=2, bg=None )
        self.desc_1_2.pack(side=tk.TOP)

        self.imgcanvas = tk.Canvas(self.frame,width=200,height=200,bg='#000')
        self.imgcanvas.pack()
        
        self.pad2 = tk.Label(self.frame,height=2)
        self.pad2.pack()

        self.button1_2 = tk.Button(self.frame, text="Next", image=None, command = self.nextpage, height=2, width=12)
        self.button1_2["state"] = "disabled"
        self.button1_2.pack()

        self.frame.pack_propagate(False) 

    def fetchfile(self) :
        self.filepath = tk.filedialog.askopenfilename(parent=self.root,filetypes = [("Jpeg", "*.jpg"),("Jpeg", "*.jpeg"),("Png", "*.png"),("Png", "*.bmp")])
        self.filename = self.filepath.split("/")[-1]
        self.desc_1_2.configure(text=str("File Choosen: "+self.filename))
        if len(self.filename)!=0 :
            self.button1_2["state"] = "normal"
        else :
            self.button1_2["state"] = "disabled"

    def nextpage(self) :
        import imagecrop
        self.frame.destroy()

# 1. Upload a certificate
class Frame1(object) :

    def __init__(self,root) :
        self.root = root

    def load(self) :
        self.filepath = None
        self.frame = tk.Frame(self.root,width=self.root.winfo_screenwidth()-400,height=self.root.winfo_screenheight()-350,bg="#fff")
        self.frame.pack(anchor=tk.N, fill=tk.X, expand=True, side=tk.TOP )
        # self.frame.grid(row=2, column=0)

        self.stepname = tk.Label(self.frame, text="1. Get the mailing list.", font=("Helvetica", 36), fg="#4f4f4f" )
        self.stepname['bg'] = self.stepname.master['bg']
        self.stepname.pack(side=tk.TOP)

        self.pad1 = tk.Label(self.frame,height=2)
        self.pad1.pack()

        self.desc_1_1 = tk.Label(self.frame, text="Attach a .csv or a .xlsx file",font=("Helvetica", 18), fg="#4f4f4f", height=2, bg=None )
        self.desc_1_1.pack(side=tk.TOP)

        # img=ImageTk.PhotoImage(Image.open(dir_path+"/src/assets/button_1_1.png"))
        self.button1_1 = tk.Button(self.frame, text="Upload a file", image=None, command = self.fetchfile, height=2, width=12)
        self.button1_1.pack()

        self.desc_1_2 = tk.Label(self.frame, text='No File Choosen', font=("Helvetica", 12), fg="#4f4f4f", height=2, bg=None )
        self.desc_1_2.pack(side=tk.TOP)

        # Image to be added here
        self.imgcanvas = tk.Canvas(self.frame,width=200,height=200,bg='#000')
        self.imgcanvas.pack()

        self.pad2 = tk.Label(self.frame,height=2)
        self.pad2.pack()

        self.button1_2 = tk.Button(self.frame, text="Next", image=None, command = self.validate_csv, height=2, width=12)
        self.button1_2["state"] = "disabled"
        self.button1_2.pack()

        self.frame.pack_propagate(False) 

        return True

    def fetchfile(self) :
        self.filepath = tk.filedialog.askopenfilename(parent=self.root,filetypes = [("Comma Seperated Values", "*.csv"),("Excel File", "*.xls"),("Excel File", "*.xlsx")])
        self.filename = self.filepath.split("/")[-1]
        self.desc_1_2.configure(text=str("File Choosen: "+self.filename))
        if len(self.filename)!=0 :
            self.button1_2["state"] = "normal"
        else :
            self.button1_2["state"] = "disabled"
        

    def validate_csv(self) :
        # Now check wether name and email fields exist
        file = open(self.filepath,'r+')
        content = file.readline().split(',')
        emailFound,nameFound = 0,0
        for i in content :
            x = i.strip().lower()
            if x in ['email', 'e-mail', 'email address', 'e-mail address'] :
                emailFound += 1
            if x == 'name':
                nameFound += 1
        
        if  emailFound == 0 :
            self.raise_validate_error("EMAIL COLUMN NOT FOUND")
            return
        elif  emailFound > 1 :
            self.raise_validate_error("MULTIPLE EMAIL COLUMNS")
            return
        elif  nameFound == 0 :
            self.raise_validate_error("NAME COLUMN NOT FOUND")
            return
        elif  nameFound > 1 :
            self.raise_validate_error("MULTIPLE NAME COLUMN")
            return
        
        DB = {}
        with open('config.dat','rb+') as config :
            DB = pickle.load(config)
        DB['DATA_PATH'] = self.filepath
        with open('config.dat','wb+') as config :
            pickle.dump(DB,config)
        
        self.frame.destroy()
        f2 = Frame2(self.root)
        f2.load()
        # self.frame.geometry('0x0')
        # self.frame.destroy()
        f2.frame.tkraise()

        return

        
    def raise_validate_error(self,error) :
        self.checker = tk.Toplevel(self.frame) 
        self.checker.title("Validating File")
        # self.checker.geometry("+%d+%d" % (x + 100, y + 200))
        self.pad2 = tk.Label(self.frame,height=2)
        self.pad2.pack()

        self.checkerLabel = tk.Label(self.checker,text="Checking File", fg="#4f4f4f")
        self.checkerLabel.pack()
        self.checkerDesc = tk.Label(self.checker, fg="#4f4f4f")
        self.checkerDesc.pack()
        center_window(self.checker,400,250)
        self.checkerLabel.configure(text=error)
        self.checker.grab_set()
        self.checkerButton = tk.Button(self.checker, text="Retry", image=None, command = self.checker.destroy , height=2, width=12)
        self.checkerButton.pack()


# 1. FileList Upload
f1 = Frame1(root)
f1.load()
# f1.hide()
# f2 = Frame2(root)
# f2.load()
# f2.frame.grid(row=0,column=0,sticky="nsew")
root.mainloop()