from socket import *
from threading import *
from tkinter import *

# Set to store connected clients and list to store messages
clients = set()
messages = []


# Function to handle communication with each client
def clientThread(clientSocket, clientAddress):
    while True:
        # Receive message from client
        message = clientSocket.recv(1024).decode("utf-8")
        # Print client's message in server console
        print(clientAddress[0] + ":" + str(clientAddress[1]) + " says: " + message)
        # Append client's message to the list of messages
        messages.append(
            clientAddress[0] + ":" + str(clientAddress[1]) + " says: " + message
        )
        # Send received message to all clients except the sender
        for client in clients:
            if client is not clientSocket:
                client.send(
                    (
                        clientAddress[0]
                        + ":"
                        + str(clientAddress[1])
                        + " says: "
                        + message
                    ).encode("utf-8")
                )

        # If client closes connection, remove it from the clients set
        if not message:
            clients.remove(clientSocket)
            # Print disconnection message in server console
            print(clientAddress[0] + ":" + str(clientAddress[1]) + " disconnected")
            break

    # Close client's socket connection
    clientSocket.close()


# Function to send a message from server to all clients
def sendServerMessage(message):
    for client in clients:
        client.send(("Server: " + message).encode("utf-8"))


# Function to update the messages displayed in the GUI
def update_messages():
    chat_area.config(state=NORMAL)
    chat_area.delete(1.0, END)
    for msg in messages:
        chat_area.insert(END, msg + "\n")
    chat_area.config(state=DISABLED)
    chat_area.yview(END)
    # Schedule the update_messages function to run again after 1 second
    window_server.after(1000, update_messages)


# Function to handle sending message from server
def handle_send():
    message = entry_message.get()
    if message:
        sendServerMessage(message)
        entry_message.delete(0, END)


# Create GUI window for server
window_server = Tk()
window_server.title("Chat Server")
window_server.config(background="sandybrown")

# Text area to display chat messages
chat_area = Text(window_server, width=30, height=10)
chat_area.pack(padx=10, pady=10)

# Entry field to type and send messages
entry_message = Entry(window_server, width=30)
entry_message.pack(pady=5)

# Button to send messages
send_button = Button(window_server, text="Send", width=10, command=handle_send)
send_button.pack(pady=10)

# Start updating the messages in the GUI
update_messages()

# Create server socket
hostSocket = socket(AF_INET, SOCK_STREAM)
hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Set server's IP address and port number
hostIp = "127.0.0.1"
portNumber = 7500
hostSocket.bind((hostIp, portNumber))
hostSocket.listen()
print("Waiting for connection...")

# Accept incoming connections from clients
while True:
    clientSocket, clientAddress = hostSocket.accept()
    clients.add(clientSocket)
    # Print connection established message in server console
    print(
        "Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1])
    )
    # Start a new thread to handle communication with the client
    thread = Thread(
        target=clientThread,
        args=(
            clientSocket,
            clientAddress,
        ),
    )
    thread.start()
    # Start the GUI main loop
    window_server.mainloop()






# from socket import *
# from threading import *
# from tkinter import *

# clients = set()
# messages = []


# def clientThread(clientSocket, clientAddress):
#     while True:
#         message = clientSocket.recv(1024).decode("utf-8")
#         print(clientAddress[0] + ":" + str(clientAddress[1]) + " says: " + message)
#         messages.append(
#             clientAddress[0] + ":" + str(clientAddress[1]) + " says: " + message
#         )
#         for client in clients:
#             if client is not clientSocket:
#                 client.send(
#                     (
#                         clientAddress[0]
#                         + ":"
#                         + str(clientAddress[1])
#                         + " says: "
#                         + message
#                     ).encode("utf-8")
#                 )

#         if not message:
#             clients.remove(clientSocket)
#             print(clientAddress[0] + ":" + str(clientAddress[1]) + " disconnected")
#             break

#     clientSocket.close()


# def sendServerMessage(message):
#     for client in clients:
#         client.send(("Server: " + message).encode("utf-8"))


# def update_messages():
#     chat_area.config(state=NORMAL)
#     chat_area.delete(1.0, END)
#     for msg in messages:
#         chat_area.insert(END, msg + "\n")
#     chat_area.config(state=DISABLED)
#     chat_area.yview(END)
#     window_server.after(1000, update_messages)


# def handle_send():
#     message = entry_message.get()
#     if message:
#         sendServerMessage(message)
#         entry_message.delete(0, END)


# window_server = Tk()
# window_server.title("Chat Server")
# window_server.config(background="sandybrown")

# chat_area = Text(window_server, width=30, height= 10 ,font=('Arial', 14), bg='white')
# chat_area.pack(padx=10, pady=10)

# entry_message = Entry(window_server, width=30)
# entry_message.pack(pady=5)

# send_button = Button(window_server, text="Send", width=10, command=handle_send)
# send_button.pack(pady=10)

# update_messages()

# hostSocket = socket(AF_INET, SOCK_STREAM)
# hostSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# hostIp = "122.0.0.1"
# portNumber = 5000
# hostSocket.bind((hostIp, portNumber))
# hostSocket.listen()
# print("Waiting for connection...")

# while True:
#     clientSocket, clientAddress = hostSocket.accept()
#     clients.add(clientSocket)
#     print(
#         "Connection established with: ", clientAddress[0] + ":" + str(clientAddress[1])
#     )
#     thread = Thread(
#         target=clientThread,
#         args=(
#             clientSocket,
#             clientAddress,
#         ),
#     )
#     thread.start()
#     window_server.mainloop()
