from tkinter import *
import tkinter
import random
import time
import json
from pathlib import Path
import os
import base64
from subprocess import call
from base64 import b64encode

root = Tk()
root.title("Acchiappa i bottoni")
root.geometry("600x800+100+10")

root.resizable(False, True)
frame = Frame(root)
dangerous_bg = "deepskyblue"
dangerous = "blue"
active_bg = "#fe4b03"
active = "red"
default_color_bg = "gainsboro"
default_color = "white"
deactive_bg = "gray"

count = 0
score = 0

infoframe = Frame(root, height=90)
scorelabel = Label(infoframe, relief=RAISED, width=35, anchor="center",
                   text='Il tuo punteggio ' + chr(233) + ' di ' + str(count))
axsieslabel = Label(infoframe, relief=RAISED, width=35, anchor="center")
lives = [5, 5]
liveslabel = Label(infoframe, relief=RAISED, width=35, anchor="center")
endlabel = Frame(root)
resetlabel = Label(endlabel, relief=RAISED, width=15, anchor="center", text="Hai perso")
timelabel = Label(infoframe, relief=RAISED, width=35, anchor="center")
levellabel = Label(infoframe, relief=RAISED, width=35, anchor="center")


def restart():
    global count, lastcount, lives, frame, swap, liveslabel, endlabel, resetlabel, retrybtn, score, stop, start_time, minu, sec, levels,end
    end=False
    scorelabel.config(text='Il tuo punteggio ' + chr(233) + ' di ' + str(count))
    frame.destroy()
    frame = Frame(root)
    count = 0
    score = 1
    lastcount = 1
    lives[0] = 5
    lives[1] = 5
    swap = False
    stop = False
    minu = 0
    sec = 0
    levels = 0
    start_time = time.time()
    main(2, 2)


def change(x, y):
    global frame, stop, count, resetlabel, retrybtn
    frame.destroy()
    frame = Frame(root)
    stop = False
    #print(str(x) + " " + str(y))
    main(x, y)

end=False
retrybtn = Button(endlabel, text='Riprova', command=restart, relief=RAISED, width=15, anchor="center")
swap = False
levels = 1
minu = 0
sec = 0
stopchange = False
btnpressed = 0
start_change_time = 0
levels_for_increment = 10
score_for_increment_lives=10
time_increment = 0
time_passed = 0
lastgrid = 4
lastcount = 1


def main(height=5, width=5):
    global stop, minu, sec, start_time, levels, btnpressed, stopchange, start_change_time, _x, _y, count, \
        lastgrid, count_for_dangerous_buttons, lastcount, levels_for_increment, time_increment,end
    elapsed_time = int(time.time() - start_time)
    if not end:
        if elapsed_time - (minu * 60) >= 60:
            minu += 1

        else:
            sec = elapsed_time - (minu * 60)
        if sec < 10:
            sec = "0" + str(sec)

        texttime = "Tempo trascorso: " + str(minu) + " : " + str(sec)
        timelabel.config(text=texttime)
        livestext = 'Vita : ' + str(lives[0]) + "/" + str(lives[1])
        liveslabel.config(text=livestext)
        if btnpressed >= 150:
            lives[0] += 1
            lives[1] += 1
            btnpressed = 0
        # print(str(height) + " " + str(width))
        levelstext = "Livello: " + str(levels)
        levellabel.config(text=levelstext)
        if not stop:
            start_change_time = time.time()
            level_time_start = time.time()
            stop = True
            count = 0

            axiestext = "Assi y: " + str(height) + "\n" + "Assi x: " + str(width)
            _x = height
            _y = width
            axsieslabel.config(text=axiestext)




            def click(button):
                global lastcount, swap, lives, score, stop, btnpressed, levels, count, count_for_dangerous_buttons,end,score_for_increment_lives
                if not end:
                    if button["bg"] == dangerous:
                        button["bg"] = default_color
                        button["activebackground"] = default_color_bg
                        count = count + 1
                        score = score + 1
                        if score >= score_for_increment_lives:
                            lives[0]+=1
                            lives[1]+=1
                            score_for_increment_lives*=2
                        btnpressed += 1
                    elif button["bg"] != dangerous:
                        lives[0] -= 1

                    textpunteggio = 'Il tuo punteggio ' + chr(233) + ' di ' + str(score)
                    scorelabel.config(text=textpunteggio)
                    #print("Conteggio "+str(count) + ", Conteggio bottoni " + str(count_for_dangerous_buttons))
                    if lives[0] <= 0 or score < 0:
                        #print("mortooooo")
                        end=True
                        endlabel = Frame(root)
                        resetlabel = Label(endlabel, relief=RAISED, width=15, anchor="center", text="Hai perso")
                        retrybtn = Button(endlabel, text='Riprova', command=restart, relief=RAISED, width=15, anchor="center")
                        resetlabel.configure(font=('calibri', 36, 'bold'), borderwidth='2')
                        retrybtn.configure(font=('calibri', 36, 'bold'), borderwidth='2')
                        resetlabel.grid(row=1, column=1)
                        retrybtn.grid(row=2, column=1)
                        endlabel.place(relx=0.5, rely=0.35, anchor=CENTER)


                    if count == count_for_dangerous_buttons:
                        stop = False
                        if swap:
                            swap = False
                            main(height + 1, width)
                        else:
                            swap = True
                            main(height, width + 1)
                        time_of_the_level = time.time() - level_time_start
                        js_record_file = os.path.basename(__file__).replace("py", "data")

                        if Path(js_record_file).is_file():
                            with open(js_record_file, "rb") as json_file:
                                byte_content = json_file.read()
                                encodedBytes = base64.b64decode(byte_content).decode("utf-8")
                                data = (json.loads(encodedBytes))
                        else:
                            data = []

                        # print(str(min_of_the_level)+" : "+str(sec_of_the_level)+str(str(time_of_the_level)[str(
                        # time_of_the_level).find("."):str(time_of_the_level).find(".")+3]))
                        data.append({
                            "level": levels-1,
                            "time": time_of_the_level,
                            "real_time": time.strftime('%X %d/%m/%Y')
                        })

                        with open(js_record_file, "wb") as outfile:
                            outfile.write(base64.b64encode(json.dumps(data).encode("utf-8")))

                        outfile.close()

            index = width * height
           # print(lastgrid, lastcount, count_for_dangerous_buttons, index)
            if lastgrid != index:
                levels += 1
                index = levels
                count_for_dangerous_buttons = 0
                if levels > levels_for_increment:
                    #print("new level: "+str(levels_for_increment))
                    levels_for_increment += levels_for_increment
                    time_increment += 1.5
            else:
                index = lastcount
                count_for_dangerous_buttons = 0
            while count_for_dangerous_buttons != index:
                count_for_dangerous_buttons = 0
             #   print("start "+str(count_for_dangerous_buttons))
                for x in range(width):
                    for y in range(height):
                        btn = tkinter.Button(frame, bg=default_color)
                        btn.grid(column=x, row=y, sticky=N + S + E + W)
                        btn["command"] = lambda bt=btn: click(bt)
                        btn["activebackground"] = default_color_bg
                        if width * height >= 1:
                            # print(count)
                            if lastgrid != index:
                                getrandomindex = random.randint(0, 2)
                            else:
                                getrandomindex = random.randint(0, 1)

                            if getrandomindex == 0 and count_for_dangerous_buttons < index and btn["bg"] != dangerous:
                                btn["bg"] = dangerous
                                btn["activebackground"] = dangerous_bg
                                count_for_dangerous_buttons += 1
                                print("x: "+str(x)+", y: "+str(y))
            #    print("end "+str(count_for_dangerous_buttons))
            for x in range(width):
                Grid.columnconfigure(frame, x, weight=1)

            for y in range(height):
                Grid.rowconfigure(frame, y, weight=1)
            frame.place(relx=0.5, rely=0.28, anchor=CENTER, height=400, width=400)
        if time.time() - start_change_time > (1.5 + time_increment):
            start_change_time = time.time()
          #  print("ewqrqer " + str(count_for_dangerous_buttons) + " " + str(count))
            lastgrid = height * width
            lastcount=count_for_dangerous_buttons-count
            change(height, width)


scorelabel.configure(font=('calibri', 16, 'bold'), borderwidth='2')
scorelabel.pack()
axsieslabel.configure(font=('calibri', 16, 'bold'), borderwidth='2')
axsieslabel.pack(pady=5)
liveslabel.configure(font=('calibri', 16, 'bold'), borderwidth='2')
liveslabel.pack(pady=5)
timelabel.configure(font=('calibri', 16, 'bold'), borderwidth='2')
timelabel.pack(pady=5)
levellabel.configure(font=('calibri', 16, 'bold'), borderwidth='2')
levellabel.pack(pady=5)


def rtbtn():
    root.destroy()
    call('python Scelta(principale).py')


returnbtn = Button(infoframe, text="Ritorna", width=6, command=rtbtn)
returnbtn.pack()
returnbtn.configure(font=('calibri', 16, 'bold'), borderwidth='2')
infoframe.place(relx=0.5, rely=0.80, anchor=CENTER)
start_time = time.time()
stop = False
_x = 2
_y = 2
try:
    while True:

        time.sleep(0.05)
        main(_x, _y)
        root.update_idletasks()
        root.update()
except:
    pass
