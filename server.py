import socket
import threading
import tkinter as tk

window = tk.Tk()
window.title("Sever")

# top frame

topFrame = tk.Frame(window)
topFrame.pack(side=tk.TOP, pady=(5, 0))

    # start button

btnStart = tk.Button(topFrame, text="Connect", command=lambda : start_server())
btnStart.pack(side=tk.LEFT)

    # stop button

btnStop = tk.Button(topFrame, text="Stop", command=lambda : stop_server(), state=tk.DISABLED)
btnStop.pack(side=tk.LEFT)


# middle frame

middleFrame = tk.Frame(window)
middleFrame.pack(side=tk.TOP, pady=(5, 0))

    # host info

lblHost = tk.Label(middleFrame, text = "Host: X.X.X.X")
lblHost.pack(side=tk.LEFT)

    # port info

lblPort = tk.Label(middleFrame, text = "Port:XXXX")
lblPort.pack(side=tk.LEFT)


# client list

clientFrame = tk.Frame(window)
lblLine = tk.Label(clientFrame, text="*******************CLIENT LIST*****************").pack()
clientFrame.pack(side=tk.BOTTOM, pady=(5, 10))

    # scroll bar

scrollBar = tk.Scrollbar(clientFrame)
scrollBar.pack(side=tk.RIGHT, fill=tk.Y)

tkDisplay = tk.Text(clientFrame, height=15, width=40)
tkDisplay.pack(side=tk.LEFT, fill=tk.Y, padx=(5, 0))
tkDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")

scrollBar.config(command=tkDisplay.yview)

# server variables

server = None
HOST_ADDR = "0.0.0.0"
HOST_PORT = 8080
clients = []
clients_names = []

def start_server():
    btnStart.config(state=tk.DISABLED)
    btnStop.config(state=tk.NORMAL)

    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((HOST_ADDR,HOST_PORT))
    server.listen(5) # listen for clients

    threading._start_new_thread(accept_clients,(server," "))
    lblHost["text"] = "Host: " + HOST_ADDR
    lblPort["text"] = "Port: " + str(HOST_PORT)

def stop_server():
    btnStart.config(state=tk.NORMAL)
    btnStop.config(state=tk.DISABLED)
    lblHost["text"] = "Host: X.X.X.X"
    lblPort["text"] = "Port: XXXX"

def accept_clients(the_server, y):
    while True:
        client, addr = the_server.accept()
        clients.append(client)

        threading._start_new_thread(send_receive_client_message, (client, addr))

def send_receive_client_message(client_connection, client_ip_addr):
    global server, client_name, clients, clients_addr
    client_msg = " "

    client_name  = client_connection.recv(4096)
    client_connection.send("Welcome " + client_name + ". Use 'exit' to quit")

    clients_names.append(client_name)

    update_client_names_display(clients_names)


    while True:
        data = client_connection.recv(4096)
        if not data: break
        if data == "exit": break

        client_msg = data

        idx = get_client_index(clients, client_connection)
        sending_client_name = clients_names[idx]

        for c in clients:
            if c != client_connection:
                c.send(sending_client_name + "->" + client_msg)

    idx = get_client_index(clients, client_connection)
    del clients_names[idx]
    del clients[idx]
    client_connection.close()

    update_client_names_display(clients_names)  # update client names display

# helper functions

def get_client_index(client_list, curr_client):
    idx = 0
    for conn in client_list:
        if conn == curr_client:
            break
        idx = idx + 1

    return idx


def update_client_names_display(name_list):
    tkDisplay.config(state=tk.NORMAL)
    tkDisplay.delete('1.0', tk.END)

    for c in name_list:
        tkDisplay.insert(tk.END, c+"\n")
    tkDisplay.config(state=tk.DISABLED)

window.mainloop()
