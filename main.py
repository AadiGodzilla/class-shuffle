from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
from startfile import startfile
from functools import partial
import os, sys

from conversion.conversion import conversion

window = Tk()
window.configure(bg="CYAN")

def popup():
    popup_window = Toplevel(window)
    frame = Frame(popup_window, padx=10, pady=10)

    text = "File: "
    promotion = StringVar()
    sections = IntVar()

    def open_file():
        global file_name
        try:
            file_name = askopenfilename(filetypes=[("Excel SpreadSheet",".xlsx")])
            res = text + file_name
            label_1.config(text=res)
        except TypeError:
            pass

    def convert():
        try:
            global file_name

            if not file_name:
                messagebox.showerror("Error", "File not selected")
                return

            if not promotion.get() or promotion.get() == "":
                messagebox.showerror("Error", "Promotion Class Field must not be empty")
                return
            if not sections.get() or sections.get() == 0:
                messagebox.showerror("Error", "Sections must not be empty or be 0")
                return

            conversion(promotion.get(), sections.get(), file_name)
            messagebox.showinfo("Success", "Suffling and Promotion Successful")
            popup_window.destroy()
        except NameError:
            messagebox.showerror("Error","File not selected")
            print("File not selected")

    label_1 = Label(frame, text=text, wraplength=300, anchor=W)
    label_1.pack(side=LEFT, anchor=NW)

    label_2 = Label(frame, text="No. of Sections:")
    label_2.pack(side=LEFT, anchor=SW, padx=5)
    entry_1 = Entry(frame, textvariable=sections, width=5)
    entry_1.pack(side=LEFT, anchor=SW, padx=5)
    label_3 = Label(frame, text="Class: ")
    label_3.pack(side=LEFT, anchor=SW)
    entry_2 = Entry(frame, textvariable=promotion, width=8)
    entry_2.pack(side=LEFT, anchor=SW)

    button_1 = Button(frame, text="SELECT FILE", command=open_file)
    button_1.pack(side=TOP, anchor=NE)
    button_2 = Button(frame, text="PROMOTE", command=convert)
    button_2.pack(side=BOTTOM, padx=10, anchor=SE)

    frame.pack()

menu = Menu(window)

file_menu = Menu(menu)
file_menu.add_command(label="SELECT FILE", command=popup)
file_menu.add_command(label="EXIT", command=lambda: sys.exit(0))

select_menu = Menu(menu)

class_names = ["VI", "VII", "VIII", "IX", "X"]
sections = ["A", "B", "C", "D", "E", "F"]
class_drops = []

def open_spreadsheet(class_name, class_section):
    startfile(os.path.abspath(os.path.join(os.path.dirname(__file__), "class", class_name, f"section_{class_section}.xlsx")))

for i in range(len(class_names)):
    c = Menu(select_menu)
    for section in sections:
        c.add_command(label=f"SECTION {section}", command=partial(open_spreadsheet, class_names[i], section))
    class_drops.append(c)

for i in range(len(class_drops)):
    select_menu.add_cascade(label=f"CLASS {class_names[i]}", menu=class_drops[i])

menu.add_cascade(label="FILE", menu=file_menu)
menu.add_cascade(label="SELECT", menu=select_menu)

mainframe = Frame(window, width=700, height=600, bg="CYAN")
mainframe.pack()

title = Label(mainframe, text="MODERN INDIAN SCHOOL", bg="CYAN", fg="BLUE", font=("Noto Sans", 36))
title.place(x=350, y=300, anchor=CENTER)

window.config(menu=menu)
window.mainloop()