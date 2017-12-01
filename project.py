'''
Thomas Nix
ITCS 3166
Professor Cheng
Completed 12/1/2017
'''

#import socket module
from socket import *


#Main function to encapsulate socket connection code
def main():
    
    #Prepare a server socket
    serverSocket = socket(AF_INET, SOCK_STREAM)
    IP_ADDR = gethostbyname(gethostname())
    PORT = 6789
    BUFFER_SIZE = 1024

    print "Host: ",IP_ADDR

    #Set server options
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #This is important to prevent port blockage. This line will allow subsequent connections on any non-blocked port.
    serverSocket.bind((IP_ADDR, PORT))
    serverSocket.listen(1)

    while True: 
        #Establish the connection
        print 'Ready to serve...'
        connectionSocket, addr = serverSocket.accept()

        #Attempt connection
        try:
            message = connectionSocket.recv(BUFFER_SIZE)
            print "Message: ", message
            filename = message.split()[1]
            print "filename: ", filename
            print "f: " , filename[1:]
            f = open(filename[1:])
            outputdata = f.read()
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n") # Sets the header information prior to sending data
            #Send the content of the requested file to the client 
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i])
            connectionSocket.send("\r\n") # Terminate line endings
            connectionSocket.close() # Close socket at end of send
           
        except IOError:
            print "404 Error encountered"
           
            #Send response message for file not found
            #I decided to also make a 404 page to send.
            filename = '404.html'
            f = open(filename)
            outputdata = f.read()
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n")
            for i in range(0, len(outputdata)):
                connectionSocket.send(outputdata[i])
            connectionSocket.send("\r\n")
            #Close client socket
            connectionSocket.close() # Close socket at end of send

    #Important to close the socket when you're done!
    serverSocket.close()

#Execute main function
main()
