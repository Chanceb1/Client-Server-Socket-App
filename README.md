# Simple Client-Server Socket Application

This is a simple client-server application that enables bidirectional file transfer and text messaging using socket programming. The client can connect to the server to send and receive both files and text messages.

## Screenshots

![GUI Application Screenshot](Interface/public/gui)

*Application GUI interface showcasing the terminal-based client-server communication*

## Features

- **Bidirectional Communication:** Supports sending and receiving text messages between the client and server.
- **File Transfer:** Enables file transfer from client to server and vice versa.
- **Socket Programming:** Uses TCP sockets for reliable communication.

## Requirements

- Python 3.x

# Client Script

### when prompted for input ( -> ) the user can:
* type any text message to send to the server
* type 'file' to enter file transfer mode
    then enter the file's 'file path' to send file to server
* type 'bye' to disconnect from the server and exit application


# Server Script

### when prompted for input ( -> ) the user can:

* type any message to send to the client
* type 'file' to enter file transfer mode then enter the file's 'file path' to send file to client
* type 'bye' to exit the application
* type 'exit' to shutdown the server,
closing any active client connections prior to shutting down
