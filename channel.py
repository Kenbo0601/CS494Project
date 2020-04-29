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
    channels = {}

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Greetings from the cave! Now type your name and press enter!", "utf8"))
        Thread(target=handle_client, args=(client,client_address,server,)).start()

def handle_client(client,client_address,channel):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    channel.broadcast(bytes(msg, "utf8"))
    channel.add(client,name,client_address)

    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            channel.broadcast(msg, name+": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            channel.remove(client)
            channel.broadcast(bytes(" has left the chat.","utf8"),name)
            return

HOST = ''
PORT = 9009
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

server = Server("CS494 Project")


if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()

