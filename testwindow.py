import pymongo
import tkinter as tk
from tkinter import messagebox
from subprocess import call
from subjects import *

def testwindow():
    window2 = tk.Toplevel()
    window2.title("Subject Form")
    window2.geometry("1500x400")
    window2.configure(bg="orange")

    savebtn = tk.Button(window2,text="Save")
    savebtn.grid(column=1, row = 8)
 
    savebtn = tk.Button(text="Delete")
    savebtn.grid(column=2, row = 8)

    savebtn = tk.Button(text="Update")
    savebtn.grid(column=3, row = 8)
 

    window2.mainloop()