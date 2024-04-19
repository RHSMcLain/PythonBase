import socket
from Drone import Drone

sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

maxDrones = 3
drones = []
# UDP_IP = "192.168.50.124"
UDP_IP = "10.127.174.114"
UDP_PORT = 5005

def handshake(parts, addr):
    i = int(parts[1])
    if (i == -1):
        i = len(drones)
        drone =  Drone(i, parts[2], addr[0], addr[1])
        drones.append(drone)
        listDrones()
        sendMessage(drone.ipAddress, drone.port, "HSC|" + str(i))

    else:
        if drones[i].name == parts[2]:
            #we could update here
            drones[i].ipAddress = addr[0]
            drones[i].port = addr[1]
        
def sendMessage(ipAddress, port, msg):
    
    bMsg = msg.encode("ascii")
    sendSocket.sendto(bMsg, (ipAddress, port))
    print("sent message")
def listDrones():
    global drones
    for drone in drones:
        print(drone.name, drone.ipAddress, drone.port, "\t") 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
print("Ready3")
while True:
    
    data, addr = sock.recvfrom(1024)
    strData = data.decode("utf-8")
    print("Received message %s" % data)
    print(addr)
    
    print("----")
    print(strData)
    
    parts = strData.split("|")
    print(parts)
    cmd = parts[0]

    if cmd == "HND":
        #HANDSHAKE
        handshake(parts, addr)
    
