from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
import os
py=sys.executable


#creating window
class Lib(Tk):
    def __init__(self):
        super().__init__()
        self.a = StringVar()
        self.b = StringVar()
        self.maxsize(1200, 700)
        self.minsize(1200, 700)
        self.state("zoomed")
        self.iconbitmap(r'libico.ico')
        self.canvas = Canvas(width=1366, height=768, bg='blue')
        self.canvas.pack()
        self.photo = PhotoImage(file='login.png')
        self.canvas.create_image(-20, -20, image=self.photo, anchor=NW)
        self.title("SHEPHERD LIBRARY MANAGEMENT SYSTEM (SLIMS)")


#verifying input
        def chex():
            if len(self.user_text.get()) < 0:
                messagebox.showinfo(" INVALID USERNAME OR PASSWORD" )
            elif len(self.pass_text.get()) < 0:
                messagebox.showinfo(" INVALID USERNAME OR PASSWORD")
            else:
                try:
                    self.conn = sqlite3.connect('library_administration.db')
                    self.myCursor = self.conn.cursor()
                    self.myCursor.execute("Select * from admin where id=? AND password =?",[self.user_text.get(),self.pass_text.get()])
                    self.pc = self.myCursor.fetchall()
                    self.myCursor.close()
                    self.conn.close()
                    if self.pc:
                        self.destroy()
                        os.system('%s %s' % (py, 'options.py'))
                    else:
                        messagebox.showinfo('Error', 'Username and password not found')
                        self.user_text.delete(0, END)
                        self.pass_text.delete(0, END)
                except Error:
                    messagebox.showinfo('Error',"Something Goes Wrong,Try restarting")
        def fp():
            os.system('%s %s' % (py, 'f_passwd.py'))

        def check():
            try:
                conn = sqlite3.connect('library_administration.db')
                mycursor = conn.cursor()
                mycursor.execute("Select * from admin")
                z = mycursor.fetchone()
                mycursor.close()
                conn.close()
                if not z:
                    messagebox.showinfo("Error", "Please Register A user")
                    x = messagebox.askyesno("Confirm","Do you want to register a user")
                    if x:
                        self.destroy()
                        os.system('%s %s' % (py, 'Reg.py'))
                else:
                    self.label = Label(self, text="LOGIN CREDENTIAL'S",bg ='BLACK',fg = 'white', font=("Algerian", 24,'bold'))
                    self.label.place(x=415, y=475)
                    self.label1 = Label(self, text="User-Id",bg='black',fg = 'white', font=("Times New roman", 18, 'bold'))
                    self.label1.place(x=370, y=530)
                    self.user_text = Entry(self, textvariable=self.a, width=45)
                    self.user_text.place(x=480, y=540)
                    self.label2 = Label(self, text="Password",bg='black',fg = 'white', font=("Times new roman", 18, 'bold'))
                    self.label2.place(x=370, y=565)
                    self.pass_text = Entry(self, show='*', textvariable=self.b, width=45)
                    self.pass_text.place(x=480, y=575)
                    self.butt = Button(self, text="Login",bg ='light green', font=10, width=8, command=chex).place(x=580, y=610)
                    self.butt2 = Button(self, text="Forgot Password",bg ='yellow', font=8, width=15, command=fp).place(x=547, y=650)
            except Error:
                messagebox.showinfo("Error", "Something Goes Wrong")

        check()

Lib().mainloop()