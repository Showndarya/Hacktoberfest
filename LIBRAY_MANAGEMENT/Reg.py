from tkinter import *
from tkinter import messagebox
import re
from tkinter import ttk
import sqlite3
from sqlite3 import Error
import os,sys
py=sys.executable

#creating window
class reg(Tk):
    def __init__(self):
        super().__init__()
        self.title("SLIMS")
        self.maxsize(1366, 768)
        self.minsize(1366, 768)
        self.state("normal")
        self.iconbitmap(r'libico.ico')
        self.configure(background="black")
        self.canvas = Canvas(width=1366, height=768, bg='black')
        self.canvas.pack()
        self.photo = PhotoImage(file='reg.png')
        self.canvas.create_image(-20, -20, image=self.photo, anchor=NW)
#creating variables Please chech carefully
        z = StringVar()
        y = StringVar()
        x = StringVar()
        w = StringVar()
        v = StringVar()
        u = StringVar()
        s = StringVar()
        r = StringVar()

        def insert():
            try:
                self.conn = sqlite3.connect('library_administration.db')
                self.myCursor = self.conn.cursor()
                c = self.myCursor.execute("Insert into admin values (?,?,?,?,?,?,?)",[z.get(), y.get(), x.get(), w.get(), v.get(), s.get(), r.get()])
                self.conn.commit()
                self.myCursor.close()
                self.conn.close()
                if c:
                    messagebox.showinfo("Confirm", "Data Inserted Successfully")
                    self.destroy()
                    os.system('%s %s' % (py, 'Main.py'))
            except Error:
                messagebox.showinfo("Error", "Something Goes Wrong")
# verify input
        def verify():
            if(len(z.get())) < 5:
                messagebox.showinfo("Error","Enter User Id\nUser Id should be greater than 5 letters")
            elif (len(y.get())) < 3:
                messagebox.showinfo("Error", "Please Enter Your Full Name")
            elif (len(x.get())) < 8:
                while True:
                    if not re.search("[a-z]", x.get()):
                        flag = -1
                        break
                    elif not re.search("[A-Z]", x.get()):
                        flag = -1
                        break
                    elif not re.search("[0-9]", x.get()):
                        flag = -1
                        break
                    elif not re.search("[_@$]", x.get()):
                        flag = -1
                        break
                    elif re.search("\s", x.get()):
                        flag = -1
                        break
                    else:
                        flag = 0
                        break
                if len(x.get()) == 0:
                    messagebox.showinfo("Error","Please Enter Your Password")
                elif flag == -1:
                    messagebox.showinfo("Error","Minimum 8 characters.\nThe alphabets must be between [a-z]\nAt least one alphabet should be of Upper Case [A-Z]\nAt least 1 number or digit between [0-9].\nAt least 1 character from [ _ or @ or $ ].")
            elif len(w.get()) == 0:
                messagebox.showinfo("Error","Please select a question")
            elif len(v.get()) == 0:
                messagebox.showinfo("Error","Please write an answer")
            elif len(s.get()) == 0 or len(s.get()) > 10 or len(s.get()) < 10:
                messagebox.showinfo("Error","Enter Valid Phone Number")
            elif len(s.get()) == 10:
                if s.get().isdigit():
                    cas = re.fullmatch("[6-9][0-9]{9}", s.get())
                    if cas is None:
                        messagebox.showinfo("Error","Check Your Phone Number")
                    else:
                        insert()
#label and input
        Label(self,text="Library Management System",font=("Algerian",35,'bold'),fg="white",bg="black").place(x=100,y=80)
        Label(self,text="Enter your details and click save",font=("Arial",20,'bold'),fg="white",bg="black").place(x=200,y=600)
        Label(text = "Library Information",fg='white',font = ("Arial",13,"bold"),bg="black").place(x=300,y=220)
        Label( text="User ID",fg='white', font=("Arial", 13, "bold"), bg="black").place(x=100, y=260)
        Label( text="User - Name",fg='white', font=("Arial", 13, "bold"), bg="black").place(x=100, y=300)
        Label( text="User - Password",fg='white', font=("Arial", 13, "bold"), bg="black").place(x=100, y=340)
        Label( text="Security Question",fg='white', font=("Arial", 13, "bold"), bg="black").place(x=100, y=380)
        Label( text="Security Answer",fg='white', font=("Arial", 13, "bold"), bg="black").place(x=100, y=420)
        Label( text="Phone",fg='white', font=("Arial", 13, "bold"), bg="black").place(x=100, y=460)
        Label( text="City",fg='white', font=("Arial", 13, "bold"), bg="black").place(x=100, y=500)
        Entry(textvariable=z,width=60).place(x=250,y=260)
        Entry( textvariable=y, width=60).place(x=250, y=300)
        Entry( show = '*',textvariable=x, width=60).place(x=250, y=340)
        ttk.Combobox( textvariable = w, values=["What is your school name?", "What is your home name?","What is your Father name?", "What is your pet name?"], width=57,state="readonly").place(x=250, y=380)
        Entry( show = '*',textvariable=v, width=60).place(x=250, y=420)
        Entry( textvariable=s, width=60).place(x=250, y=460)
        Entry( textvariable=r, width=60).place(x=250, y=500)
        Button( text="Save", width=10, font=("Arial", 13, "bold"), command=verify).place(x=300, y=550)
        Button( text="Cancel", width=10, font=("Arial", 13, "bold")).place(x=460, y=550)

reg().mainloop()