# import tkinter as tk


# app = tk.Tk()

# class Excel(tk.Frame):
#     def __init__(self, master, rows, columns, width):
#         super().__init__(master)

#         for i in range(columns):
#             self.make_entry(0, i+1, width, f'C{i}', False) 

#         for row in range(rows):
#             self.make_entry(row+1, 0, 5, f'R{row}', False)
                
#             for column in range(columns):
#                 self.make_entry(row+1, column+1, width, '', True)

#     def make_entry(self, row, column, width, text, state):
#         e = tk.Entry(self, width=width)
#         if text: e.insert(0, text)
#         e['state'] = tk.NORMAL if state else tk.DISABLED
#         e.coords = (row-1, column-1)
#         e.grid(row=row, column=column)

# ex = Excel(app, rows=5, columns=2, width=8)
# ex.pack(padx=20, pady=20)

# def show_cells():
#     print('\n--== dumping cells ==--')
#     for e in ex.children:
#         v = ex.children[e]
#         print(f'{v.get()}', end=', ')
#     print()

# def newcell() :
#     pass

# bt = tk.Button(app, text='Dump', command=show_cells)
# bt.pack(pady=20)

# add = tk.Button(app, text='+', command=newcell)
# add.pack()
# app.mainloop()

# // GIFmage on canvas
from tkinter import *
# create the canvas, size in pixels
canvas = Canvas(width = 300, height = 200, bg = 'yellow')
# pack the canvas into a frame/form
canvas.pack(expand = YES, fill = BOTH)
# load the .gif image file
# put in your own gif file here, may need to add full path
# like 'C:/WINDOWS/Help/Tours/WindowsMediaPlayer/Img/mplogo.gif'
gif1 = PhotoImage(file = 'sheet_1.gif')
# put gif image on canvas
# pic's upper left corner (NW) on the canvas is at x=50 y=10
canvas.create_image(50, 10, image = gif1, anchor = NW)
# run it ...
mainloop()