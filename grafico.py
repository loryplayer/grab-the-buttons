import json
import getopt, sys
import base64
from pathlib import Path
from tkinter import PhotoImage

import pandas as pd
import matplotlib.pyplot as plt

try:
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]
except getopt.error as err:
    sys.exit(2)

argument_list[0] = argument_list[0].replace("--", "")
argument_list[1]=argument_list[1].replace("\n","")
if Path(argument_list[0]).is_file():
    jsfile = argument_list[0]
    with open(jsfile, "rb") as json_file:
        byte_content = json_file.read()
        encodedBytes = base64.b64decode(byte_content).decode("utf-8")
        data = (json.loads(encodedBytes))

    n_punti = 0
    data_graph_values=[]
    for y in data:
        if str(y["level"]) == argument_list[1]:
            n_punti += 1
            data_graph_values.append(y)

    axies_y=[]
    for y in data_graph_values:
        time = float(y["time"])
        time = round(time,5)
        axies_y.append(time)

    axies_x=[]
    for y in data_graph_values:
        real_time=y["real_time"].replace(" ","\n")
        axies_x.append(real_time)

    Data = {'Tempo_reale': axies_x ,'Tempo_di_completamento': axies_y}

    df = pd.DataFrame(Data, columns=['Tempo_reale', 'Tempo_di_completamento'])
    plt.figure("Grafico",figsize=(10,6.8))
    plt.gca().invert_yaxis()
    thismanager = plt.get_current_fig_manager()
    #icon = PhotoImage(file="graph_icon.png")
    #thismanager.window.tk.call('wm', 'iconphoto', thismanager.window._w, icon)
    plt.plot(df['Tempo_reale'], df['Tempo_di_completamento'], color='red', marker='o')
    plt.title('Statistica', fontsize=14)
    plt.xlabel('Tempo reale', fontsize=14)
    plt.ylabel('Tempo di completamento', fontsize=14)
    plt.grid(True)
    plt.show()
