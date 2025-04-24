from socket import *
from threading import *
from tkinter import *

# Setting Up Network Connection:
clientSocket = socket(AF_INET , SOCK_STREAM)  # create a socket object representing the client-side connection
# AF_INET specifies the IPv4 address
clientSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #reusing the address and port combination immediately after closing the socket

# Defining Server Details:
hostIp = "127.0.0.1"
portNumber = 7500

# Connecting to Server:
clientSocket.connect((hostIp, portNumber))

# Building the Chat Window:
window_cleint = Tk()  # Creates the main window for the chat application
window_cleint.title("Chat Client") # Sets the title of the window 
window_cleint.config(background="sandybrown")  # Sets the background color


txtMessages = Text(window_cleint)   # Creating a text box where messages
txtMessages.pack(padx=10, pady=10)

txtYourMessage = Entry(window_cleint, width=30)    # Creating an entry field for user's message
txtYourMessage.pack(pady=5)

# Defining the Send Message Functionality:
def sendMessage(): # When user clicks on 'Send' button this function called 
    clientMessage = txtYourMessage.get()
    txtMessages.insert(END, "\n" + "You: "+ clientMessage) # Adds message to the textbox
    clientSocket.send(clientMessage.encode("utf-8")) #  Converts message into bytes and sends it to server
    txtYourMessage.delete(0, END) # Clears the text box after sending a message
# Creating the Send Message Button:
btnSendMessage = Button(window_cleint, text="Send", width=10, command=sendMessage)  # Creates a button labeled "Send" ##Clicking this button triggers the sendMessage function
btnSendMessage.pack(padx=5, pady=10)

# Defining the Receive Message Functionality
def recvMessage(): # function that runs in separate thread to receive messages from server
    while True:  # create  an infinite loop
        serverMessage = clientSocket.recv(1024).decode("utf-8") # receive  data from server
        print(serverMessage) # print the received message
        txtMessages.insert(END, "\n"+serverMessage) # insert the received message into the chat window text-box 

recvThread = Thread(target=recvMessage)  # Create new thread with target as our function
recvThread.daemon = True # set the thread as daemon so it will die when the main app dies
recvThread.start() # start the thread

window_cleint.mainloop()
