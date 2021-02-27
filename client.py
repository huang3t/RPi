import socketio
from utils.utility import uploadImg
from utils.analysis import analysis
from hardware.controller import Controller
import subprocess
import time
import threading

print("Start Running Client ...")
controller = Controller()
# standard Python
sio = socketio.Client()
host = "https://smartsmokedetection.herokuapp.com/"
# host = "http://localhost:5000"
# host = "https://c6d8171fbc15.ngrok.io"
sio.connect(host)


@sio.event
def connect():
    print("Socket connected to server at " + host)


@sio.event
def connect_error():
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


@sio.on("watch")
def watch():
    # Get smoke status and call pi camera
    print("Watching ...")
    # Call MQ2
    data = eval(readLastLog())
    # Call pi camera
    path = controller.get_picture()
    link = uploadImg(path)
    data["link"] = link
    data["analysis_link"] = uploadImg(analysis(20))
    print("Watched !")
    return data


@sio.on("close_door")
def close_alert():
    # Close the door
    print("close_door")
    controller.servo_close()
    controller.LED_off()
    return {"OK": True}


@sio.on("close_alert")
def close_alert():
    # Close the alert
    controller.buzzer_off()
    print("close_alert")


@sio.on("test")
def test():
    # Open door, led and watch
    print("Start testing ...")
    # controller.servo_open()
    # controller.LED_on()
    # controller.buzzer_on()
    # SendFireMsg
    data = eval(readLastLog())
    sendFireMsg(data)
    data["OK"] = True
    return data



def sendMsg(msg):  # Send Msg
    sio.emit("msg", msg)



def sendFireMsg(data):
    print("Sending Fire Msg")
    controller.buzzer_on()
    controller.LED_on()
    controller.servo_open()
    path = controller.get_picture()
    print(path)
    link = uploadImg(path)
    data["link"] = link
    sio.emit("fire", data)

def readLog():
    f = open("result.log", "r")
    while 1:
        where = f.tell()
        lines = f.readlines()
        lastTen = lines[-10:]
        for d in lastTen:
            if not d:
                continue
            data = eval(d[:-1])
            if data["CO"] > 88:
                sendFireMsg(data)
                break
        time.sleep(10)
        f.seek(where)


def readLastLog():
    f = open("result.log", "r")
    lines = f.readlines()
    return lines[-1][:-1]
log_thread = threading.Thread(target=readLog)
log_thread.start()
