'''
Client-Server Application:
    This client server application facilitates instant messaging type chat functionality
    wherein messages sent from a client terminal should be visible on the server terminal 
    and vice versa. The app also supports file shares between the client and server 
    terminals. 

    Server side of the application: enables threading to handle multiple client connections
    and file sharing functionality.
'''

import socket           # for socket
import threading        # for multiple clients
import os               # for file operations


# define fixed host and port
host = '127.0.0.1'
port = 3000  # initiate port num above 1024


def handleClient (clientSocket, address):

    print(f"Connection from: {address}\n") # Notify server of a new connection

    while True:
        try:
            data = clientSocket.recv(1024).decode() # receive data from the client

            if not data:  # if data is not received, break
                break
            
            if data.lower().strip() == 'file':
                receiveFile(clientSocket)       # call function to receive file
                continue
            else:
                print(f"From {str(address)}: {str(data)}")  # Print the client's message

            # Respond to the client
            msg = input(" -> ")

            if msg.lower().strip() == 'exit':  # if server user msg is 'exit' then close server   
                print(f"Closing connection...")
                clientSocket.send("Server is shutting down.".encode())
                clientSocket.close()
                exit()      

            clientSocket.send(msg.encode())

        except socket.error as e:
            print(f"Error with client {address}:{e}")
            break

    # Close the connection
    clientSocket.close()


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
        return  # Exit if the file size is invalid
        
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
    # Alternative: savePath = fileName (if you want to save it using the full path)

    # Write the file to disk
    with open(savePath, 'wb') as f:
        f.write(receivedData)
    
    print(f"File {savePath} received successfully!")
    
    # # Close the client socket
    # clientSocket.close()
    # return


def server_program():
    try:
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create an INET, STREAMing socket
        serverSocket.bind((host, port))         # bind socket to a public host, and port
        serverSocket.listen(5)                  # Listen for clients, 5 clients can queue
        print(f"Server started at {host}:{port}\nlistening for connections... ")

    except socket.error as err:
        print(f"Socket creation/bind failed with error: {err}")
        return

    # run forever loop until we interrupt 
    # or an error occurs 
    while True:
        try:
            # Establish connection with client. 
            (client, address) = serverSocket.accept()
            # print (f'Connection from: {str(address)}\n')
            
            # send a connection message to the client. encoding to send byte type. 
            # client.send('Thanks for connecting to the server !'.encode())

            # Start a new thread to handle the client
            clientHandler = threading.Thread(target=handleClient, args=(client, address))
            clientHandler.start()

        except KeyboardInterrupt:
            print("\nServer shutting down...")
            break

    serverSocket.close()
        
if __name__ == '__main__':
    server_program()