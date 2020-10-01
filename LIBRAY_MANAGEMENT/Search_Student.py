from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from sqlite3 import Error
from PIL import ImageTk,Image
import os,glob


class Sst(Tk):
    def __init__(self):
        super().__init__()
        f = StringVar()
        g = StringVar()
        self.title("Search Student")
        self.maxsize(770,420)
        self.canvas = Canvas(width=1366, height=768, bg='black')
        self.canvas.pack()
        self.photo = PhotoImage(file='searchstudent.png')
        self.canvas.create_image(-20, -20, image=self.photo, anchor=NW)
        self.iconbitmap(r'libico.ico')
        l1=Label(self,text="Search Student",font=("Algerian",20,'bold')).place(x=290,y=40)
        l = Label(self, text="Search By", font=("Arial", 15, 'bold')).place(x=180, y=100)
        def writeTofile(data,filename):
            with open(filename,'wb') as file:
                file.write(data)

        def insert(data):
            self.listTree.delete(*self.listTree.get_children())
            for row in data:
                self.listTree.insert("","end",text = row[2], values = (row[1],row[4],row[6]))

        def photo(pic):
            try:
                self.conn = sqlite3.connect('library_administration.db')
                self.mycursor = self.conn.cursor()
                self.mycursor.execute("Select * from students where Student_Id = ?", [pic])
                pc = self.mycursor.fetchone()
                if pc[5] != '':
                    photoPath = "Temp Images\\" + pc[1] + ".jpeg"
                    writeTofile(pc[5], photoPath)
                    self.photo = ImageTk.PhotoImage(Image.open("Temp Images\\" + pc[1] + ".jpeg"))
                    Label(image=self.photo, width=150, height=150).place(x=625, y=20)
                    filelist = glob.glob("Temp Images\*.jpeg")
                    for file in filelist:
                        os.remove(file)
                else:
                    self.photo = ImageTk.PhotoImage(Image.open("Temp Images\\48-512.png"))
                    Label(image=self.photo, width=150, height=150).place(x=625, y=20)
            except Error:
                messagebox.showerror("Error", "Something goes wrong")

#clicking the record will open the picture
        def select(a):
            curItem = self.listTree.focus()
            selItem = self.listTree.item(curItem)
            pic = str(selItem['text'])
            photo(pic)


        def ge():
            if (len(g.get())) == 0:
                messagebox.showinfo('Error', 'First select a item')
            elif (len(f.get())) == 0:
                messagebox.showinfo('Error', 'Enter the '+g.get())
            elif g.get() == 'Name':
                try:
                    self.conn = sqlite3.connect('library_administration.db')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select * from students where name like ?",['%'+f.get()+'%'])
                    pc = self.mycursor.fetchall()
                    if pc:
                        insert(pc)
                    else:
                        messagebox.showinfo("Oop's","Name not found")
                except Error:
                    messagebox.showerror("Error", "Something goes wrong")
            elif g.get() == 'ID':
                try:
                    self.conn = sqlite3.connect('library_administration.db')
                    self.mycursor = self.conn.cursor()
                    self.mycursor.execute("Select * from students where Student_Id like ?", ['%' + f.get() + '%'])
                    pc = self.mycursor.fetchall()
                    if pc:
                        insert(pc)
                    else:
                        messagebox.showinfo("Oop's", "Id not found")
                except Error:
                    messagebox.showerror("Error", "Something goes wrong")


        b=Button(self,text="Find",width=8,font=("Arial",8,'bold'),command=ge).place(x=400,y=170)
        c=ttk.Combobox(self,textvariable=g,values=["Name","ID"],width=40,state="readonly").place(x = 310, y = 105)
        en = Entry(self,textvariable=f,width=43).place(x=310,y=145)
        la = Label(self, text="Enter", font=("Arial", 15, 'bold')).place(x=180, y=140)

        def handle(event):
            if self.listTree.identify_region(event.x,event.y) == "separator":
                return "break"


        self.listTree = ttk.Treeview(self, height=13,columns=('Student Name', 'Phone Number', 'No. Of Books Issued'))
        self.vsb = ttk.Scrollbar(self,orient="vertical",command=self.listTree.yview)
        self.listTree.configure(yscrollcommand=self.vsb.set)
        self.listTree.heading("#0", text='Student ID', anchor='w')
        self.listTree.column("#0", width=100, anchor='w')
        self.listTree.heading("Student Name", text='Student Name')
        self.listTree.column("Student Name", width=200, anchor='center')
        self.listTree.heading("Phone Number", text='Phone Number')
        self.listTree.column("Phone Number", width=200, anchor='center')
        self.listTree.heading("No. Of Books Issued", text='No. Of Books Issued')
        self.listTree.column("No. Of Books Issued", width=200, anchor='center')
        self.listTree.bind("<Button-1>", handle)
        self.listTree.bind("<ButtonRelease-1>",select)
        self.listTree.place(x=40, y=200)
        self.vsb.place(x=743,y=200,height=287)
        ttk.Style().configure("Treeview", font=('Times new Roman', 15))

Sst().mainloop()