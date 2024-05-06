import socket
import netifaces as ni
from tkinter import *
from tkinter import ttk
from Drone import Drone
from threading import Thread
from queue import Queue
from pynput.keyboard import Key, Listener
import time
#pip3 install "requests>=2.*"
#pip3 install netifaces

UDP_IP = "10.232.88.99" #this needs to be the current IP of this computer. Can we grab it at runtime?

#BRENDAN CODE _____________________________________________________________________________________________________
yaw = 0
keyQ = False
keyE = False
roll = 0 
keyA = False
keyD = False
pitch = 0
keyW = False
keyS = False
throttle = 0
keyAU = False
keyAD = False
shouldQuit = False
#BRENDAN CODE _____________________________________________________________________________________________________

try:
    hostname = socket.gethostname()
    print(hostname)
    print("00000")
    # ipv4_address = socket.gethostbyname(hostname + ".local")
    # print(f"Internal IPv4 Address for {hostname}: {ipv4_address}")
    # 
    ip = ni.ifaddresses('en1')[ni.AF_INET][0]['addr']
    UDP_IP = ip
    print(ip)
except socket.gaierror as e:
    print("There was an error resolving the hostname.")
    print(e)
except Exception as e:
    print(f"An unexpected error occurred: {e}")

qFromComms = Queue()
qToComms = Queue()
sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

terminate = False
maxDrones = 3
drones = []
#these next two lines are for testing only. Remove them
drones.append(Drone(0, "one", "10.20.18.23", 85))
drones.append(Drone(1, "two", "10.20.18.23", 85))


UDP_PORT = 5005

root = Tk()
root.geometry("400x400")

frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="hello world").grid(column = 0, row = 0)
ttk.Label(frm, text="Drones List").grid(column = 0, row = 1)

listVar = StringVar(value = drones)
droneList = Listbox(master = root,width =100, height = 100, listvariable = listVar)

droneList.grid(column = 0, row = 2)




def handshake(msg, addr):
    
    parts = msg.split("|")
    i = int(parts[1])
   
    if (i == -1):
        i = len(drones)
        print(i)
        print(addr)
        print(addr[1])
        drone =  Drone(i, parts[2], addr[0], addr[1])
        drones.append(drone)
        for adrone in drones:
            print(adrone)
        updateList()
        sendMessage(drone.ipAddress, drone.port, "HSC|" + str(i))

    else:
        if drones[i].name == parts[2]:
            #we could update here
            drones[i].ipAddress = addr[0]
            drones[i].port = addr[1]
    droneList.update()    
def sendMessage(ipAddress, port, msg):
    print("sendMessage")
    print(ipAddress)
    print(port)
    print(msg)
    print("----------------------------")    
    bMsg = msg.encode("ascii")
    sendSocket.sendto(bMsg, (ipAddress, int(port)))
    print("sent message")
def manualControl():


def updateList():
    #clear the list box
    droneList.delete(0, len(drones)-1)

    #walk through drones
    for i in range(len(drones)):
        droneList.insert(i, str(drones[i]))
    #insert all the drone elements


def listDrones():
    global drones
    for drone in drones:
        print(drone.name, drone.ipAddress, drone.port, "\t") 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind((UDP_IP, UDP_PORT))

print("Ready3")
def listen(q_out, q_in):#happens on a separate thread
    
    while True:
        #check if we need to stop--grab from q_in  
        data = b""    #the b prefix makes it byte data
        if (not q_in.empty()):
            qIn = q_in.get()
            if (qIn == "TERMINATE"):
                q_out.put("STOPPING")
                break
        try:
            data, addr = sock.recvfrom(1024)
        except:
            continue
        strData = data.decode("utf-8")
        print("Received message %s" % data)
        strData = strData + "|" + addr[0] + "|" + str(addr[1])#the message, the ip, the port
        strData = addr[0] + "*" + str(addr[1]) + "*" + strData#the ip, the port, the message
        q_out.put(strData) #this sends the message to the main thread
        # parts = strData.split("|")
        # print(parts)
        # cmd = parts[0]

        # if cmd == "HND":
        #     #HANDSHAKE
        #     handshake(parts, addr)
    print("goodbye")
def addDrone():
    #this is just to test if tkinter will add them to the listbox on a button press.
    drones.append(Drone(8, "test", "none", 17))
    print(str(drones))
def checkQueue(q_in):
    if (not q_in.empty()):
        print("checking queue")
        #grab the item
        #process the info
        #mark it complete
        data = q_in.get()
        parts = data.split("*")
        addr = parts[0]
        port = int(parts[1])
        msg = parts[2]
        # print(parts)
        msgParts = msg.split("|")

        cmd = msgParts[0]

        if cmd == "HND":
            #HANDSHAKE
            handshake(msg, (addr, port))
    root.after(1000, checkQueue, q_in)

t = Thread(target=listen, args=(qFromComms, qToComms))
t.start()
root.after(1000, checkQueue, qFromComms)
# root.bind("<<updateevent>>", updateDronesList)
root.mainloop()
qToComms.put("TERMINATE") #tell the subloop on the backup thread to quit.
t = qFromComms.get(timeout=3.0)
#give it a chance to quit
print("all done")
exit(0)
