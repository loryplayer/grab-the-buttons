from tkinter import *
import os
from subprocess import call
import tkinter



root = Tk()
root.title("Scelta")
root.geometry("500x300")
root.resizable(False,False)
Domanda = Label(root, text="Scegli la modalità di gioco", height=55, width=50)
Domanda.place(relx=0.5, rely=0.15, anchor=CENTER)
Domanda.configure(font=('calibri', 20, 'bold'), borderwidth='3')
gamemods = ["Acchiappa i bottoni", "Sfida a tempo", "Record a tempo"]
files = [os.listdir(),os.listdir()]
files_to_remove = []
index = 0
for file in files[0]:
    if not ".py" in file or "Records" in file or "Scelta" in file:
        files_to_remove.append(file)


for file_to_remove in files_to_remove:
    files[0].remove(file_to_remove)

def rungame(pyfile):
    root.destroy()
    call('python ' + pyfile)


def runrecords(file):
    root.destroy()
    jsfile = file.replace("py", "data")
    call('python Records.py --' + jsfile)
arbtn=[0,0,0]
for x in range(len(gamemods)):
    pyfile = ""
    for file in files[0]:
        if gamemods[x][0:gamemods[x].find(" ")] in file:
            pyfile = file

    if pyfile != "":

        btn = Button(Domanda, text=gamemods[x], width=20, command=lambda name=pyfile: rungame(name))
        btn.configure(font=('calibri', 16, 'bold'), borderwidth='2')
        btn.place(relx=0.42, rely=0.53 + (0.03 * x), anchor=CENTER)
       # print(pyfile)
        if os.path.exists(pyfile.replace("py","data")):

            arbtn[x]=tkinter.Button(Domanda, text="Records", width=6,command=lambda name=pyfile: runrecords(name))
            #print(pyfile)
            arbtn[x].configure(font=('calibri', 16, 'bold'), borderwidth='2')
            arbtn[x].place(relx=0.7, rely=0.53 + (0.03 * x), anchor=CENTER)





root.mainloop()
