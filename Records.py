from pathlib import Path
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import json
import getopt, sys
import base64
from subprocess import call
import sys
import os


try:
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
except getopt.error as err:
    sys.exit(2)

argument_list[0] = argument_list[0].replace("--", "")

if Path(argument_list[0]).is_file():
    jsfile = argument_list[0]
    root = Tk()
    root.title("Records " + str(jsfile).replace("_", " ").replace(".data", ""))
    main_frame = Frame(root)
    root.resizable(False, False)
    main_frame.pack(fill=BOTH, expand=1, anchor=W)

    canvas = Canvas(main_frame)
    canvas.pack(fill=BOTH, expand=1, anchor=NW)

    def on_mouse_wheel(event):
        canvas.yview_scroll(int(-1 * (event.delta // 120)), "unit")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    component_frame = Frame(canvas, relief="solid", bd=2)
    canvas.create_window((0, 0), window=component_frame, anchor=NW)


    def rtbtn():
        root.destroy()
        call('python Scelta(principale).py')


    root.geometry("500x600")
    with open(jsfile, "rb") as json_file:
        byte_content = json_file.read()
        encodedBytes = base64.b64decode(byte_content).decode("utf-8")
        data = (json.loads(encodedBytes))

    valout = ["Livello", "Tempo di esecuzione", "Tempo reale"]
    for i in range(len(data)):
        min = data[i]["level"]
        for e in range(len(data)):
            if min < data[e]["level"]:
                temp = data[i]
                min = data[e]["level"]
                data[i] = data[e]
                data[e] = temp

    storage_time = []
    for i in range(len(data)):
        levels = data[i]["level"]
        min_time_for_level = data[i]["time"]
        for e in range(len(data)):
            # print(str(levels) + " " + str(min_time_for_level)+" "+str(data[e]["level"]))
            if levels == data[e]["level"]:
                if min_time_for_level > data[e]["time"]:
                    min_time_for_level = data[e]["time"]

        if not [levels, min_time_for_level] in storage_time:
            storage_time.append([levels, min_time_for_level])

    for i in range(len(data)):
        levels = data[i]["level"]
        for e in range(len(data)):
            if levels == data[e]["level"]:
                if data[i]["time"] < data[e]["time"]:
                    temp = data[i]
                    data[i] = data[e]
                    data[e] = temp

    #   min=max
    #   for index, x in enumerate(data):
    #       if x["level"] < min:
    #           min = x["level"]
    #           #data[index+1]=data[index]

    st = []
    indextime = 0
    for indexx, x in enumerate(data):
        for indexy, y in enumerate(x):
            if valout[indexy] != valout[1]:

                st.append(valout[indexy] + ": " + str(x[y]) + "\n")
            else:
                sec_of_the_level = int(x[y])
                min_of_the_level = 0
                while sec_of_the_level > 60:
                    min_of_the_level += 1
                    sec_of_the_level -= 60
                sttime = valout[indexy] + ": " + str(min_of_the_level) + " : " + str(sec_of_the_level) + str(
                    str(x[y])[str(x[y]).find("."):str(x[y]).find(".") + 3]) + "s" + "\n"
                # print(str(storage_time[indexx][1]) in str(x[y]))
                try:
                    if str(x[y]) in str(storage_time[indextime][1]):
                        storage_time[indextime][1] = sttime
                        indextime += 1
                    st.append(sttime)
                except:
                    pass

        st.append("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")


    def click(level):
        level = level.replace(valout[0] + ": ", "")
        call('python grafico.py --' + jsfile + ' ' + level)


    icon = PhotoImage(file="graph_icon.png")
    for y, text in enumerate(st):
        if valout[0] in text:
            label = Label(component_frame, text="\n" + text, width=45, height=1)
            label.config(font=('calibri', 16, 'bold'))
            label.grid(row=y, column=0, pady=10, padx=0)
            # label.place(x=10,y=y*50)
        elif valout[1] in text:
            if st[y - 1] != st[y - 5]:
                btn = Button(component_frame, image=icon)
                btn.grid(row=y - 1, column=0, pady=20, padx=50, sticky=NW)
                btn["command"] = lambda level=st[y - 1]: click(level)
                # btn.place(x=310, y=((y-1) * 50)+2, width=50)
                label = Label(component_frame, text="\n" + text, bg="yellow", anchor=CENTER, fg="blue", height=1,
                              width=40, justify=CENTER)
                label.config(font=('calibri', 19, 'italic'))
                label.grid(row=y, column=0, pady=10, padx=0)
                # label.place(y=y * 50,height=40)
            else:
                label = Label(component_frame, text="\n" + text, width=45, height=1)
                label.config(font=('calibri', 16, 'bold'))
                label.grid(row=y, column=0, pady=10, padx=0)
                # label.place(x=10,y=y * 50)
        elif valout[2] in text:
            label = Label(component_frame, text="\n" + text, width=45, height=1)
            label.config(font=('calibri', 16, 'bold'))
            label.grid(row=y, column=0, pady=10, padx=0)
            # label.place(x=10,y=y*50)
        else:
            label = Label(component_frame, text="\n" + text, width=45, height=1)
            label.config(font=('calibri', 16, 'bold'))
            label.grid(row=y, column=0, pady=10, padx=0)

    # print(storage_time)
    indextime = 0

    for x in range(len(st)):
        if indextime < len(storage_time):
            if storage_time[indextime][1] in st[x]:
                if str(storage_time[indextime][0]) in st[x - 1]:
                    # f = open("read.txt", "a")
                    # f.write(st[x-1]+"\n"+str(x)+"\n")
                    # f.close()
                    #

                    indextime += 1


    def delbtn():

        os.remove(jsfile)
        rtbtn()


    button_frame = Label(main_frame, relief="solid", bd=2, height=5)
    returnbtn = Button(button_frame, text="Ritorna", width=6, command=rtbtn)
    returnbtn.place(relx=0.2, rely=0.5, anchor=CENTER)
    returnbtn.configure(font=('calibri', 16, 'bold'), borderwidth='2')

    delbtn = Button(button_frame, text="Elimina i record", width=16, command=delbtn)
    delbtn.place(relx=0.7, rely=0.5, anchor=CENTER)
    delbtn.configure(font=('calibri', 16, 'bold'), borderwidth='2')
    button_frame.place(relx=0.5, rely=0.9, anchor=CENTER, width=450)
    root.mainloop()
