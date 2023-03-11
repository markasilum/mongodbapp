import pymongo
import tkinter as tk
from tkinter import messagebox
from subprocess import call
from tkinter import *

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["enrollmentsystem"]
mycol= mydb["students"]

lst = [["ID","Name","Email","Course"]]


window = tk.Tk()
window.title("Students Form")
window.geometry("1500x400")
window.configure(bg="orange")

fid = tk.StringVar()
nStart = tk.StringVar()
nEnd = tk.StringVar()
mStart = tk.StringVar() 
crs = tk.StringVar()
clicked = StringVar()

idfilter = 0
operator = ""

studnameFilter = ""
studnameFilter2 = ""
studemailFilter = ""
crsFilter = ""
testDict = {}
filtercursor = {}



def callback(event):
    li=[]
    li = event.widget._values
    sid.set(lst[li[1]] [0])
    sname.set(lst[li[1]] [1])
    semail.set(lst[li[1]] [2])
    scourse.set(lst[li[1]] [3])


def setFilter():
    global idfilter
    global studnameFilter
    global studnameFilter2
    global studemailFilter
    global crsFilter
    global operator
    global filtercursor

    if(fid.get() == ''):
        idfilter = 0
    else:
        idfilter = int(fid.get())
    
    studnameFilter = str(nStart.get())
    studnameFilter2 = str(nEnd.get())
    studemailFilter = str(mStart.get())
    crsFilter = str(crs.get())

    startNameFilter = "^"+studnameFilter
    endNameFilter = studnameFilter2+"$"
    emailStartFilter = "^"+studemailFilter
    
    

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
        filtercursor["studid"] = {operator:idfilter}

    
    
    
    if(studnameFilter != '' and studnameFilter2 == ''):
        filtercursor["studname"] = {"$regex":startNameFilter}
    else:
        if("studname" in filtercursor and studnameFilter2 ==''):
            filtercursor.pop("studname")
    if(studnameFilter2 != '' and studnameFilter == ''):
        filtercursor["studname"] = {"$regex":endNameFilter}
    else:
        if("studname" in filtercursor and studnameFilter ==''):
            filtercursor.pop("studname")
    

    if(studemailFilter != ''):
        filtercursor["studemail"] = {"$regex":emailStartFilter}
    else:
        if("studemail" in filtercursor):
            filtercursor.pop("studemail")

    if(crsFilter != ''):
        filtercursor["studcourse"] = crsFilter
    else:
        if("studcourse" in filtercursor):
            filtercursor.pop("studcourse")

    for x in filtercursor:
        print(filtercursor[x])

    creategrid(3)
    creategrid(2)
    
    if(studnameFilter != '' and studnameFilter2 != ''):
        # filtercursor = {"studname":{"$regex":startNameFilter}}, {"studname":{"$regex":endNameFilter}}
        creategrid(5)
        creategrid(4)
    else:
        if("studname" in filtercursor and studnameFilter2 =='' and studnameFilter ==''):
            filtercursor.pop("studname")

def creategrid(n):
    lst.clear()
    lst.append(["ID","Name","Email","Course"])

    
    startNameFilter = "^"+studnameFilter
    endNameFilter = studnameFilter2+"$"
    emailStartFilter = "^"+studemailFilter
    
    cursor = ""
    if(n == 0):
        cursor = mycol.find({})
    elif(n==2 or n==4):
        if(n==2):
            cursor = mycol.find({"$and":[filtercursor]})
        else:
            cursor = mycol.find({"$and":[{"studname":{"$regex":startNameFilter}}, {"studname":{"$regex":endNameFilter}}]})   
    
        
        

    for text_fromDB in cursor:
        studid = str(text_fromDB['studid'])
        studname = str(text_fromDB['studname'].encode('utf-8').decode("utf-8"))
        studemail = str(text_fromDB['studemail'.encode('utf-8').decode("utf-8")])
        studcourse = str(text_fromDB['studcourse'.encode('utf-8').decode("utf-8")])
        lst.append([studid,studname,studemail,studcourse])
    
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            mygrid = tk.Entry(window, width = 10)
            mygrid.insert(tk.END,lst[i][j])
            mygrid._values = mygrid.get(), i
            mygrid.grid(row=i+7, column=j+4,sticky="E")
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
            newid = mycol.find_one(sort=[("studid",-1)])["studid"]
        id = newid+1
        sid.set(id)
        mydict = {"studid": int(studid.get()), "studname": studname.get(), "studemail":studemail.get(), "studcourse":studcourse.get()}
        x = mycol.insert_one(mydict)

        creategrid(1)
        creategrid(0)

def delete():
    r = msgbox("Delete?","Record")
    if r==True:
        myquery = {"studid": int(studid.get())}
        mycol.delete_one(myquery)
        
        creategrid(1)
        creategrid(0)

def update():
    r = msgbox("Update?","Record")
    if r==True:
        myquery = {"studid": int(studid.get())}
        
        newvalues = {"$set":{"studname":studname.get()}}
        mycol.update_one(myquery, newvalues)

        newvalues = {"$set":{"studemail":studemail.get()}}
        mycol.update_one(myquery, newvalues)

        newvalues = {"$set":{"studcourse":studcourse.get()}}
        mycol.update_one(myquery, newvalues)

        creategrid(1)
        creategrid(0)

def teachersform():
   call(["python", "teachers.py"])
def subjectsform():
   call(["python", "subjects.py"])


def filter():
    test = ""



menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Subjects", command = subjectsform)
filemenu.add_command(label="Teachers", command = teachersform)
filemenu.add_separator()
filemenu.add_command(label="Close", command=window.quit)

editmenu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Edit", menu=editmenu)
editmenu.add_command(label="Undo", command = subjectsform)
editmenu.add_separator()
editmenu.add_command(label="Cut", command = subjectsform)


window.config(menu= menubar)

label = tk.Label(window, text="Student Enlistment Form", width = 30, height =1, bg="yellow", anchor="center")
label.config(font=("Courier",10))
label.grid(column=2,row=1)

label = tk.Label(window, text="Student ID", width = 15, height =1, bg="yellow")
label.grid(column=1,row=2)
sid = tk.StringVar()
studid = tk.Entry(window, textvariable=sid) 
studid.grid(column=2,row=2)
studid.configure(state=tk.DISABLED)


label = tk.Label(window, text="Student Name", width = 15, height =1, bg="yellow")
label.grid(column=1,row=3)
sname = tk.StringVar()
studname = tk.Entry(window, textvariable=sname) 
studname.grid(column=2,row=3)

label = tk.Label(window, text="Student Email", width = 15, height =1, bg="yellow")
label.grid(column=1,row=4)
semail = tk.StringVar()
studemail = tk.Entry(window, textvariable=semail) 
studemail.grid(column=2,row=4)

label = tk.Label(window, text="Student Course", width = 15, height =1, bg="yellow")
label.grid(column=1,row=5)
scourse = tk.StringVar()
studcourse = tk.Entry(window, textvariable=scourse) 
studcourse.grid(column=2,row=5)


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

label = tk.Label(window, text="Mail Start",  width = 8 ,height =1, bg="yellow")
label.grid(column=6,row=5)

mailStart = tk.Entry(window, textvariable=mStart,width = 10) 
mailStart.grid(column=6,row=6)

label = tk.Label(window, text="Course", width = 8 ,height =1, bg="yellow")
label.grid(column=7,row=5)

courseFilter = tk.Entry(window, textvariable=crs,width = 10) 
courseFilter.grid(column=7,row=6)

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
