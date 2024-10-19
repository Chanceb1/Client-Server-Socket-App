'''
Client-Server Application:
    This client server application facilitates instant messaging type chat functionality
    wherein messages sent from a client terminal should be visible on the server terminal 
    and vice versa. The app also supports file shares between the client and server 
    terminals. 
'''

import socket
import os
from sys import exit


# define the host and port
host = '127.0.0.1'  
port = 3000          

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

# Function to send a file to the server
def sendFile(client):
    while True:
        filePath = input("Enter the file path to send: ").strip()
        if os.path.exists(filePath):
            break
        print("File does not exist!")

    fileName = os.path.basename(filePath)
    fileSize = os.path.getsize(filePath)

    # Send the 'file' command to notify the server of an incoming file
    client.send("file".encode())

    # Wait for server acknowledgment
    if client.recv(1024).decode() != "ready":
        print("Server not ready to receive file.")
        return
    
    # Send the file name
    client.send(fileName.encode())

    # Wait for server acknowledgment
    if client.recv(1024).decode() != "name_received":
        print("Error in file name transmission.")
        return
    
    # Send file size
    client.send(str(fileSize).encode())

    # Wait for server acknowledgment
    if client.recv(1024).decode() != "size_received":
        print("Error in file size transmission.")
        return
    
    # Send the file in chunks
    with open(filePath, 'rb') as f:
        print(f"Sending file: {fileName} ({fileSize} bytes)")
        chunk = f.read(1024)
        while chunk:
            client.send(chunk)
            chunk = f.read(1024)

    print(f"File {fileName} sent successfully!")
    return

# Main function
def clientProgram():
    # Create a socket object, configure it to use IPv4 and TCP
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print(f"Socket creation failed with error: {err}")
        exit()

    # connect to the server on local host
    try:
        s.connect((host, port))
        print(f"Successfully connected to server at {host}:{port}")
    except socket.error as err:
        print(f"Connection to server failed with error: {err}")
        exit()

    while True:
        msg = input(" -> ")  # take input

        if msg.lower().strip() == 'bye':  # exit condition
            print("Disconnecting from the server...")
            break
        elif msg.lower().strip() == 'file':  # File transfer mode
            sendFile(s)
        else:
            s.send(msg.encode())  # Send message

        try:
            # Receive the response
            data = s.recv(1024).decode()
            if not data:  # If the server has disconnected
                print("Server disconnected.")
                break
            print(f"Received from server: {str(data)}")
        except socket.error as e:
            print(f"Error receiving data: {e}")
            break

    s.close()  # close the connection


if __name__ == '__main__':
    clientProgram()