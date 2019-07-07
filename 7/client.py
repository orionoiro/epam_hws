import socket
import threading


class Client:
    def __init__(self, host_ip, port):
        self.nickname = input('Enter your nickname: ')
        self.host_ip = host_ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.host_ip, self.port))

    def send(self):
        while True:
            message = self.nickname + '%' + input()
            self.socket.send(message.encode('ascii'))
            if message.split('%', 1)[1] == 'exit()':
                self.socket.close()
                break

    def recieve(self):
        try:
            while True:
                data = self.socket.recv(1024)
                if not data:
                    break
                print(str(data.decode('ascii')))
        except Exception:
            print('disconnected')


if __name__ == '__main__':
    test = Client('127.0.0.1', 20145)
    test.connect()

    thread_send = threading.Thread(target=test.send)
    thread_send.start()

    thread_receive = threading.Thread(target=test.recieve)
    thread_receive.start()
