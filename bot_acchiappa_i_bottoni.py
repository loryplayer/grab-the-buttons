import pyautogui
import time
import keyboard
from pynput.mouse import Listener

press_x, press_y = [0, 0], [0, 0]

press = 0


def on_click(x, y, button, pressed):
    global press_x, press_y, press
    if pressed and press < 2:
        press_x[press] = x
        press_y[press] = y
        press += 1
        print(str(x) + " " + str(y))
        if press == 2:
            return False


# Collect events until released
with Listener(
        on_click=on_click) as listener:
    listener.join()
corner_x_1 = press_x[0]
corner_y_1 = press_y[0]
corner_x_2 = press_x[1]
corner_y_2 = press_y[1]
width = abs(corner_x_2 - corner_x_1)
height = abs(corner_y_2 - corner_y_1)
if corner_x_1 < corner_x_2:
    corner_up_x = corner_x_1
    corner_up_y = corner_y_1
else:
    corner_up_x = corner_x_2
    corner_up_y = corner_y_2
color = (255, 219, 195)  # 255, 219, 195
count = 0
path = "ScreenShot\\"
while keyboard.is_pressed('q') == False:
    """
    print("Corner_X_1: "+str(corner_x_1)+", Corner_Y_1:"+str(corner_y_1)+"\n")
    print("Corner_X_2: " + str(corner_x_2) + ", Corner_Y_2:" + str(corner_y_2))
    print("Width: "+str(width)+", Height:"+str(height)+"\n")
    """
    screen = pyautogui.screenshot(region=(corner_up_x, corner_up_y, width, height))
    screen.save(path + str(count) + ".png")
    width, height = screen.size

    for x in range(0, width, 5):
        # print(x)
        for y in range(0, height, 5):
            # print(y)
            r,g,b=screen.getpixel((x, y))

            if b==195: #color == screen.getpixel((x, y))
                pyautogui.click(x + corner_up_x, y + corner_up_y)
                pyautogui.PAUSE = 0
                time.sleep(0.05)
                screen = pyautogui.screenshot(region=(corner_up_x, corner_up_y, width, height))
                if b==195:
                    pyautogui.click(x + corner_up_x, y + corner_up_y)
                    pyautogui.PAUSE = 0
                    time.sleep(0.05)
                    screen = pyautogui.screenshot(region=(corner_up_x, corner_up_y, width, height))
                    
                elif screen.getpixel((int(width/2), int(height/2))) == (240, 240, 240): #(240,240,240)
                    x = 0
                    y = 0
                    while screen.getpixel((int(width/2), int(height/2))) == (240, 240, 240):
                      time.sleep(0.5)
                      screen = pyautogui.screenshot(region=(corner_up_x, corner_up_y, width, height))
                screen.save(path + str(count) + "_" + str(x) + "_" + str(y) + ".png")
                break
    count += 1
