from sqlite3 import threadsafety
import string
from plyer import notification
import tkinter as tk
import socket
import time
from datetime import datetime
from threading import Thread

root = tk.Tk()
root.configure(background='black')
root.overrideredirect(True)

titleBar = tk.Label(
    root,
    text='INTERNET CHECKER',
    fg="white",
    bg="black")
titleBar.grid(row=0, column=0)
tk.Label(
    root,
    text='Internet Status:',
    fg="white",
    bg="black").grid(row=1, column=0)
tk.Label(
    root,
    text='Start Time:',
    fg="white",
    bg="black").grid(row=4, column=0)
tk.Label(
    root,
    text='Last Disconnect:',
    fg="white",
    bg="black").grid(row=5, column=0)
tk.Label(
    root,
    text='Total Disconnect:',
    fg="white",
    bg="black"). grid(row=6, column=0)

beginText = "Start App to begin"
status = tk.StringVar()
startTime = tk.StringVar()
lastDisconnect = tk.StringVar()
totalDisconnect = tk.StringVar()
startTime.set(beginText)
lastDisconnect.set(beginText)
totalDisconnect.set(beginText)
status.set("")

statusLabel = tk.Label(
    root,
    textvariable=status,
    fg="white",
    bg="black").grid(row=1, column=1)
startLabel = tk.Label(
    root,
    textvariable=startTime,
    fg="white",
    bg="black").grid(row=4, column=1)
lastDisconnectLabel = tk.Label(
    root,
    textvariable=lastDisconnect,
    fg="white",
    bg="black").grid(row=5, column=1)
totalDisconnectLabel = tk.Label(
    root,
    textvariable=totalDisconnect,
    fg="white",
    bg="black"). grid(row=6, column=1)

internetCheck = False
totalDisconnectNumber = 0
threadWorking = False


def have_internet(host="8.8.8.8", port=53, timeout=3):
    global internetCheck
    global totalDisconnectNumber
    global threadWorking
    INTERNET_DISCONNECTED = False
    while internetCheck:
        time.sleep(21)
        if internetCheck == False:
            break
        now = datetime.now()
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(
                (host, port))
            status.set("Active-" + now.strftime("%H:%M:%S"))
            if INTERNET_DISCONNECTED == True:
                INTERNET_DISCONNECTED = False
                notification.notify(
                    title="Internet Connection",
                    message="Internet Connected!",
                    app_name="Internet Checker App",
                    ticker="Internet Checker",
                    timeout=10
                )
        except socket.error:
            if INTERNET_DISCONNECTED == False:
                INTERNET_DISCONNECTED = True
                totalDisconnectNumber += 1
                lastDisconnect.set(now.strftime("%H:%M:%S"))
                totalDisconnect.set(str(totalDisconnectNumber))
                status.set("Passive-" + now.strftime("%H:%M:%S"))
                notification.notify(
                    title="Internet Connection",
                    message="Internet Disconnected!",
                    app_name="Internet Checker App",
                    ticker="Internet Checker",
                    timeout=10
                )
    threadWorking = False


def stp():
    global internetCheck
    internetCheck = False
    startTime.set("App paused")
    status.set("-")


def strt():
    global internetCheck
    global totalDisconnectNumber
    global threadWorking
    if internetCheck == False and threadWorking == False:
        internetCheck = True
        now = datetime.now()
        startTime.set(now.strftime("%H:%M:%S"))
        lastDisconnect.set("No disconnect detected")
        totalDisconnect.set("0")
        status.set("Initializing")
        totalDisconnectNumber = 0
        threadWorking = True
        worker = Thread(target=have_internet, args=())
        worker.setDaemon(True)
        worker.start()
    else:
        print("Program already working!! ")


startButton = tk.Button(root, text='START ',
                        command=strt, bg="#2e2e2e", fg='white')
startButton.grid(row=8, column=0)
stopButton = tk.Button(root, text='STOP ', command=stp,
                       bg="#2e2e2e", fg='white')
stopButton.grid(row=8, column=1)
closeButton = tk.Button(root, text='X', command=root.destroy, bg="#2e2e2e", padx=2,
                        pady=2, activebackground='red', bd=0, font="bold", fg='white', highlightthickness=0)
closeButton.grid(row=0, column=3)


def change_on_hover(button, color_on_hover, color_on_leave):
    button.bind("<Enter>", func=lambda e: button.config(
        background=color_on_hover))
    button.bind("<Leave>", func=lambda e: button.config(
        background=color_on_leave))


def move_window(event):
    root.geometry('+{0}+{1}'.format(event.x_root, event.y_root))


def change_on_hovering(button):
    button['bg'] = 'red'


def return_to_normalstate(button):
    button['bg'] = '#2e2e2e'


root.bind('<B1-Motion>', move_window)
change_on_hover(startButton, 'green', 'grey')
change_on_hover(stopButton, 'red', 'grey')
change_on_hover(closeButton, 'red', '#2e2e2e')


root.mainloop()
