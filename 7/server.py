import socket
import threading


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.clients = []

    def add_client(self):
        while True:
            client, address = self.socket.accept()
            self.clients.append(client)
            threading.Thread(target=self.listen_to_client, args=[client]).start()

    def listen_to_client(self, client):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                self.send_to_others(client, data)
            except:
                client.close()
                break

    def send_to_others(self, client, data):
        data = data.decode('ascii')
        data = data.split('%', 1)
        if data[1] == 'exit()':
            data = f'{data[0]} disconnected'.encode('ascii')
            self.clients.remove(client)
        else:
            data = f'{data[0]}: {data[1]}'.encode('ascii')

        for each in self.clients:
            if each != client:
                each.send(data)


if __name__ == '__main__':
    s = Server('127.0.0.1', 20145)
    s.socket.listen(1)
    print('Chat server started')
    thread_ac = threading.Thread(target=s.add_client).start()
