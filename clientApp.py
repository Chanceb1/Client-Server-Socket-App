'''

Client-Server Application:
    This client server application facilitates instant messaging type chat functionality
    wherein messages sent from a client terminal should be visible on the server terminal 
    and vice versa. The app also supports file shares between the client and server 
    terminals. 
'''

# from socket import socket, connect, sendall
import socket
from sys import exit as sys_exit


# Create a socket object
try:
    # Create a socket object, configure it to use IPv4 and TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket successfully created")
except socket.error as err:
    print("socket creation failed with error %s" % (err))

# define the host address
host = '127.0.0.1'  # localhost as code is running on same pc
port = 3000         # port number 

# Define the port on which you want to connect
# get user input for port number
# def userInput(prompt):
#     while True:
#         try:
#             userInput = int(input(prompt))
#             if userInput < 0 or userInput > 65535:
#                 raise ValueError
#             return userInput
#         except ValueError:
#             print("Invalid input. Enter a valid port number between 0 and 65535.")

# port = userInput("Enter port number: ")


# connect to the server on local host
try:
    s.connect((host, port))
    print("Successfully Connected to server")
except socket.error as err:
    print("Connection to server failed with error %s" % (err))
    sys_exit()

message = input(" -> ")  # take input

while message.lower().strip() != 'bye':
    s.send(message.encode())  # send message

    data = s.recv(1024).decode()  # receive response

    print(f'Received from server: {data}')  # print in terminal

    message = input(" -> ")  # again take input

s.close()  # close the connection
