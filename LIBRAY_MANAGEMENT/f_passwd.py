from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from sqlite3 import Error


#creating window
class Fp(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'libico.ico')
        self.maxsize(480, 320)
        self.title("Forget Password")
        self.canvas = Canvas(width=500, height=500, bg='black')
        self.canvas.pack()
        self.photo = PhotoImage(file='forgot.png')
        self.canvas.create_image(-20, -20, image=self.photo, anchor=NW)
        #creating variables
        a = StringVar()
        b = StringVar()
        c = StringVar()
        d = StringVar()
        e = StringVar()
        #verifying input
        def ins():
            if (len(d.get())) < 8 or len(e.get()) < 8:
                while True:
                    if not re.search("[a-z]", d.get()):
                        flag = -1
                        break
                    elif not re.search("[A-Z]", d.get()):
                        flag = -1
                        break
                    elif not re.search("[0-9]", d.get()):
                        flag = -1
                        break
                    elif not re.search("[_@$]", d.get()):
                        flag = -1
                        break
                    elif re.search("\s", d.get()):
                        flag = -1
                        break
                    else:
                        flag = 0
                        break
                if len(d.get()) == 0:
                    messagebox.showinfo("Error","Please Enter Your Password")
                elif flag == -1:
                    messagebox.showinfo("Error","Minimum 8 characters.\nThe alphabets must be between [a-z]\nAt least one alphabet should be of Upper Case [A-Z]\nAt least 1 number or digit between [0-9].\nAt least 1 character from [ _ or @ or $ ].")
            elif d.get() != e.get():
                messagebox.showinfo("Error","New and retype password are not some")
            else:
                try:
                    self.conn = sqlite3.connect('library_administration.db')
                    self.myCursor = self.conn.cursor()
                    self.myCursor.execute("Update admin set password = ? where id = ?",[e.get(),a.get()])
                    self.conn.commit()
                    self.myCursor.close()
                    self.conn.close()
                    messagebox.showinfo("Confirm","Password Updated Successfuly")
                    self.destroy()
                except Error:
                    messagebox.showerror("Error","Something Goes Wrong")

        def check():
            if len(a.get()) < 5:
                messagebox.showinfo("Error","Please Enter User Id")
            elif len(b.get()) == 0:
                messagebox.showinfo("Error","Please Choose a question")
            elif len(c.get()) == 0:
                messagebox.showinfo("Error", "Please Enter a answer")
            else:
                try:
                    self.conn = sqlite3.connect('library_administration.db')
                    self.myCursor = self.conn.cursor()
                    self.myCursor.execute("Select id,secQuestion,secAnswer from admin where id = ?",[a.get()])
                    pc = self.myCursor.fetchone()
                    if not pc:
                        messagebox.showinfo("Error", "Something Wrong in the Details")
                    elif str(pc[0]) == a.get() or str(pc[1]) == b.get() or str(pc[2]) == c.get():
                        Label(self, text="New Password", font=('arial', 15, 'bold')).place(x=40, y=220)
                        Entry(self, show = "*", textvariable=d, width=40).place(x=230, y=224)
                        Label(self, text="Retype Password", font=('arial', 15, 'bold')).place(x=40, y=270)
                        Entry(self, show = "*", textvariable=e, width=40).place(x=230, y=274)
                        Button(self, text="Submit", width=15, command=ins).place(x=230, y=324)
                except Error:
                    messagebox.showerror("Error","Something Goes Wrong")

        #label and input box
        Label(self, text="Enter User Id",bg='black',fg='white', font=('arial', 15, 'bold')).place(x=40, y=20)
        Label(self, text="Security Question",bg='black',fg='white',font=('arial', 15, 'bold')).place(x=40, y= 70)
        Label(self, text="Security Answer",bg='black',fg='white',font=('arial', 15, 'bold')).place(x=40, y= 120)
        Entry(self, textvariable=a, width=40).place(x=230, y=24)
        ttk.Combobox(self, textvariable = b,values=["What is your school name?", "What is your home name?","What is your Father name?", "What is your pet name?"], width=37,state="readonly").place(x=230, y=74)
        Entry(self, show = "*", textvariable=c, width=40).place(x=230, y=124)
        Button(self, text='Verify', width=15,command = check).place(x=275, y=170)

Fp().mainloop()
