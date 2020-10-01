from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
import os,sys
from datetime import datetime,date
py = sys.executable


class ret(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'libico.ico')
        self.title("Return")
        self.maxsize(420,280)
        self.canvas = Canvas(width=500, height=417, bg='black')
        self.canvas.pack()
        self.photo = PhotoImage(file='ret.png')
        self.canvas.create_image(-20, -20, image=self.photo, anchor=NW)
        self.cal = 0
        a = StringVar()

        def days_between(d1, d2):
            if d2 <= d1:
                return 0
            else:
                d1 = datetime.strptime(d1, "%Y-%m-%d")
                d2 = datetime.strptime(d2, "%Y-%m-%d")
                return abs((d2 - d1).days)

        def qui():
            if len(a.get()) == '0':
                messagebox.showerror("Error","Please Enter The Book Id")
            else:
                try:
                    self.conn = sqlite3.connect('library_administration.db')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select SID from issue where BID = ?", [a.get()])
                    sid = list(self.mycursor.fetchone())
                    self.mycursor.execute("Select Books_Issued from students where Student_Id = ?", [sid[0]])
                    gsid = list(self.mycursor.fetchone())
                    gsid[0] = gsid[0] - 1
                    self.mycursor.execute("Select BID from issue where BID = ?",[a.get()])
                    temp = self.mycursor.fetchone()
                    self.mycursor.execute("Select Fine from students where Student_Id = ?", [sid[0]])
                    fine = self.mycursor.fetchone()
                    self.mycursor.execute("Select Return_date from issue where BID = ? and SID = ?", [a.get(), sid[0]])
                    temp1 = self.mycursor.fetchone()
                    da = str(date.today())
                    ea = str(temp1[0])
                    self.cal = days_between(ea, da)
                    self.cal += int(fine[0])
                    if da <= ea and int(self.cal) == 0:
                        self.mycursor.execute("DELETE FROM issue WHERE BID = ?", [a.get()])
                        self.mycursor.execute("update books set Availiability = 1 where Book_Id = ?", [a.get()])
                        self.mycursor.execute("update students set Books_Issued = ? where Student_Id = ?", [gsid[0],sid[0]])
                        self.conn.commit()
                        self.conn.close()
                        messagebox.showinfo('Info', 'Succesfully Returned')
                        d = messagebox.askyesno("Confirm", "Return more books?")
                        if d:
                            self.destroy()
                            os.system('%s %s' % (py, 'ret.py'))
                        else:
                            self.destroy()
                    elif len(temp) > 0:
                        if int(self.cal) > 0:
                            messagebox.showinfo('Warning','Please Return/Renew book Timely to avoid termination of id')
                            self.mycursor.execute("Update students set Fine = ? where Student_Id = ?",[int(self.cal), sid[0]])
                            self.mycursor.execute("DELETE FROM issue WHERE BID = ?", [a.get()])
                            self.mycursor.execute("update books set Availiability = 1 where Book_Id = ?", [a.get()])
                            self.mycursor.execute("update students set Books_Issued = ? where Student_Id = ?", [gsid[0],sid[0]])
                            self.conn.commit()
                            self.conn.close()
                            messagebox.showinfo('Info', 'Succesfully Returned')
                            d = messagebox.askyesno("Confirm", "Return more books?")
                            if d:
                                self.destroy()
                                os.system('%s %s' % (py, 'ret.py'))
                            else:
                                self.destroy()
                        else:
                            self.mycursor.execute("DELETE FROM issue WHERE BID = ?", [a.get()])
                            self.mycursor.execute("update books set Availiability = 1 where Book_Id = ?", [a.get()])
                            self.mycursor.execute("update students set Books_Issued = ? where Student_Id = ?", [gsid[0],sid[0]])
                            self.conn.commit()
                            self.conn.close()
                            messagebox.showinfo('Info', 'Succesfully Returned')
                            d = messagebox.askyesno("Confirm", "Return more books?")
                            if d:
                                self.destroy()
                                os.system('%s %s' % (py, 'ret.py'))
                            else:
                                self.destroy()
                    else:
                        messagebox.showinfo("Oop's", "Book not yet issued")
                except Error:
                    messagebox.showerror("Error","Something Goes Wrong")
        Label(self, text='Return Book', fg='red',font=('arial', 35, 'bold')).pack()
        Label(self, text='Enter Book ID', font=('Comic Scan Ms', 15, 'bold')).place(x=20, y=120)
        Entry(self, textvariable=a, width=40).place(x=165, y=124)
        Button(self, text="Return", width=25, command=qui).place(x=180, y=180)
ret().mainloop()