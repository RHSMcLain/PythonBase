class Drone:
    id = -1
    name = ""
    ipAddress = ""
    port = 0
    def __init__(self, id, name, ipAddress, port) -> None:
        self.id = id
        self.name = name
        self.ipAddress = ipAddress
        self.port = port