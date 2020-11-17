from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
import os
import sys

py = sys.executable

class Rem(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'libico.ico')
        self.maxsize(450,250)
        self.minsize(450,250)
        self.title("Remove Student")
        self.canvas = Canvas(width=500, height=417, bg='black')
        self.canvas.pack()
        self.photo = PhotoImage(file='removestudent.png')
        self.canvas.create_image(-20, -20, image=self.photo, anchor=NW)
        a = StringVar()

        def iii():
            if len(a.get()) == 0:
                messagebox.showerror("Error", "Please Enter The Student Id")
            else:
                c = messagebox.askyesno('Remove Book', 'Are You Sure You Want To Remove The Student')
                if c:
                    try:
                        self.conn = sqlite3.connect('library_administration.db')
                        self.mycursor = self.conn.cursor()
                        self.mycursor.execute("DELETE FROM students WHERE Student_Id = ?", [a.get()])
                        messagebox.showinfo('Remove', 'Succesfully Removed')
                        self.conn.commit()
                        self.conn.close()
                        d = messagebox.askyesno("Confirm", "Do you want to remove another student")
                        if d:
                            self.destroy()
                            os.system('%s %s' % (py, 'Remove_student.py'))
                        else:
                            self.destroy()
                    except Error:
                        messagebox.showerror("Error", "Something Goes Wrong")

        self.lb = Label(self, text="Enter Student Id", font=('Comic Scan Ms', 15, 'bold'))
        self.lb.place(x=30, y=70)
        self.e1 = Entry(self, textvariable=a, width=30).place(x=230, y=77)
        self.butt1234 = Button(self, text="Remove", width=20, command=iii).place(x=230, y=120)
Rem().mainloop()
