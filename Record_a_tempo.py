try:
    from tkinter import *
    import tkinter
    import random
    import time
    import json
    from pathlib import Path
    import os
    import base64
    from subprocess import call

    root = Tk()
    root.title("Record a tempo")
    root.geometry("600x800+100+10")

    root.resizable(False, True)
    frame = Frame(root)
    dangerous_bg = "deepskyblue"
    dangerous = "blue"
    active_bg = "#fe4b03"
    active = "red"
    default_color_bg = "gainsboro"
    default_color = "white"

    count = 0
    score = 0
    lastcount = 0
    infoframe = Frame(root, height=90)
    scorelabel = Label(infoframe, relief=RAISED, width=35, anchor="center",
                       text='Il tuo punteggio ' + chr(233) + ' di ' + str(count))
    axsieslabel = Label(infoframe, relief=RAISED, width=35, anchor="center")
    lives = [3, 3]
    liveslabel = Label(infoframe, relief=RAISED, width=35, anchor="center")
    endlabel = Frame(root)
    resetlabel = Label(endlabel, relief=RAISED, width=15, anchor="center", text="Hai perso")
    timelabel = Label(infoframe, relief=RAISED, width=35, anchor="center")
    levellabel = Label(infoframe, relief=RAISED, width=35, anchor="center")


    def restart():
        global count, lastcount, lives, frame, swap, liveslabel, endlabel, resetlabel, retrybtn, score, stop, start_time, minu, sec, levels, end
        end = False
        scorelabel.config(text='Il tuo punteggio ' + chr(233) + ' di ' + str(count))
        frame.destroy()
        frame = Frame(root)
        endlabel = Frame(root)
        resetlabel = Label(endlabel, relief=RAISED, width=15, anchor="center", text="Hai perso")
        retrybtn = Button(endlabel, text='Riprova', command=restart, relief=RAISED, width=15, anchor="center")
        count = 0
        score = 0
        lastcount = 0
        lives[0] = 3
        swap = False
        stop = False
        minu = 0
        sec = 0
        levels = 0
        start_time = time.time()
        main(1, 1)


    retrybtn = Button(endlabel, text='Riprova', command=restart, relief=RAISED, width=15, anchor="center")
    swap = False
    levels = 0
    minu = 0
    sec = 0
    end = False
    btnpressed = 0
    level_of_time_start=0
    return_game = False


    def main(height=5, width=5):
        global stop, minu, sec, start_time, levels, btnpressed, end, elapsed_time, return_game,level_of_time_start
        if not end:
            elapsed_time[0] = int(time.time() - start_time)
            elapsed_time[1] = (time.time() - start_time)

            if elapsed_time[0] - (minu * 60) >= 60:
                minu += 1

            else:
                sec = elapsed_time[0] - (minu * 60)
            if sec<10:
                sec="0"+str(sec)

            texttime = "Tempo trascorso: " + str(minu) + " : " + str(sec)
            timelabel.config(text=texttime)
            livestext = 'Vita : ' + str(lives[0]) + "/" + str(lives[1])
            liveslabel.config(text=livestext)
            if btnpressed >= 100:
                lives[0] += 1
                lives[1] += 1
                btnpressed = 0
            #print(str(level_of_time_start) + " " + str(time.time()))
            if not stop:
                stop = True
                levels += 1
                level_of_time_start = time.time()
                count_for_dangerous_buttons = 0
                axiestext = "Assi y: " + str(height) + "\n" + "Assi x: " + str(width)
                axsieslabel.config(text=axiestext)
                levelstext = "Livello: " + str(levels)
                levellabel.config(text=levelstext)

                def click(button):
                    global count, lastcount, swap, lives, score, stop, btnpressed, end
                    if not end:
                        if button["bg"] == active:
                            button["bg"] = default_color
                            button["activebackground"] = default_color_bg
                            count = count - 1
                            score = score - 1
                        elif button["bg"] != dangerous:
                            button["bg"] = active
                            button["activebackground"] = active_bg
                            btnpressed += 1
                            count = count + 1
                            score = score + 1
                        else:
                            score = score - 15
                            lives[0] = lives[0] - 1
                            btnpressed = 0

                        textpunteggio = 'Il tuo punteggio ' + chr(233) + ' di ' + str(score)
                        scorelabel.config(text=textpunteggio)
                        print("Count: "+str(count)+", Height: "+str(height)+", Width: "+str(width)+", Lastcount: "+str(lastcount)+", Count for dangerous buttons: "+str(count_for_dangerous_buttons))
                        if count == ((height * width) + lastcount) - count_for_dangerous_buttons:
                            time_of_the_level = time.time() - level_of_time_start
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
                            #print(str(level_of_time_start) + " " + str(time.time()) + " " + str(time_of_the_level))
                            data.append({
                                "level": levels,
                                "time": time_of_the_level,
                                "real_time": time.strftime('%X %d/%m/%Y')
                            })

                            with open(js_record_file, "wb") as outfile:
                                outfile.write(base64.b64encode(json.dumps(data).encode("utf-8")))
                            lastcount = count
                            stop = False
                            if swap:
                                swap = False
                                main(height + 1, width)
                            else:
                                swap = True
                                main(height, width + 1)
                            outfile.close()
                        if lives[0] <= 0 or score < 0:
                            end = True
                            resetlabel.configure(font=('calibri', 36, 'bold'), borderwidth='2')
                            retrybtn.configure(font=('calibri', 36, 'bold'), borderwidth='2')
                            resetlabel.grid(row=1, column=1)
                            retrybtn.grid(row=2, column=1)
                            endlabel.place(relx=0.5, rely=0.35, anchor=CENTER)

                for x in range(width):
                    for y in range(height):
                        btn = tkinter.Button(frame, bg=default_color)
                        btn.grid(column=x, row=y, sticky=N + S + E + W)
                        btn["command"] = lambda bt=btn: click(bt)
                        btn["activebackground"] = default_color_bg
                        if count >= 1:
                            getrandomindex = random.randint(0, 2)
                            if getrandomindex == 0 and count_for_dangerous_buttons < count:
                                btn["bg"] = dangerous
                                btn["activebackground"] = dangerous_bg
                                count_for_dangerous_buttons += 1
                for x in range(width):
                    Grid.columnconfigure(frame, x, weight=1)

                for y in range(height):
                    Grid.rowconfigure(frame, y, weight=1)
                frame.place(relx=0.5, rely=0.28, anchor=CENTER, height=400, width=400)




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
    elapsed_time = [0, 0]

    try:
        while True:
           # if keyboard.is_pressed("Esc") and not end:
           #     end = True
           #     print("pausa")
           #     time.sleep(0.5)
           # elif keyboard.is_pressed("Esc") and end:
           #     print("riprendi")
           #     start_time = time.time() - elapsed_time[1]
           #     #time_of_the_level = time.time() - level_of_time_start
           #     print("start #1 "+str(level_of_time_start)+" time "+str(time.time()))
           #     level_of_time_start=time.time()+(time.time()-level_of_time_start)
           #     print("start #2 " + str(level_of_time_start) + " time " + str(time.time()))
           #     end = False
           #     time.sleep(0.5)
            time.sleep(0.05)
            main(1, 1)
            root.update_idletasks()
            root.update()
    except:
        pass
except:
    call("")