import socket
import pickle


class Network:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.addr = (self.server, self.port)
        self.name = name
        self.id = None
        self.data = self.connect()

    def connect(self):
        try:
            self.client.connect(self.addr)
            data = pickle.loads(self.client.recv(4096))
            for pid in data:
                if data[pid]["name"].startswith("Player"):
                    data[pid]["name"] = self.name
                    self.id = pid
                    break
            return data
        except Exception as e:
            print(f"Connection failed: {e}")
            return None

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            print(e)
            return {}
