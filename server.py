import socket 
from _thread import *
import sys
from collections import defaultdict as df
import time


class Server:
    def __init__(self):
        self.rooms = df(list)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    def accept_connections(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.server.bind((self.ip_address, int(self.port)))
        self.server.listen(100)
        print("o servidor está funcionando :)")

        while True:
            connection, address = self.server.accept()
            print(str(address[0]) + ":" + str(address[1]) + " conectado")

            start_new_thread(self.clientThread, (connection,))

        self.server.close()

    
    def clientThread(self, connection):
        user_id = connection.recv(1024).decode().replace("usuario ", "")
        room_id = connection.recv(1024).decode().replace("se juntou ", "")

        if room_id not in self.rooms:
            connection.send("nova zap-sala criada".encode())
        else:
            connection.send("bem vindo ao zap".encode())

        self.rooms[room_id].append(connection)

        while True:
            try:
                message = connection.recv(1024)
                print(str(message.decode()))
                if message:
                    if str(message.decode()) == "FILE":
                        self.broadcastFile(connection, room_id, user_id)

                    else:
                        message_to_send = "o " + str(user_id) + " disse: " + message.decode()
                        self.broadcast(message_to_send, connection, room_id)

                else:
                    self.remove(connection, room_id)
            except Exception as e:
                print(repr(e))
                print("ficamos por aqui, o client desconectou e encerraremos o servidor")
                break
    
    
    def broadcastFile(self, connection, room_id, user_id):
        file_name = connection.recv(1024).decode()
        lenOfFile = connection.recv(1024).decode()
        for client in self.rooms[room_id]:
            if client != connection:
                try: 
                    client.send("FILE".encode())
                    time.sleep(0.1)
                    client.send(file_name.encode())
                    time.sleep(0.1)
                    client.send(lenOfFile.encode())
                    time.sleep(0.1)
                    client.send(user_id.encode())
                except:
                    client.close()
                    self.remove(client, room_id)

        total = 0
        print(file_name, lenOfFile)
        while str(total) != lenOfFile:
            data = connection.recv(1024)
            total = total + len(data)
            for client in self.rooms[room_id]:
                if client != connection:
                    try: 
                        client.send(data)
                        # time.sleep(0.1)
                    except:
                        client.close()
                        self.remove(client, room_id)
        print("enviado")



    def broadcast(self, message_to_send, connection, room_id):
        for client in self.rooms[room_id]:
            if client != connection:
                try:
                    client.send(message_to_send.encode())
                except:
                    client.close()
                    self.remove(client, room_id)

    
    def remove(self, connection, room_id):
        if connection in self.rooms[room_id]:
            self.rooms[room_id].remove(connection)


if __name__ == "__main__":
    ip_address = "localhost"
    port = 12345

    s = Server()
    s.accept_connections(ip_address, port)
