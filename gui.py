from tkinter import *
from tkinter import messagebox
import mysql.connector

root = Tk()
db = mysql.connector.connect(host = "localhost",
                             user = "root",
                             password = "",
                             database = "collage")
mycursor = db.cursor()
def search():
    id = txtid.get()
    if id!="":
        sql = "SELECT * FROM stud WHERE id = %s"
        val = (id,)
        mycursor.execute(sql,val)
        myresult = mycursor.fetchall()
        count = len(myresult)
        if count >=1 :
            for i in myresult:
                txtname.delete(0,END)
                txtres.delete(0,END)
                txtsid.insert(1,i[2])
                txtname.insert(1,i[0])
                txtres.insert(1,i[1])
        else:
            txtname.delete(0,END)
            txtres.delete(0,END)
            messagebox.showinfo("Database","No Data Found.")



         
def insert():
    id = txtsid.get()
    nm = txtname.get()
    res = txtres.get()
    if nm!="" and res!="":    
        sql = "INSERT INTO stud (id,name,result) VALUES (%s,%s,%s)"
        val = (id,nm,res,)
        mycursor.execute(sql,val)
        db.commit()
        count = mycursor.rowcount
        if count == 1:
             messagebox.showinfo("Database","Inserted Successfully.")
             clear() 
        else:
            messagebox.showinfo("Database","No Inserted Any Record.")
    else:
        messagebox.showwarning("Database","Enter All Fields.")
   

def update():
    id = txtid.get()
    sid = txtsid.get()
    nm = txtname.get()
    res = txtres.get()
    if nm!="" and res!="" and id!="":    
        sql = "UPDATE stud SET name=%s , result=%s ,id=%s WHERE id=%s"
        val = (nm,res,sid,id,)
        mycursor.execute(sql,val)
        db.commit()
        count = mycursor.rowcount
        if count == 1:
             messagebox.showinfo("Database","Upadated Successfully.") 
             clear()
        else:
            messagebox.showinfo("Database","Update Record Failed.")
    else:
        messagebox.showwarning("Database","Enter All Fields.")
    
def delete():
    id = txtid.get()
    
    if id!="":    
        sql = "DELETE FROM stud WHERE id=%s"
        val = (id,)
        mycursor.execute(sql,val)
        db.commit()
        count = mycursor.rowcount
        if count == 1:
             messagebox.showinfo("Database","Deleted Successfully.") 
             clear()

        else:
            messagebox.showinfo("Database","Deletion Failed.")
    else:
        messagebox.showwarning("Database","Enter ID For Delete.")

def clear():
    txtname.delete(0,END)
    txtres.delete(0,END)
    txtid.delete(0,END)
    txtsid.delete(0,END)

Label(root,text="Enter Id For Search").pack()
txtid = Entry(root)
txtid.pack()
Button(root,text="Search",command=search).pack()
Label(root,text="Enter ID").pack()
txtsid = Entry(root)
txtsid.pack()
Label(root,text="Enter Name").pack()
txtname = Entry(root)
txtname.pack()
Label(root,text="Enter Result").pack()
txtres = Entry(root)
txtres.pack()
Button(root,text="Insert",command=insert).pack()
Button(root,text="Update",command=update).pack()
Button(root,text="Delete",command=delete).pack()
Button(root,text="Clear",command=clear).pack()
root.mainloop()