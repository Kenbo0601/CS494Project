#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class Room:

# initiates name and client list
    def __init__(self,name):
        self.name = name
        self.clients = {}
        self.addresses = {}

# helper get function
    def name():
        return self.name

# adds socket to client list
    def add(self,client,name,client_address):
        self.clients[client] = name
        self.addresses[client] = client_address
        self.broadcast(" has joined %s." % self.name,self.clients[client])

# removes socket from clients list
    def remove(self,client):
        if client in self.clients:
            self.broadcast(" has left %s." % self.name,self.clients[client])
            del self.clients[client]
            del self.addresses[client]

# sends message to all sockets stored in clients list
    def broadcast(self,msg, prefix=""):
        for sock in self.clients:
            sock.send(bytes(prefix+'['+str(len(msg))+']'+msg, "utf8"))



class Server(Room):

# initiates server using input variables
    def __init__(self,name,host,port,buffersize):
        self.name = name
        self.clients = {}
        self.addresses = {}
        self.rooms = {}
        self.create("test")
        self.create("another")
        self.create("magic")

        self.buffersize = buffersize
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((host,port))

# wrapper functions for socket - may be dropped if encapsulated further

    def listen(self,n):
        self.socket.listen(n)

    def close(self):
        self.socket.close()

# list management functions

    def create(self,name):
        self.rooms[name] = Room(name)

    def join(self,name,client):
        if name in self.rooms:
            room = self.rooms[name]
            room.add(client,self.clients[client],self.addresses[client])
            return self.rooms[name]
        else:
            return None

    def drop(self,room,client):
        if room in self.rooms:
            self.rooms[room].remove(client)

    def make(self,name):
        if name not in self.rooms:
            self.rooms[name] = Room(name)
            self.broadcast(name,"{room}")   # tell everyone there is a new room

    def shout(self,socket):
        for room in self.rooms:
            msg = '{room}['+str(len(room))+']'+room
            socket.send(bytes(msg,'utf8'))

# creates a thread for each new connection

    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        while True:
            client, client_address = self.socket.accept()
            print("%s:%s has connected." % client_address)
            client.send(bytes("Greetings! Type your name and press enter!", "utf8"))
            Thread(target=self.handle_client, args=(client,client_address,)).start()

# handles inbound signals from single connection

    def handle_client(self,client,client_address):  # Takes client socket as argument.
        """Handles a single client connection."""
        name = client.recv(self.buffersize).decode("utf8")
        print(("%s:%s adopted the name: " % client_address) + name)
#        welcome = 'Welcome %s! Type {quit} to exit.' % name
#        client.send(bytes(welcome, "utf8"))
        self.add(client,name,client_address)
        room = None

        # sends list of rooms to client
        self.shout(client)

        while True:
            msg = client.recv(self.buffersize).decode()
            if msg[:6] == "{quit}":
                client.send(bytes("{quit}", "utf8"))
                client.close()
                if room is not None:
                    room.remove(client)
                self.remove(client)
                return
            elif msg[:6] == "{join}":
                room = self.join(msg[6:],client)
            elif msg[:6] == "{drop}":
                self.drop(msg[6:],client)
            elif msg[:6] == "{make}":
                self.make(msg[6:])
            elif msg[:6] == "{room}":
                self.shout(client)
            else:
                if room is not None:
                    room.broadcast(msg, name+": ")
    
HOST = ''
PORT = 9009

server = Server("CS494 Project",HOST,PORT,1024)

if __name__ == "__main__":
    server.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=server.accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    server.close()

