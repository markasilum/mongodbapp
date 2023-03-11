import pymongo
import tkinter as tk
from tkinter import messagebox
from subprocess import call
from tkinter import *

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["enrollmentsystem"]
mycol= mydb["teachers"]

window = tk.Tk()
window.title("Students Form")
window.geometry("1500x400")
window.configure(bg="orange")

lst = [["ID","Name","Dept","Contact"]]

clicked = StringVar()
contfltr = tk.StringVar()
dStart = tk.StringVar()
nEnd = tk.StringVar()
nStart = tk.StringVar()
fid = tk.StringVar()

idfilter = 0
teachnameFilter = ""
teachnameFilter2 = ""
deptFilter = ""
conFilter = ""
filtercursor = {}
def callback(event):
    li=[]
    li = event.widget._values
    tid.set(lst[li[1]] [0])
    tname.set(lst[li[1]] [1])
    dept.set(lst[li[1]] [2])
    cont.set(lst[li[1]] [3])

def setFilter():
    global idfilter
    global teachnameFilter
    global teachnameFilter2
    global deptFilter
    global conFilter
    global operator
    global filtercursor

    if(fid.get() == ''):
        idfilter = 0
    else:
        idfilter = int(fid.get())
    
    
    teachnameFilter = str(nStart.get())
    teachnameFilter2 = str(nEnd.get())
    deptFilter = str(dStart.get())
    conFilter = str(contfltr.get())

    startNameFilter = "^"+teachnameFilter
    endNameFilter = teachnameFilter2+"$"
    deptStartFilter = "^"+deptFilter
    
    

    if(clicked.get() == "="):
        operator = "$eq"
    elif(clicked.get()== ">"):
        operator = "$gt"
    elif(clicked.get()== ">="):
        operator = "$gte"
    elif(clicked.get()== "<"):
        operator = "$lt"
    elif(clicked.get()== "<="):
        operator = "$lte"
    else:
        operator = "$ne"
    
    #Individual filters
    if(idfilter != ''):
        filtercursor["teacherid"] = {operator:idfilter}

    
   
    
    if(teachnameFilter != '' and teachnameFilter2 == ''):
        filtercursor["teachername"] = {"$regex":startNameFilter}
    else:
        if("teachername" in filtercursor and teachnameFilter2 ==''):
            filtercursor.pop("teachername")

    if(teachnameFilter2 != '' and teachnameFilter == ''):
        filtercursor["teachername"] = {"$regex":endNameFilter}
    else:
        if("teachername" in filtercursor and teachnameFilter ==''):
            filtercursor.pop("teachername")
    

    if(deptFilter != ''):
        filtercursor["teacherdept"] = {"$regex":deptStartFilter}
    else:
        if("teacherdept" in filtercursor):
            filtercursor.pop("teacherdept")

    if(conFilter != ''):
        filtercursor["teachercont"] = conFilter
    else:
        if("teachercont" in filtercursor):
            filtercursor.pop("teachercont")

    for x in filtercursor:
        print(filtercursor[x])

    creategrid(3)
    creategrid(2)
    
    if(teachnameFilter != '' and teachnameFilter2 != ''):
        # filtercursor = {"studname":{"$regex":startNameFilter}}, {"studname":{"$regex":endNameFilter}}
        creategrid(5)
        creategrid(4)
    else:
        if("teachername" in filtercursor and teachnameFilter =='' and teachnameFilter2 ==''):
            filtercursor.pop("teachername")
def creategrid(n):
    lst.clear()
    lst.append(["ID","Name","Dept","Contact"])

    startNameFilter = "^"+teachnameFilter
    endNameFilter = teachnameFilter2+"$"
    deptStartFilter = "^"+deptFilter

    cursor = ""
    if(n == 0):
        cursor = mycol.find({})
    elif(n==2 or n==4):
        if(n==2):
            cursor = mycol.find({"$and":[filtercursor]})
        else:
            cursor = mycol.find({"$and":[{"teachername":{"$regex":startNameFilter}}, {"teachername":{"$regex":endNameFilter}}]})

    for text_fromDB in cursor:
        teacherid = str(text_fromDB['teacherid'])
        teachername = str(text_fromDB['teachername'].encode('utf-8').decode("utf-8"))
        teacherdept = str(text_fromDB['teacherdept'.encode('utf-8').decode("utf-8")])
        teachercont = str(text_fromDB['teachercont'.encode('utf-8').decode("utf-8")])
        lst.append([teacherid,teachername,teacherdept,teachercont])
    
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            mygrid = tk.Entry(window, width = 10)
            mygrid.insert(tk.END,lst[i][j])
            mygrid._values = mygrid.get(), i
            mygrid.grid(row=i+7, column=j+4, sticky="E")
            mygrid.bind("<Button-1>", callback)
    
    if (n==1 or n==3 or n==5):
        for label in window.grid_slaves():
            if int(label.grid_info()["row"]) > 6:
                label.grid_forget()

def msgbox(msg,titlebar):
    result=messagebox.askokcancel(title=titlebar,message=msg)
    return result

def save():
    r=msgbox("Save Record?","Record")
    if r==True:
        newid = mycol.count_documents({})
        if newid != 0:
            newid = mycol.find_one(sort=[("teacherid",-1)])["teacherid"]
        id = newid+1
        tid.set(id)
        mydict = {"teacherid": int(teacherid.get()), "teachername": teachername.get(), "teacherdept":teacherdept.get(), "teachercont":teachercont.get()}
        x = mycol.insert_one(mydict)

        creategrid(1)
        creategrid(0)

def delete():
    r = msgbox("Delete?","Record")
    if r==True:
        myquery = {"teacherid": int(teacherid.get())}
        mycol.delete_one(myquery)
        
        creategrid(1)
        creategrid(0)

def update():
    r = msgbox("Update?","Record")
    if r==True:
        myquery = {"teacherid": int(teacherid.get())}
        
        newvalues = {"$set":{"teachername":teachername.get()}}
        mycol.update_one(myquery, newvalues)

        newvalues = {"$set":{"teacherdept":teacherdept.get()}}
        mycol.update_one(myquery, newvalues)

        newvalues = {"$set":{"teachercont":teachercont.get()}}
        mycol.update_one(myquery, newvalues)

        creategrid(1)
        creategrid(0)

def teachersform():
   call(["python", "teachers.py"])
def subjectsform():
   call(["python", "subjects.py"])

def filter():
    test = ""




label = tk.Label(window, text="Teachers Form", width = 30, height =1, bg="yellow", anchor="center")
label.config(font=("Courier",10))
label.grid(column=2,row=1)

label = tk.Label(window, text="Teacher's ID", width = 15, height =1, bg="yellow")
label.grid(column=1,row=2)
tid = tk.StringVar()
teacherid = tk.Entry(window, textvariable=tid) 
teacherid.grid(column=2,row=2)
teacherid.configure(state=tk.DISABLED)


label = tk.Label(window, text="Teacher's Name", width = 15, height =1, bg="yellow")
label.grid(column=1,row=3)
tname = tk.StringVar()
teachername = tk.Entry(window, textvariable=tname) 
teachername.grid(column=2,row=3)

label = tk.Label(window, text="Department", width = 15, height =1, bg="yellow")
label.grid(column=1,row=4)
dept = tk.StringVar()
teacherdept = tk.Entry(window, textvariable=dept) 
teacherdept.grid(column=2,row=4)

label = tk.Label(window, text="Contact", width = 15, height =1, bg="yellow")
label.grid(column=1,row=5)
cont = tk.StringVar()
teachercont = tk.Entry(window, textvariable=cont) 
teachercont.grid(column=2,row=5)


creategrid(0)

savebtn = tk.Button(text="Save",command=save)
savebtn.grid(column=1, row = 6)
savebtn = tk.Button(text="Delete",command=delete)
savebtn.grid(column=2, row = 6)
savebtn = tk.Button(text="Update", command=update)
savebtn.grid(column=3, row = 6)


#filter
label = tk.Label(window, text="Filter:",  height =1, bg="yellow")
label.grid(column=4,row=3)

label = tk.Label(window, text="ID:",  height =1, bg="yellow")
label.grid(column=4,row=4)

label = tk.Label(window, text="Name Start", height =1, bg="yellow")
label.grid(column=5,row=3)

nameStart = tk.Entry(window, textvariable=nStart,width = 10) 
nameStart.grid(column=5,row=4)

idFilter = tk.Entry(window, textvariable=fid,width= 10) 
idFilter.grid(column=4,row=6)

label = tk.Label(window, text="Name End",  width = 8 ,height =1, bg="yellow")
label.grid(column=5,row=5)

nameEnd = tk.Entry(window, textvariable=nEnd,width = 10) 
nameEnd.grid(column=5,row=6)

label = tk.Label(window, text="Dept Start",  width = 8 ,height =1, bg="yellow")
label.grid(column=6,row=5)

deptStart = tk.Entry(window, textvariable=dStart,width = 10) 
deptStart.grid(column=6,row=6)

label = tk.Label(window, text="Contact", width = 8 ,height =1, bg="yellow")
label.grid(column=7,row=5)

contactFilter = tk.Entry(window, textvariable=contfltr,width = 10) 
contactFilter.grid(column=7,row=6)

filterbtn = tk.Button(text="Filter", command=setFilter)
filterbtn.grid(column=8, row = 6)


options = [
    ">",
    ">=",
    "<",
    "<=",
    "!=",
    "="
]


clicked.set(">")

drop = OptionMenu(window, clicked, *options)
drop.grid(column=4,row=5)








window.mainloop()
