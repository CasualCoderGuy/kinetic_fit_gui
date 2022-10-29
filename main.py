from fileinput import filename
import os
from tkinter import *
from tkinter import ttk
import tkinter.filedialog as fd

from datetime import datetime, timezone
from tkinter.tix import FileSelectBox

from kinfit_lm import fit_data

filesToFit = []

def Fit(event):    
    fitStart = 0.0
    fitEnd = 0.0
    xCorrect = 0.0
    kval = 0.0
    Aval = 0.0
    AinfVal = 0.0
    kfix = True
    Afix = True
    AinfFix = True
    equation = ""
    weights = ""
    skipNeg = False
    try:
        if kvalTK.get() != "":
            kval = float(kvalTK.get())
        if AvalTK.get() != "":
            Aval = float(AvalTK.get())
        if AinfValTK.get() != "":
            AinfVal = float(AinfValTK.get())
        if fitStartTK.get() != "":
            fitStart = float(fitStartTK.get())
        if fitEndTK.get() != "":
            fitEnd = float(fitEndTK.get())
        if xCorrectTK.get() != "":
            xCorrect = float(xCorrectTK.get())
        #kfix = kfixTK.get()
        #Afix = AfixTK.get()
        #AinfFix = AinfFixTK.get()
        #skipNeg = skipNegTK.get()
    except ValueError:
        return
    fitWindow.destroy()
    print("fitting")
    print(kfix)
    fit_data(filesToFit[0], fitStart, fitEnd, xCorrect, kval, Aval, AinfVal, kfix, Afix, AinfFix, skipNeg)
    #open result win
    filesToFit.pop(0)

def openResultWindow():
    resultWindow = Toplevel(root)
    resultWindow.title("Fit Results")
    filename = filesToFit[0]
    ttk.Label(resultWindow, text=filename).grid(column=1, row=1, columnspan = 3, sticky=W)
    ttk.Label(resultWindow, text="Fit Results").grid(column=1, row=2, sticky=W)

def openFitWindow():
    global fitWindow
    if len(filesToFit) < 1:
        return
    fitWindow = Toplevel(root)
    fitWindow.title("Fit Settings")
    floatValid2 = fitWindow.register(validateFloat)
    filename = filesToFit[0]
    ttk.Label(fitWindow, text=filename).grid(column=1, row=1, columnspan = 3, sticky=W)
    ttk.Label(fitWindow, text="Fit Settings").grid(column=1, row=2, sticky=W)
    ttk.Label(fitWindow, text="Fit start").grid(column=1, row=3, sticky=W)
    ttk.Label(fitWindow, text="Fit end").grid(column=1, row=4, sticky=W)
    ttk.Label(fitWindow, text="Correct X").grid(column=1, row=5, sticky=W)
    ttk.Label(fitWindow, text="k").grid(column=1, row=6, sticky=W)
    ttk.Label(fitWindow, text="A0").grid(column=1, row=7, sticky=W)
    ttk.Label(fitWindow, text="Ainf").grid(column=1, row=8, sticky=W)
    ttk.Label(fitWindow, text="Weights").grid(column=1, row=9, sticky=W)

    #autofill default
    entry1 = ttk.Entry(fitWindow, textvariable=fitStartTK, validate='all', validatecommand=(floatValid2,'%P'))
    entry1.grid(column=2, row=3, sticky=W)
    entry2 = ttk.Entry(fitWindow, textvariable=fitEndTK, validate='all', validatecommand=(floatValid2,'%P'))
    entry2.grid(column=2, row=4, sticky=W)
    entry6 = ttk.Entry(fitWindow, textvariable=xCorrectTK, validate='all', validatecommand=(floatValid2,'%P'))
    entry6.grid(column=2, row=5, sticky=W)
    entry3 = ttk.Entry(fitWindow, textvariable=kvalTK, validate='all', validatecommand=(floatValid2,'%P'))
    entry3.grid(column=2, row=6, sticky=W)
    entry4 = ttk.Entry(fitWindow, textvariable=AvalTK, validate='all', validatecommand=(floatValid2,'%P'))
    entry4.grid(column=2, row=7, sticky=W)
    entry5 = ttk.Entry(fitWindow, textvariable=AinfValTK, validate='all', validatecommand=(floatValid2,'%P'))
    entry5.grid(column=2, row=8, sticky=W)
    entry7 = ttk.Entry(fitWindow, textvariable=weightsTK)
    entry7.grid(column=2, row=9, sticky=W)
    fitBtn = ttk.Button(fitWindow, text="Fit", command=lambda:Fit(None))
    fitBtn.grid(column=2, row=11, sticky=N)
    fitWindow.bind('<Escape>', lambda x:fitWindow.destroy()) #!! handle remaining fit


def open_file():
    filestxt = fd.askopenfilenames(parent=root, title='Choose Files to Fit',
                            filetypes= (("CSV files","*.csv"),
                            ("Text files","*.txt"),
                            ("XLS files","*.xls"),
                            ("XLSX files","*.xlsx"),
                            ("All files","*.*")))
    files = root.splitlist(filestxt)
    for file in files:
        if file not in filesToFit:
            filesToFit.append(file)
    updateList()

def updateList():
    lb1.delete(0,END)
    i = 0
    for file in filesToFit:
        lb1.insert(i, file)
        i += 1

def deleteList():
    filesToFit.clear()
    lb1.delete(0,END)

def validateFloat(entry):
	if entry == '' or entry == '.' or entry == '-':
		return True
	try:
		val = float(entry)
	except ValueError:
		return False
	return True


root = Tk()
root.title("Kinetic Fitter")

fitStartTK = StringVar()
fitEndTK = StringVar()
xCorrectTK = StringVar()
kvalTK = StringVar()
AvalTK = StringVar()
AinfValTK = StringVar()
kfixTK = BooleanVar()
AfixTK = BooleanVar()
AinfFixTK = BooleanVar()
equationTK = StringVar()
weightsTK = StringVar()
skipNegTK = BooleanVar()

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
#root.columnconfigure(0, weight=1)
#root.rowconfigure(0, weight=1)

ttk.Label(mainframe, text="Choose Files to Fit").grid(column=1, row=1, sticky=W)
# ttk.Label(mainframe, text="Source").grid(column=1, row=2, sticky=W)
# ttk.Label(mainframe, text="Destination").grid(column=2, row=2, sticky=W)
# entry1 = ttk.Entry(mainframe)
# entry1.grid(column=1, row=3, sticky=(N, W, E, S))
# entry2 = ttk.Entry(mainframe)
# entry2.grid(column=2, row=3, sticky=(N, W, E, S))
openBtn = ttk.Button(mainframe, text="Browse...", command=open_file)
openBtn.grid(column=2, row=1, sticky=W)
deleteBtn = ttk.Button(mainframe, text="Delete All", command=deleteList)
deleteBtn.grid(column=3, row=1, sticky=W)
startBtn = ttk.Button(mainframe, text="Start", command=openFitWindow)
startBtn.grid(column=4, row=1, sticky=W)


lb1 = Listbox(mainframe, font=('Arial', 8))
#lb2 = Listbox(mainframe, font=('Arial', 13))
lb1.grid(column=1, row=3, columnspan=4, sticky=(N, W, E, S))
#lb2.grid(column=2, row=2, sticky=(N, W, E, S))

# ttk.Label(mainframe, text="File Differences").grid(column=1, row=5, sticky=W)
# canvas = Canvas(mainframe, width=740)
# canvas.grid(column=1, row=6, columnspan=2, sticky=(N, W, S))
# canvas.configure(bg='white')

# dirtest1 = "F://Coding//dirsync-develop//dirsync-develop//dirsync"
# dirtest2 = "F://Coding//dirsync-develop//dirsync-develop//tests"

#lb1.configure(yscrollcommand=scrolly.set,)
#lb2.configure(yscrollcommand=scrolly.set)

# ttk.Label(mainframe, text="Logs").grid(column=1, row=7, sticky=W)
# textbox = Text(mainframe, width=40, height=10)
# textbox.grid(column=1, row=8, columnspan=2, sticky=(W, E))


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.bind("<Return>", openFitWindow)
floatValid = root.register(validateFloat) # register

root.mainloop()