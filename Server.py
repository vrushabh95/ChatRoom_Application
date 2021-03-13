import threading
import socket
import logging
logging.basicConfig(level=logging.INFO)
logging.info("This is Server Side ")

host = '127.0.0.1' #localhost
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
"""
the first argument AF_INET is the address domain of the socket. This is used when we have an Internet Domain
with any two hosts
The second argument is the type of socket. SOCK_STREAM means that data or characters are read in a continuous flow
"""
server.bind((host, port)) #binding Server to the host and port
server.listen()    #Activate the listening mode for new connection to the server
clients = []      #we put all our client in Clients list
aliases = []      #we put our nicknames in aliases which clients going to give

def broadcast(message):
    '''
    its function that sends the message to all the clients that currently connected to the server.
    for every client in the clients list which is now connected to the server
    simply we will iterate through the list of clients and for each client we need to send the message
    '''
    for client in clients:
        client.send(message)

# Function to handle clients'connections

def handle_client(client):
    '''this function  which will handle the connection of each client computer so client a connect to the server
    send a message to client b computer we want to receive this message from client a and sent it to client b so in
    order to do that we will wrap our code inside try except block which is use catch handle exception.

    '''
    while True:
        try:
            message = client.recv(1024)#msg recieve from the client
            broadcast(message) #broadcat message to all the other clients
        except:
            index = clients.index(client)#in case any errors we wnat to identify the client we need to get rid of client list
            clients.remove(client)#remove that client
            client.close() #close client
            alias = aliases[index] #we need to also remove this alias of that specific client from the aliases
            broadcast(f'{alias} has left the chat room!'.encode('utf-8')) #broadcast to all the clients that this client has left the chat
            aliases.remove(alias) #remove that alias
            break
# Main function to receive the clients connection

def receive():
    '''this is main function which receives the client connection

    '''
    while True:
        print('Server is running and listening ...')
        client, address = server.accept()#ready to accept any incomming connection and running constantly
        print(f'connection is established with {str(address)}') #cannot concanate the string with integer so we need to parse in string
        client.send('alias?'.encode('utf-8'))#we want to send to client some kind of word what is alias.
        alias = client.recv(1024) #information recv from the clients
        aliases.append(alias) #append to alias to list of aliases
        clients.append(client)
        print(f'The alias of this client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat room'.encode('utf-8')) #invoke broadcat function telling that client connected to chat
        client.send('you are now connected!'.encode('utf-8')) #send message from the server to client
        thread = threading.Thread(target=handle_client, args=(client,)) #craete and start thread in order to invoke handle_client function
        thread.start() #thread start

if __name__ == "__main__":
    receive() #invoke receive function