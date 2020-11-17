from tkinter import *
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
import os
import sys
from tkinter import ttk
py=sys.executable

#creating window
class MainWin(Tk):
    def __init__(self):
        super().__init__()
        self.iconbitmap(r'libico.ico')
        self.configure(bg='black')
        self.canvas = Canvas(width=1366, height=768, bg='black')
        self.canvas.pack()
        self.photo = PhotoImage(file='sset2.png')
        self.canvas.create_image(-20, -20, image=self.photo, anchor=NW)
        self.maxsize(1320, 768)
        self.minsize(1320,768)
        self.state('zoomed')
        self.title('SHEPHERD LIBRARY MANAGEMENT SYSTEMS(SLIMS)')
        self.a = StringVar()
        self.b = StringVar()
        self.mymenu = Menu(self)
#calling scripts
        def a_s():
            os.system('%s %s' % (py, 'Add_Student.py'))

        def a_b():
            os.system('%s %s' % (py, 'Add_Books.py'))

        def r_b():
            os.system('%s %s' % (py, 'remove_book.py'))

        def r_s():
            os.system('%s %s' % (py, 'Remove_student.py'))

        def ib():
            os.system('%s %s' % (py, 'issueTable.py'))

        def rb1():
            os.system('%s %s' % (py, 'renew.py'))

        def ret():
            os.system('%s %s' % (py, 'ret.py'))

        def sea():
            os.system('%s %s' % (py,'Search.py'))

        def log():
             self.destroy()
             os.system('%s %s' % (py, 'main.py'))
             exit()


      # def handle(event):
        #     if self.listTree.identify_region(event.x,event.y) == "separator":
        #         return "break"
        def add_user():
            os.system('%s %s' % (py, 'Reg.py'))
        def rem_user():
            os.system('%s %s' % (py, 'Rem.py'))
        def cfine():
            os.system('%s %s' % (py,'fine.py'))
        def sest():
            os.system('%s %s' % (py,'Search_Student.py'))

#creating table

        self.listTree = ttk.Treeview(self,height=14,columns=('SID','Name','Fine','Book Name','Issue Date','Return Date'))
        self.vsb = ttk.Scrollbar(self,orient="vertical",command=self.listTree.yview)
        self.hsb = ttk.Scrollbar(self,orient="horizontal",command=self.listTree.xview)
        self.listTree.configure(yscrollcommand=self.vsb.set,xscrollcommand=self.hsb.set)
        self.listTree.heading("#0",text='Book ID',anchor = 'center')
        self.listTree.column("#0",width=100,minwidth=100,anchor='center')
        self.listTree.heading("#1", text='SID')
        self.listTree.column("#1",width=100,minwidth=100,anchor='center')
        self.listTree.heading("Name", text='Name')
        self.listTree.column("Name", width=150,minwidth=150,anchor='center')
        self.listTree.heading("Fine", text='Fine')
        self.listTree.column("Fine", width=100,minwidth=100,anchor='center')
        self.listTree.heading("Book Name", text='Book Name')
        self.listTree.column("Book Name", width=200, minwidth=200,anchor='center')
        self.listTree.heading("Return Date", text='Return Date')
        self.listTree.column("Return Date", width=125, minwidth=125,anchor='center')
        self.listTree.heading("Issue Date", text='Issue Date')
        self.listTree.column("Issue Date", width=125, minwidth=125,anchor='center')
        # self.listTree.bind('<Button-1>',handle) if you don't want to expand column activat this and the above handle function
        self.listTree.place(x=220,y=360)
        self.vsb.place(x=1123,y=361,height=287)
        self.hsb.place(x=220,y=650,width=922)
        ttk.Style().configure("Treeview",font=('Times new Roman',15))

        list1 = Menu(self)
        list1.add_command(label="Student", command=a_s)
        list1.add_command(label="Book", command=a_b)

        list2 = Menu(self)
        list2.add_command(label="Student", command=r_s)
        list2.add_command(label="Book", command=r_b)

        list3 = Menu(self)
        list3.add_command(label = "Add User",command = add_user)
        list3.add_command(label = "Remove User",command = rem_user)


        self.mymenu.add_cascade(label='Add', menu=list1)
        self.mymenu.add_cascade(label='Remove', menu=list2)
        self.mymenu.add_cascade(label = 'Admin Tools', menu = list3)

        self.config(menu=self.mymenu)

        def ser():
            try:
                self.conn = sqlite3.connect('library_administration.db')
                self.myCursor = self.conn.cursor()
                self.change = int(self.a.get())
                self.myCursor.execute("Select issue.BID,issue.SID,students.name,students.Fine,books.Book_name,issue.Issue_date,issue.Return_date from books,students,issue where issue.BID = books.Book_Id and SID = ?",[self.change])
                self.pc = self.myCursor.fetchall()
                if self.pc:
                    self.listTree.delete(*self.listTree.get_children())
                    for row in self.pc:
                        self.listTree.insert("",'end',text=row[0] ,values = (row[1],row[2],row[3],row[4],row[5],row[6]))
                else:
                    messagebox.showinfo("Error", "Either ID is wrong or The book is not yet issued on this ID")
            except Error:
                messagebox.showerror("Error","Something Goes Wrong")
        def ent():
            try:
                self.conn = sqlite3.connect('library_administration.db')
                self.myCursor = self.conn.cursor()
                self.myCursor.execute("Select issue.BID,issue.SID,students.name,students.Fine,books.Book_name,issue.Issue_date,issue.Return_date from books,students, issue where issue.BID = books.Book_Id and BID = ?",[self.b.get()])
                self.pc = self.myCursor.fetchall()
                if self.pc:
                    self.listTree.delete(*self.listTree.get_children())
                    for row in self.pc:
                        self.listTree.insert("", 'end', text=row[0],values=(row[1], row[2], row[3], row[4], row[5],row[6]))
                else:
                    messagebox.showinfo("Error", "Please Enter a valid ID")
            except Error:
                messagebox.showerror("Error", "Something Goes Wrong")

        def check():
            try:
                conn = sqlite3.connect('library_administration.db')
                mycursor = conn.cursor()
                mycursor.execute("Select * from admin")
                z = mycursor.fetchone()
                if not z:
                    messagebox.showinfo("Error", "Please Register A user")
                    x = messagebox.askyesno("Confirm","Do you want to register a user")
                    if x:
                        self.destroy()
                        os.system('%s %s' % (py, 'Reg.py'))
                else:
                    #label and input box
                    self.label3 = Label(self, text='SHEPHERD LIBRARY MANAGEMENT SYSTEM',fg='black',bg="white" ,font=('AlGERIAN', 30, 'bold'))
                    self.label3.place(x=147, y=22)
                    self.label4 = Label(self, text="ENTER STUDENT", font=('Arial', 18, 'bold'))
                    self.label4.place(x=50, y=107)
                    self.e1 = Entry(self, textvariable=self.a, width=90).place(x=405, y=110)
                    self.srt = Button(self, text='Search', width=15, font=('arial', 10),command = ser).place(x=1000, y=106)
                    self.label5 = Label(self, text="ENTER THE BOOK ID", font=('Arial', 18, 'bold'))
                    self.label5.place(x=75, y=150)
                    self.e2 = Entry(self, textvariable=self.b, width=90).place(x=405, y=160)
                    self.brt = Button(self, text='Find', width=15, font=('arial', 10),command = ent).place(x=1000, y=150)
                    self.label6 = Label(self, text="INFORMATION DETAILS",  font=('Arial', 15, 'underline', 'bold'))
                    self.label6.place(x=510, y=300)
                    self.button = Button(self, text='Search Student', width=25, font=('Algerian', 10), command=sest).place(x=240,y=250)
                    self.button = Button(self, text='Search Book', width=25, font=('Algerian', 10), command=sea).place(x=470,y=250)
                    self.brt = Button(self, text="Issue Book", width=15, font=('Algerian', 10), command=ib).place(x=700, y=250)
                    self.brt = Button(self, text="Renew Book", width=15, font=('Algerian', 10), command=rb1).place(x=850, y=250)
                    self.brt = Button(self, text="Return Book", width=15, font=('Algerian', 10), command=ret).place(x=1000, y=250)
                    self.brt = Button(self, text="LOGOUT", width=15, font=('Algerian', 10), command=log).place(x=1150, y=105)
                    self.brt = Button(self, text="Fine Clear", width=15, font=('Algerian', 10), command=cfine).place(x=1150,y=150)
            except Error:
                messagebox.showerror("Error", "Something Goes Wrong")
        check()

MainWin().mainloop()
