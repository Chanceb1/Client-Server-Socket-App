'''
Client-Server Application:
    This client server application facilitates instant messaging type chat functionality
    wherein messages sent from a client terminal should be visible on the server terminal 
    and vice versa. The app also supports file shares between the client and server 
    terminals. The server supports threading allowing for multiple client connections.

    Server side of the application: enables threading to handle multiple client connections
    and file sharing functionality.

    when prompted for input ( -> ) the user can:
        * type any message to send to the client
        * type 'file' to enter file transfer mode
            then enter the file's 'file path' to send file to client
        * type 'bye' to exit the application
        * type 'exit' to shutdown the server
            closing any active client connections prior to shutting down the server
'''

import socket           # for socket
import threading        # for multiple clients
import os               # for file operations
import time             # for the sleep function

# Global variables
shutdown_flag = False   # Global flag to control server shutdown
host = '127.0.0.1'      # fixed for now
port = 3000  # initiate port num above 1024


def handleClient (clientSocket, address):
    global shutdown_flag

    print(f"Connection from: {address}\n") # Notify server of a new connection

    while not shutdown_flag:
        try:
            data = clientSocket.recv(1024).decode() # receive data from the client

            if not data:  # if data is not received, break
                break
            
            if data.lower().strip() == 'file':
                receiveFile(clientSocket)       # call function to receive file
            elif data.lower().strip() == 'bye':  # if client msg is 'bye' then close connection
                print(f"Client {address} has disconnected.")
                clientSocket.close()
                break
            else:
                print(f"From {str(address)}: {str(data)}")  # Print the client's message

            # Respond to the client
            msg = input(" -> ")

            if msg.lower().strip() == 'exit':  # if server user msg is 'exit' then close server   
                print(f"Closing connection...")
                clientSocket.send(msg.encode())
                time.sleep(1)
                clientSocket.close()
                shutdown_flag = True   # Set the shutdown flag to true to stop the server
                break
            elif msg.lower().strip() == 'file': # if server user msg is 'file' then send file
                sendFile(clientSocket)
            else:
                clientSocket.send(msg.encode())

        except socket.error as e:
            print(f"Error with client {address}:{e}")
            break

    # Close the connection
    clientSocket.close()


# Function to send a file to the client
def sendFile(clientSocket):
    while True:
        filePath = input("Enter the file path to send: ").strip()
        if os.path.exists(filePath):
            break
        else:
            print("File does not exist!")


    fileName = os.path.basename(filePath)
    fileSize = os.path.getsize(filePath)

    # Send the 'file' command to notify the server of an incoming file
    clientSocket.send("file".encode())

    # Wait for server acknowledgment
    if clientSocket.recv(1024).decode() != "ready":
        print("Client not ready to receive file.")
        return
    
    # Send the file name
    clientSocket.send(fileName.encode())

    # Wait for server acknowledgment
    if clientSocket.recv(1024).decode() != "name_received":
        print("Error in file name transmission.")
        return
    
    # Send file size
    clientSocket.send(str(fileSize).encode())

    # Wait for server acknowledgment
    if clientSocket.recv(1024).decode() != "size_received":
        print("Error in file size transmission.")
        return
    
    # Send the file in chunks
    with open(filePath, 'rb') as f:
        print(f"Sending file: {fileName} ({fileSize} bytes)")
        chunk = f.read(1024)
        while chunk:
            clientSocket.send(chunk)
            chunk = f.read(1024)

    print(f"File {fileName} sent successfully!")
    return


# Function to receive a file from the client
def receiveFile(clientSocket):

    # Send ready signal
    clientSocket.send("ready".encode())
    
    # Receive the file name
    fileName = clientSocket.recv(1024).decode()  # Receive the file name
    if not fileName:
        return
    
    # Acknowledge file name received
    clientSocket.send("name_received".encode())

    # Receive file size
    fileSizeStr = clientSocket.recv(1024).decode()  # Receive file size
    try:
        fileSize = int(fileSizeStr)  # Convert the received size to an integer
        # Acknowledge file size received
        clientSocket.send("size_received".encode())
    except ValueError:
        print(f"Received invalid file size: {fileSize}")
        return 
        
    print(f"Receiving file: {fileName} ({fileSize} bytes)")
    

    receivedData = b''  # byte string to store the file data
    # Receive the file in chunks
    while len(receivedData) < fileSize:
        chunk = clientSocket.recv(1024)
        if not chunk:
            break
        receivedData += chunk


    # Extract only the file name to save it in the current directory, or use full path
    savePath = os.path.basename(fileName)  # Save in current directory

    # Write the file to disk
    with open(savePath, 'wb') as f:
        f.write(receivedData)
    
    print(f"File {savePath} received successfully!")
    

def server_program():
    global shutdown_flag

    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create an INET, STREAMing socket
        serverSocket.bind((host, port))         # bind socket to a public host, and port
        serverSocket.listen(1)                  # Listen for client connection
        print(f"Server started at {host}:{port}\nlistening for connections... ")

    except socket.error as err:
        print(f"Socket creation/bind failed with error: {err}")
        return

    # run forever loop until we interrupt 
    # or an error occurs 
    while not shutdown_flag:
        try:
            # Establish connection with client. 
            (client, address) = serverSocket.accept()
            # print (f'Connection from: {str(address)}\n')
            handleClient(client, address)  # Handle the client connection

            # Start a new thread to handle the client
            # clientHandler = threading.Thread(target=handleClient, args=(client, address))
            # clientHandler.start()

        except KeyboardInterrupt:
            print("\nServer shutting down...")
            shutdown_flag = True
            break

    serverSocket.close()
        
if __name__ == '__main__':
    server_program()