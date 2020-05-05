#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

class Channel:

    def __init__(self,name):
        self.name = name
        self.clients = {}
        self.addresses = {}

    def add(self,client,name,client_address):
        self.clients[client] = name
        self.addresses[client] = client_address
        self.broadcast(bytes(" has joined %s." % self.name,"utf8"),self.clients[client])

    def remove(self,client):
        self.broadcast(bytes(" has left %s." % self.name,"utf8"),self.clients[client])
        del self.clients[client]
        del self.addresses[client]

    def broadcast(self,msg, prefix=""):
        for sock in self.clients:
            sock.send(bytes(prefix, "utf8")+msg)



class Server(Channel):
    def __init__(self,name,host,port,buffersize):
        self.name = name
        self.clients = {}
        self.addresses = {}
        self.channels = {}

        self.buffersize = buffersize
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((host,port))

# wrapper functions for socket

    def listen(self,n):
        self.socket.listen(n)

    def close(self):
        self.socket.close()

# creates a thread for each new connection

    def accept_incoming_connections(self):
        """Sets up handling for incoming clients."""
        while True:
            client, client_address = self.socket.accept()
            print("%s:%s has connected." % client_address)
            client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
            Thread(target=self.handle_client, args=(client,client_address,)).start()

# handles inbound signals from single connection

    def handle_client(self,client,client_address):  # Takes client socket as argument.
        """Handles a single client connection."""
        name = client.recv(self.buffersize).decode("utf8")
        welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
        client.send(bytes(welcome, "utf8"))
        self.add(client,name,client_address)
        channel = None

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

