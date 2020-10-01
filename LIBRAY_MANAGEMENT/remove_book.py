from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
import os
import sys

py = sys.executable

class rb(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'libico.ico')
        self.maxsize(480,360)
        self.title("Remove book")
        self.canvas = Canvas(width=500, height=500, bg='black')
        self.canvas.pack()
        self.photo = PhotoImage(file='removebooks.png')
        self.canvas.create_image(-20, -20, image=self.photo, anchor=NW)
        a = StringVar()

        def aaa():
            if len(a.get()) == 0:
                messagebox.showerror("Error","Please Enter The Book Id")
            else:
                c = messagebox.askyesno('Remove Book', 'Are You Sure You Want To Remove The Book')
                if c:
                    try:
                        self.conn = sqlite3.connect('library_administration.db')
                        self.mycursor = self.conn.cursor()
                        self.mycursor.execute("DELETE FROM books WHERE Book_Id = ?",[a.get()])
                        messagebox.showinfo('Remove', 'Succesfully Removed')
                        self.conn.commit()
                        self.conn.close()
                        d = messagebox.askyesno("Confirm","Do you want to remove another book")
                        if d:
                            self.destroy()
                            os.system('%s %s' % (py, 'remove_book.py'))
                        else:
                            self.destroy()
                    except Error:
                        messagebox.showerror("Error", "Something Goes Wrong")

        lb = Label(self, text="Enter Book Id",fg='white', bg='black', font=('Comic Scan Ms', 20, 'bold'))
        lb.place(x=90, y=70)
        e = Entry(self, textvariable=a, width=30).place(x=85, y=135)
        bt = Button(self, text="Remove", width=20, command=aaa).place(x=100, y=170)

rb().mainloop()
