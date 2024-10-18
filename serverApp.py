'''

Client-Server Application:
    This client server application facilitates instant messaging type chat functionality
    wherein messages sent from a client terminal should be visible on the server terminal 
    and vice versa. The app also supports file shares between the client and server 
    terminals. 
'''
import socket



# get the hostname
host = socket.gethostname()
port = 3000  # initiate port no above 1024

'''
    Create a server socket
'''
def server_program():
    try:
        # create an INET, STREAMing socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Socket successfully created")
    except socket.error as err:
        print("socket creation failed with error %s" % (err))

    # bind socket to a public host, and port
    try:
        serversocket.bind(('127.0.0.1', port))
        print("Socket successfully binded")
    except socket.error as err:
        print("socket binding failed with error %s" % (err))

    # configure how many clients the server can listen simultaneously
    serversocket.listen(5)
    print("Socket is listening")

    # Establish connection with client. 
    (client, address) = serversocket.accept()
    print (f'connection from: {str(address)}\n')

    # run a forever loop until we interrupt it or 
    # an error occurs 
    while True:
        # send a connection message to the client. encoding to send byte type. 
        # client.send('Thanks for connecting to the server !'.encode()) 

        data = client.recv(1024).decode()     # receive data from the client
        print(f"From connected user: {str(data)}")  # print in terminal

        data = input(' -> ')                        # get data input
        if data.lower().strip() == 'exit':          # if data is 'exit' then close the connection
            # close the server socket
            break
        client.send(data.encode())                  # send data to the client

    # Close the connection with the client 
    client.close()

if __name__ == '__main__':
    server_program()