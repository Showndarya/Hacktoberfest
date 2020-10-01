from tkinter import *
import sqlite3
from sqlite3 import Error
from tkinter import messagebox


class Set(Tk):
    def __init__(self):
        super().__init__()
        self.title("Set Password")
        self.maxsize(500,300)
        self.minsize(500,300)
        self.canvas = Canvas(width=1366, height=768, bg='black')
        self.canvas.pack()
        self.photo = PhotoImage(file='set.png')
        self.canvas.create_image(-20, -20, image=self.photo, anchor=NW)
        self.iconbitmap(r'libico.ico')
        def verify():
            if len(d.get()) == 0:
                messagebox.showinfo("Error","Please Enter Your User Id")
            elif len(a.get()) < 4 and len(b.get()) < 4 and len(c.get()) < 4:
                messagebox.showinfo("Error","Please Enter a Valid Password")
            elif b.get() != c.get():
                messagebox.showinfo("Error","New and Retype password are not same")
            else:
                try:
                    self.conn = sqlite3.connect('library_administration.db')
                    self.myCursor = self.conn.cursor()
                    self.myCursor.execute("Select password from admin where id = ?",[d.get()])
                    temp = self.myCursor.fetchone()
                    if temp:
                        if str(temp[0]) == a.get():
                            self.myCursor.execute("UPDATE admin SET password = ? WHERE id = ?",[b.get(),d.get()])
                            self.conn.commit()
                            self.conn.close()
                            messagebox.showinfo("Successful","Password Updated successfully")
                        else:
                            messagebox.showinfo("Error","Old Password Does not Match")
                    else:
                        messagebox.showinfo("Error", "User Not Found")
                except Error:
                    messagebox.showerror("Error","Something Goes Wrong")
            a.set("")
            b.set("")
            c.set("")
            d.set("")
        ulab = Label(self, text="User Id", font=('arial', 15, 'bold')).place(x=40, y=50)
        d = StringVar()
        Uentry= Entry(self, textvariable=d, width=30).place(x=250, y=55)
        olab = Label(self,text="Old Password",font=('arial', 15, 'bold')).place(x=40,y=100)
        a=StringVar()
        entryforoldpasswd = Entry(self,show='*',textvariable=a,width = 30).place(x=250,y=105)
        label = Label(self,text="New Password",font=('arial', 15, 'bold')).place(x=40,y=150)
        b=StringVar()
        entryfornewpasswd = Entry(self,show='*',textvariable=b,width = 30).place(x=250,y=155)
        label1 = Label(self,text="Re-Type password",font=('arial', 15, 'bold')).place(x=40,y=200)
        c=StringVar()
        entryforretypepasswd = Entry(self,show='*',textvariable =c,width = 30).place(x=250,y=205)
        butt=Button(self,text="Change",width=15,command = verify).place(x=280,y=255)
Set().mainloop()