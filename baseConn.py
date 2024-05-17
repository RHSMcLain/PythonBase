import socket
import netifaces as ni
from tkinter import *
from tkinter import ttk
import tkinter as tk
from Drone import Drone
from threading import Thread
from queue import Queue
from pynput.keyboard import Key, Listener
import time
import customtkinter
import tkinter
import tkinter.messagebox
from PIL import Image
#pip3 install "requests>=2.*"
#pip3 install netifaces
#python3 -m pip install customtkinter
#python3 -m pip install --upgrade Pillow
global UDP_IP
UDP_IP = 0
def getMyIP():
    try:
        hostname = socket.gethostname()
        print(hostname)
        print("00000")
        # ipv4_address = socket.gethostbyname(hostname + ".local")
        # print(f"Internal IPv4 Address for {hostname}: {ipv4_address}")
        # 
        ip = ni.ifaddresses('en1')[ni.AF_INET][0]['addr']
        UDP_IP = ip
        UDP_PORT = 5005
        print(ip)
    except socket.gaierror as e:
        print("There was an error resolving the hostname.")
        print(e)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

getMyIP()
ip = ni.ifaddresses('en1')[ni.AF_INET][0]['addr']
 #ask mclain how to do this on windows
UDP_IP = ip
UDP_PORT = 5005

#BRENDAN CODE _____________________________________________________________________________________________________
global yaw, roll, pitch, throttle, keyQ, keyE, keyA, keyD, keyW, keyS, keyAU, keyAD, shouldQuit
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
global manualyes
global selDrone
global selDroneTK
manualyes = False

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")




def clamp(val):
    lowLimit = -100
    highLimit = 100
    if val < lowLimit:
        val = lowLimit
    if val > highLimit:
        val = highLimit   
    return val
def introToAP():
    #tell the AP that we are the base station. 
    #AP needs to save that IP address to tell it to drones (so they can connect to the base station)
    sendMessage("192.168.4.22", 80, "BaseStationIP")
    print ("sent message to AP")
    #listen 
    while True:
    #check if we need to stop--grab from q_in  
        data = b""    #the b prefix makes it byte data
        
        try:
            data, addr = sock.recvfrom(1024)
            strData = data.decode("utf-8")
            print("Received message %s" % data)
            break
        except:
            
            continue
        
        #test the input to see if it is the confirmation code
        #if it is, we can break

def show(key):
    global yaw, roll, pitch, throttle, keyQ, keyE, keyA, keyD, keyW, keyS, keyAU, keyAD, shouldQuit
    if key == Key.up:
        print("Up")
        keyAU = True
        return
    if key == Key.down:
        keyAD = True
        return
    if key.char == 'q':
        keyQ = True
    if key.char == 'e':
        keyE = True
    if key.char == 'a':
        keyA = True
    if key.char == 'd':
        keyD = True
    if key.char == 'w':
        keyW = True
    if key.char == 's':
        keyS = True
    if key.char == 'p':
        shouldQuit = True
def release(key):
    global keyQ, keyE, keyA, keyD, keyW, keyS, keyAU, keyAD, throttle
    if key == Key.up:
        keyAU = False
        return
    if key == Key.down:
        keyAD = False
        return
    if key.char == 'q':
        keyQ = False   
    if key.char == 'e':
        keyE = False
    if key.char == 'a':
        keyA = False
    if key.char == 'd':
        keyD = False
    if key.char == 'w':
        keyW = False
    if key.char == 's':
        keyS = False
def begin():
    global manualyes
    if (manualyes == True):
        manualyes = False
        print("MANUALSTOPPED")
    elif (manualyes == False):
        manualyes = True
# Collect all event until released
#BRENDAN CODE _____________________________________________________________________________________________________

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
        #sendMessage(drone.ipAddress, drone.port, "HSC|" + str(i))

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
    listener =  Listener(on_press = show, on_release = release)   
    listener.start()
    global yaw, roll, pitch, throttle, keyQ, keyE, keyA, keyD, keyW, keyS, keyAU, keyAD, shouldQuit
    global selDrone
    global selDroneTK
    # yaw = 0
    # keyQ = False
    # keyE = False
    # roll = 0 
    # keyA = False
    # keyD = False
    # pitch = 0
    # keyW = False
    # keyS = False
    # throttle = 0
    # keyAU = False
    # keyAD = False
    # shouldQuit = False
    while True:
        if keyQ:
            yaw -= 0.01
        elif keyE:
            yaw += 0.01
        if keyA:
            roll -= 0.01
        elif keyD:
            roll += 0.01
        if keyW:
            pitch += 0.01
        elif keyS:
            pitch -= 0.01
        if keyAU:
            throttle += 0.01
        elif keyAD:
            throttle -= 0.01
        if shouldQuit:
            listener.stop()
            break



        if yaw > 0 and keyQ == False and keyE == False:
            yaw -= 0.01
        elif yaw < 0 and keyQ == False and keyE == False:
            yaw += 0.01
        if roll > 0 and keyA == False and keyD == False:
            roll -= 0.01
        elif roll < 0 and keyA == False and keyD == False:
            roll += 0.01
        if pitch > 0 and keyW == False and keyS == False:
            pitch -= 0.01
        elif pitch < 0 and keyW == False and keyS == False:
            pitch += 0.01
        if throttle > 0 and keyAU == False and keyAD == False:
            throttle -= 0.01
        elif throttle < 0 and keyAU == False and keyAD == False:
            throttle += 0.01

        
        yaw = clamp(yaw)
        roll = clamp(roll)
        pitch = clamp(pitch)
        throttle = clamp(throttle)
        yaw = round(yaw, 2)
        roll = round(roll, 2)
        pitch = round(pitch, 2)
        throttle = round(throttle, 2)
        # print(yaw, " -- yaw")
        # print(roll, " -- roll")
        # print(pitch, " -- pitch")
        # print(throttle, " -- throttle")
        for i in droneList.curselection():
            selDrone = drones[i]
            #print(selDrone)
        
        #print(selDrone.ipAddress)
        if (manualyes == True):
            sendMessage(selDrone.ipAddress, selDrone.port, "|" + str(yaw) + "|" + str(roll) + "|" + str(pitch) + "|" + str(throttle) + "|")
            print(yaw)
        #sendMessage(selDrone.ipAddress, selDrone.port, yaw + str(i))

        
        time.sleep(0.01)

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
        # strData = strData + "|" + addr[0] + "|" + str(addr[1])#the message, the ip, the port
        strData = addr[0] + "*" + str(addr[1]) + "*" + strData#the ip, the port, the message
        # the message is pipe (|) delimited. The ip, port, and message are * delimited
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
    global selDrone
    global selDroneTK
    selDroneTK.set(selDrone.ipAddress)
    #lblDroneIP.config(text = selDrone.ipAddress)
    root.update_idletasks()
    #print(selDrone.ipAddress)
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


#--------------------------------------------
#------------    Main Code ------------------

qFromComms = Queue() #gets information from the comms thread
qToComms = Queue() #sends information to the comms thread
sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

terminate = False
maxDrones = 3
drones = []
#these next two lines are for testing only. Remove them
drones.append(Drone(0, "one", "10.20.18.23", 85))
drones.append(Drone(1, "two", "10.20.18.23", 85))
drones.append(Drone(2, "three", "192.168.4.22", 80))
selDrone = drones[0]

#----- Setup our GUI --------
root = Tk()
root.geometry("400x400")
root.title("Drone Manager")

frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="hello world").grid(column = 0, row = 0)
ttk.Label(frm, text="Drones List").grid(column = 0, row = 1)

listVar = StringVar(value = drones)
droneList = Listbox(master = root,width =10, height = 25, listvariable = listVar)

droneList.grid(column = 0, row = 2)
black = "black"

manualbutton = Button(root, text="Manual", width=5, height=5, command=lambda: begin()).grid(column=3, row=2, padx=50)

selDroneTK = tk.StringVar(root)
button = Button(root,text = "Test!", width=5, height=5, command=lambda: introToAP()).grid()
ttk.Label(root, text="Name | IP | Port").grid(column = 2, row = 1,padx=50)
lblDroneIP = ttk.Label(root, textvariable=selDroneTK).grid(column = 2, row = 2,padx=50)

#-------------------------------------------------------------------------------------------------
#------------------------------------CUSTOM TKINTER GUI----------------------------
#-----------------------------------------------------------------------------

# #create window
# custom = customtkinter.CTk()
# custom.geometry("300x400")
# #create button
# button = customtkinter.CTkButton(master=custom, text="test")
# button.place(relx=0.5, rely=0.5, anchor=CENTER)

#run loop
#-------------custom.mainloop()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Controlling Module")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Swarm Control Module", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="Enable Drone")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="Disable Drone")
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event, text="Test")
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="Manual UDP Console")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Send UDP Message")
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")

        # create textbox
        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        # create tabview
        self.tabview = customtkinter.CTkTabview(self, width=250)
        self.tabview.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.tabview.add("Control")
        self.tabview.add("Info")
        self.tabview.add("Swarm")
        self.tabview.tab("Control").grid_columnconfigure(0, weight=1)  # configure grid of individual tabs
        self.tabview.tab("Info").grid_columnconfigure(0, weight=1)

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.tabview.tab("Control"), dynamic_resizing=False,
                                                        values=["Value 1", "Value 2", "Value Long Long Long"])
        self.optionmenu_1.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.combobox_1 = customtkinter.CTkComboBox(self.tabview.tab("Control"),
                                                    values=["Value 1", "Value 2", "Value Long....."])
        self.combobox_1.grid(row=1, column=0, padx=20, pady=(10, 10))
        self.string_input_button = customtkinter.CTkButton(self.tabview.tab("Control"), text="Direct Command",
                                                           command=self.open_input_dialog_event)
        self.string_input_button.grid(row=2, column=0, padx=20, pady=(10, 10))
        self.label_tab_2 = customtkinter.CTkLabel(self.tabview.tab("Info"), text="Ip, Port will be here")
        self.label_tab_2.grid(row=0, column=0, padx=20, pady=20)

        # create radiobutton frame
        self.radiobutton_frame = customtkinter.CTkFrame(self)
        self.radiobutton_frame.grid(row=0, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.radio_var = tkinter.IntVar(value=0)
        self.label_radio_group = customtkinter.CTkLabel(master=self.radiobutton_frame, text="Mode and Stage Control:")
        self.label_radio_group.grid(row=0, column=2, columnspan=1, padx=10, pady=10, sticky="")
        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=0, text="Manual Mode")
        self.radio_button_1.grid(row=1, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=1, text="Swarm Mode")
        self.radio_button_2.grid(row=2, column=2, pady=10, padx=20, sticky="n")
        self.radio_button_3 = customtkinter.CTkRadioButton(master=self.radiobutton_frame, variable=self.radio_var, value=2)
        self.radio_button_3.grid(row=3, column=2, pady=10, padx=20, sticky="n")

        # create slider and progressbar frame
        self.slider_progressbar_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.slider_progressbar_frame.grid(row=1, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.slider_progressbar_frame.grid_columnconfigure(0, weight=1)
        self.slider_progressbar_frame.grid_rowconfigure(4, weight=1)
        self.seg_button_1 = customtkinter.CTkSegmentedButton(self.slider_progressbar_frame)
        self.seg_button_1.grid(row=0, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_1 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_1.grid(row=1, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.progressbar_2 = customtkinter.CTkProgressBar(self.slider_progressbar_frame)
        self.progressbar_2.grid(row=2, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_1 = customtkinter.CTkSlider(self.slider_progressbar_frame, from_=0, to=1, number_of_steps=4)
        self.slider_1.grid(row=3, column=0, padx=(20, 10), pady=(10, 10), sticky="ew")
        self.slider_2 = customtkinter.CTkSlider(self.slider_progressbar_frame, orientation="vertical")
        self.slider_2.grid(row=0, column=1, rowspan=5, padx=(10, 10), pady=(10, 10), sticky="ns")
        self.progressbar_3 = customtkinter.CTkProgressBar(self.slider_progressbar_frame, orientation="vertical")
        self.progressbar_3.grid(row=0, column=2, rowspan=5, padx=(10, 20), pady=(10, 10), sticky="ns")

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Main Swarm Communications")
        self.scrollable_frame.grid(row=1, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"Drone {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

        # create checkbox and switch frame
        self.checkbox_slider_frame = customtkinter.CTkFrame(self)
        self.checkbox_slider_frame.grid(row=1, column=3, padx=(20, 20), pady=(20, 0), sticky="nsew")
        self.checkbox_1 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Basestation Comms")
        self.checkbox_1.grid(row=1, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_2 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="SBUS Signal")
        self.checkbox_2.grid(row=2, column=0, pady=(20, 0), padx=20, sticky="n")
        self.checkbox_3 = customtkinter.CTkCheckBox(master=self.checkbox_slider_frame, text="Assaf")
        self.checkbox_3.grid(row=3, column=0, pady=20, padx=20, sticky="n")

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Connect to Swarm")
        self.checkbox_3.configure(state="disabled")
        self.checkbox_1.select()
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        self.radio_button_3.configure(state="disabled", text="Auto Mode")
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.optionmenu_1.set("Drone List")
        self.combobox_1.set("Drones")
        self.slider_1.configure(command=self.progressbar_2.set)
        self.slider_2.configure(command=self.progressbar_3.set)
        self.progressbar_1.configure(mode="indeterminnate")
        self.progressbar_1.start()
        self.textbox.insert("0.0", "flup\n\n" + "epic box.\n\n" * 20)
        self.seg_button_1.configure(values=["Sensitivity", "Throttle", "Max Range"])
        self.seg_button_1.set("Value 2")


        my_progressbar = customtkinter.CTkProgressBar(self, orientation="horizontal",
            width=200,
            height=25,
            corner_radius=15,
            mode="indeterminate",
            determinate_speed=5,
            indeterminate_speed=.5,

        )

        my_progressbar.place(anchor="center", x=405, y=450)
        my_progressbar.lift()
        my_progressbar.set(0)
        my_progressbar.start()


#image testing-----------------

    #     global my_image
    #     self.iconbitmap('images/codemy.ico')
    #     my_image = customtkinter.CTkImage(light_image=Image.open("C:\Users\Conno\Downloads\Screenshot 2024-03-28 124033.png"),
	#         dark_image=Image.open("C:\Users\Conno\Downloads\Screenshot 2024-03-28 124033.png"),
	#         size=(180,250)) # WidthxHeight

    # my_label = customtkinter.CTkLabel(root, text="", image=my_image)
    # my_label.pack(pady=10)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Enter a Direct UDP Drone Command:", title="Direct Command")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


#app = App()
#app.mainloop()










#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
#--------- END OF FIRST GRAB ----------
getMyIP() #unsure
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setblocking(0)
sock.bind((UDP_IP, UDP_PORT))

print("Ready3")
#----- END OF SECOND GRAB

#-----------  WHAT WAS ALREADY HERE IS BELOW
t = Thread(target=listen, args=(qFromComms, qToComms))
t.start()
m = Thread(target=manualControl, args=())
m.start()
root.after(1000, checkQueue, qFromComms)
# root.bind("<<updateevent>>", updateDronesList)
root.mainloop()
qToComms.put("TERMINATE") #tell the subloop on the backup thread to quit.
t = qFromComms.get(timeout=3.0)
#give it a chance to quit
print("all done")
exit(0)


