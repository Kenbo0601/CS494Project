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
    def name(self):
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
        print("Broadcasting from room \'%s\'" % self.name)
        for sock in self.clients:
            #sock.send(bytes(prefix+'['+str(len(msg))+']'+*/msg, "utf8"))
            sock.send(bytes(prefix+msg, "utf8"))

# sends list of members in room
    def list(self,socket):
        #message header
        msg = '{memb}'
        #assembles list of rooms seperated by commas
        for client in self.clients:
            msg += self.clients[client] + ','
        #sends entire message as one block
        socket.send(bytes(msg,'utf8')) #sending just room names


class Server(Room):

# initiates server using input variables
    def __init__(self,name,host,port,buffersize):
        self.name = name
        self.clients = {}
        self.addresses = {}
        self.rooms = {}
        self.make("test")
        self.make("another")
        self.make("magic")

        self.buffersize = buffersize
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.bind((host,port))

# wrapper functions for socket - may be dropped if encapsulated further

    def listen(self,n):
        self.socket.listen(n)

    def close(self):
        self.socket.close()

# adds socket to client list
    def add(self,client,name,client_address):
        self.clients[client] = name
        self.addresses[client] = client_address

# removes socket from clients list
    def remove(self,client):
        if client in self.clients:
            del self.clients[client]
            del self.addresses[client]


# list management functions

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
            print("Created room \'%s\'" % name)
        else:
            print("\'%s\' already exists" % name)

    def shout(self,socket):
        #message header
        msg = '{room}'
        #assembles list of rooms seperated by commas
        for room in self.rooms:
            msg += room + ','
        #sends entire message as one block
        socket.send(bytes(msg,'utf8')) #sending just room names

# sends message to specific client
    def whisper(self,client,msg):
        print(client)
        for k in list(self.clients):
            if self.clients[k] == client:
                k.send(bytes(msg,"utf8"))

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
        print(("%s:%s adopted the name " % client_address) + '\'' + name + '\'')
#        welcome = 'Welcome %s! Type {quit} to exit.' % name
#        client.send(bytes(welcome, "utf8"))
        self.add(client,name,client_address)
        room = None

        # sends list of rooms to client
        # self.shout(client)

        while True:
            msg = client.recv(self.buffersize).decode()
            print(("Recieved \'%s\' from " % msg) + name)
            if msg[:6] == "{quit}": #client just left the room
                #client.send(bytes("{quit}", "utf8"))
                #client.close() //don't want to close the connection, just leave the room
                if room is not None:
                    print("\'%s\' left room \'%s\'" % (name, room.name) )
                    room.remove(client)
                #self.remove(client)
                #return //dont wanna get out of this loop
            elif msg[:6] == "{join}":
                room = self.join(msg[6:],client)
                if room is not None:
                    print("\'%s\' joined room \'%s\'" % (name, room.name) )
                else:
                    print("No room named \'%s\'" % msg[6:])
            elif msg[:6] == "{drop}":
                self.drop(msg[6:],client)
            elif msg[:6] == "{make}":
                self.make(msg[6:])
            elif msg[:6] == "{room}":
                print("Sending room list to \'%s\'" % name)
                self.shout(client)
            elif msg[:6] == "{memb}":
                if room is not None:
                    print("Sending room clients list to \'%s\'" % name)
                    room.list(client)
                else:
                    print("%s is not in a room" % name)
            elif msg[:6] == "{priv}":
                i = msg[7:].index('}')
                target = msg[7:i+7] # should extract who message should go to
                msg = msg[:7] + self.clients[client] + msg[i+7:] # swap client and target names in message
                print(msg) # should print out message with swapped target and client names
                self.whisper(target,msg) # send message to target
            elif msg[:6] == "{exit}": #client leaves the server, close the connection
                client.send(bytes("{exit}", "utf8"))
                self.remove(client)
                for room in self.rooms:
                    self.drop(room,client)
                client.close()
                return
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

