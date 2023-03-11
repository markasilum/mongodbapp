import pymongo
import tkinter as tk
from tkinter import messagebox
from subprocess import call
from tkinter import *

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["enrollmentsystem"]
mycol= mydb["subjects"]

lst = [["ID","Code","Des","Unit","Sched"]]

window = tk.Tk()
window.title("Subject Form")
window.geometry("1500x400")
window.configure(bg="orange")

clicked = StringVar()
fid = tk.StringVar()
cStart = tk.StringVar()
cEnd = tk.StringVar()
dsStart = tk.StringVar()
uFilter = tk.StringVar()
schd = tk.StringVar()

idfilter = 0
operator = ""
codeFilter = ""
codeFilter2 = ""
desFilter = ""
untFilter = ""
schdFilter = ""

filtercursor = {}

def callback(event):
    li=[]
    li = event.widget._values
    sbid.set(lst[li[1]] [0])
    scode.set(lst[li[1]] [1])
    des.set(lst[li[1]] [2])
    unit.set(lst[li[1]] [3])
    sched.set(lst[li[1]] [4])

def setFilter():
    global idfilter
    global codeFilter
    global codeFilter2
    global desFilter
    global untFilter
    global schdFilter
    global operator
    global filtercursor

    if(fid.get() == ''):
        idfilter = 0
    else:
        idfilter = int(fid.get())
    
    
    codeFilter = str(cStart.get())
    codeFilter2 = str(cEnd.get())
    desFilter = str(dsStart.get())
    untFilter = str(uFilter.get())
    schdFilter = str(schd.get())

    startCodeFilter = "^"+codeFilter
    endCodeFilter = codeFilter2+"$"
    desStartFilter = "^"+desFilter
    
    

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
        filtercursor["subid"] = {operator:idfilter}

    
    if(codeFilter != '' and codeFilter2 == ''):
        filtercursor["subcode"] = {"$regex":startCodeFilter}
    else:
        if("subcode" in filtercursor and codeFilter2 ==''):
            filtercursor.pop("subcode")

    if(codeFilter2 != '' and codeFilter == ''):
        filtercursor["subcode"] = {"$regex":endCodeFilter}
    else:
        if("subcode" in filtercursor and codeFilter ==''):
            filtercursor.pop("subcode")
    

    if(desFilter != ''):
        filtercursor["subdes"] = {"$regex":desStartFilter}
    else:
        if("subdes" in filtercursor):
            filtercursor.pop("subdes")

    if(untFilter != ''):
        filtercursor["subunit"] = int(untFilter)
    else:
        if("subunit" in filtercursor):
            filtercursor.pop("subunit")

    if(schdFilter != ''):
        filtercursor["subsched"] = schdFilter
    else:
        if("subsched" in filtercursor):
            filtercursor.pop("subsched")

    for x in filtercursor:
        print(x,filtercursor[x])

    creategrid(3)
    creategrid(2)
    
    if(codeFilter != '' and codeFilter2 != ''):
        creategrid(5)
        creategrid(4)
    else:
        if("subcode" in filtercursor and codeFilter =='' and codeFilter2 ==''):
            filtercursor.pop("subcode")

def creategrid(n):
    lst.clear()
    lst.append(["ID","Code","Des","Unit","Sched"])

    startCodeFilter = "^"+codeFilter
    endCodeFilter = codeFilter2+"$"
    desStartFilter = "^"+desFilter

    cursor = ""
    if(n == 0):
        cursor = mycol.find({})
    elif(n==2 or n==4):
        if(n==2):
            cursor = mycol.find({"$and":[filtercursor]})
        else:
            cursor = mycol.find({"$and":[{"subcode":{"$regex":startCodeFilter}}, {"subcode":{"$regex":endCodeFilter}}]})

    for text_fromDB in cursor:
        subid = str(text_fromDB['subid'])
        subcode = str(text_fromDB['subcode'].encode('utf-8').decode("utf-8"))
        subdes = str(text_fromDB['subdes'.encode('utf-8').decode("utf-8")])
        subunit = str(text_fromDB['subunit'.encode('utf-8').decode("utf-8")])
        subsched = str(text_fromDB['subsched'.encode('utf-8').decode("utf-8")])
        lst.append([subid,subcode,subdes,subunit,subsched])
    
    for i in range(len(lst)):
        for j in range(len(lst[0])):
            mygrid = tk.Entry(window, width = 10)
            mygrid.insert(tk.END,lst[i][j])
            mygrid._values = mygrid.get(), i
            mygrid.grid(row=i+8, column=j+4)
            mygrid.bind("<Button-1>", callback)
    
    if (n==1 or n==3 or n==5):
        for label in window.grid_slaves():
            if int(label.grid_info()["row"]) > 7:
                label.grid_forget()

def msgbox(msg,titlebar):
    result=messagebox.askokcancel(title=titlebar,message=msg)
    return result

def save():
    r=msgbox("Save Record?","Record")
    if r==True:
        newid = mycol.count_documents({})
        if newid != 0:
            newid = mycol.find_one(sort=[("subid",-1)])["subid"]
        id = newid+1
        sbid.set(id)
        mydict = {"subid": int(subid.get()), "subcode": subcode.get(), "subdes":subdes.get(), "subunit":int(subunit.get()), "subsched":subsched.get()}
        x = mycol.insert_one(mydict)

        creategrid(1)
        creategrid(0)

def delete():
    r = msgbox("Delete?","Record")
    if r==True:
        myquery = {"subid": int(subid.get())}
        mycol.delete_one(myquery)
        
        creategrid(1)
        creategrid(0)

def update():
    r = msgbox("Update?","Record")
    if r==True:
        myquery = {"subid": int(subid.get())}
        
        newvalues = {"$set":{"subcode":subcode.get()}}
        mycol.update_one(myquery, newvalues)

        newvalues = {"$set":{"subdes":subdes.get()}}
        mycol.update_one(myquery, newvalues)

        newvalues = {"$set":{"subunit":int(subunit.get())}}
        mycol.update_one(myquery, newvalues)

        newvalues = {"$set":{"subsched":subsched.get()}}
        mycol.update_one(myquery, newvalues)

        creategrid(1)
        creategrid(0)

def teachersform():
   call(["python", "teachers.py"])
def subjectsform():
   call(["python", "subjects.py"])




label = tk.Label(window, text="Subjects Form", width = 30, height =1, bg="yellow", anchor="center")
label.config(font=("Courier",10))
label.grid(column=2,row=1)

label = tk.Label(window, text="Subject ID", width = 15, height =1, bg="yellow")
label.grid(column=1,row=2)
sbid = tk.StringVar()
subid = tk.Entry(window, textvariable=sbid) 
subid.grid(column=2,row=2)
subid.configure(state=tk.DISABLED)


label = tk.Label(window, text="Subject Code", width = 15, height =1, bg="yellow")
label.grid(column=1,row=3)
scode = tk.StringVar()
subcode = tk.Entry(window, textvariable=scode) 
subcode.grid(column=2,row=3)

label = tk.Label(window, text="Subject Des", width = 15, height =1, bg="yellow")
label.grid(column=1,row=4)
des = tk.StringVar()
subdes = tk.Entry(window, textvariable=des) 
subdes.grid(column=2,row=4)

label = tk.Label(window, text="Unit", width = 15, height =1, bg="yellow")
label.grid(column=1,row=5)
unit = tk.StringVar()
subunit = tk.Entry(window, textvariable=unit) 
subunit.grid(column=2,row=5)

label = tk.Label(window, text="Schedule", width = 15, height =1, bg="yellow")
label.grid(column=1,row=6)
sched = tk.StringVar()
subsched = tk.Entry(window, textvariable=sched) 
subsched.grid(column=2,row=6)


creategrid(0)

savebtn = tk.Button(text="Save",command=save)
savebtn.grid(column=1, row = 7)
savebtn = tk.Button(text="Delete",command=delete)
savebtn.grid(column=2, row = 7)
savebtn = tk.Button(text="Update", command=update)
savebtn.grid(column=3, row = 7)

#filter
label = tk.Label(window, text="Filter:",  height =1, bg="yellow")
label.grid(column=4,row=4)

label = tk.Label(window, text="ID:",  height =1, bg="yellow")
label.grid(column=4,row=5)

label = tk.Label(window, text="Code Start", height =1, bg="yellow")
label.grid(column=5,row=4)

codeStart = tk.Entry(window, textvariable=cStart,width = 10) 
codeStart.grid(column=5,row=5)



idFilter = tk.Entry(window, textvariable=fid,width= 10) 
idFilter.grid(column=4,row=7)

label = tk.Label(window, text="Code End",  width = 8 ,height =1, bg="yellow")
label.grid(column=5,row=6)

codeEnd = tk.Entry(window, textvariable=cEnd,width = 10) 
codeEnd.grid(column=5,row=7)

label = tk.Label(window, text="Des Start",  width = 8 ,height =1, bg="yellow")
label.grid(column=6,row=6)

desStart = tk.Entry(window, textvariable=dsStart,width = 10) 
desStart.grid(column=6,row=7)

label = tk.Label(window, text="Unit", width = 8 ,height =1, bg="yellow")
label.grid(column=7,row=6)

unitFilter = tk.Entry(window, textvariable=uFilter,width = 10) 
unitFilter.grid(column=7,row=7)

label = tk.Label(window, text="Sched", width = 8 ,height =1, bg="yellow")
label.grid(column=8,row=6)

schedFilter = tk.Entry(window, textvariable=schd,width = 10) 
schedFilter.grid(column=8,row=7)

filterbtn = tk.Button(text="Filter", command=setFilter)
filterbtn.grid(column=9, row = 7)


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
drop.grid(column=4,row=6)









window.mainloop()
