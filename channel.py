#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class Channel:

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
        self.broadcast(bytes(" has joined %s." % self.name,"utf8"),self.clients[client])

# removes socket from clients list
    def remove(self,client):
        self.broadcast(bytes(" has left %s." % self.name,"utf8"),self.clients[client])
        del self.clients[client]
        del self.addresses[client]

# sends message to all sockets stored in clients list
    def broadcast(self,msg, prefix=""):
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8")+msg)



class Server(Channel):

# initiates server using input variables
    def __init__(self,name,host,port,buffersize):
        self.name = name
        self.clients = {}
        self.addresses = {}
        self.channels = {}
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
        self.channels[name] = Channel(name)

    def shout(self,socket):
        for channel in self.channels:
            msg = '{channel}%s' % channel
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
#        welcome = 'Welcome %s! Type {quit} to exit.' % name
#        client.send(bytes(welcome, "utf8"))
        self.add(client,name,client_address)
        channel = None

        # sends list of rooms to client
        self.shout(client)

        channel = self # temporary for testing

        while True:
            msg = client.recv(self.buffersize)
            if msg != bytes("{quit}", "utf8"):
                if channel is not None:
                    channel.broadcast(msg, name+": ")
            else:
                client.send(bytes("{quit}", "utf8"))
                client.close()
                if channel is not None:
                    channel.remove(client)
                self.remove(client)
                return
    
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

