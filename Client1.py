import threading
import socket
import logging
logging.basicConfig(level=logging.INFO)
logging.info("This is Client Side ")

alias = input('Choose an alias >>> ')
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('127.0.0.1', 59000)) #connect the client to localhost and port

def client_receive():
    '''this function create for receiving the message other client through the server'''
    while True:
        try:
            message = client.recv(1024).decode('utf-8')#decodenig message
            if message == "alias?": #which defined to the server
                client.send(alias.encode('utf-8')) #send the alias
            else:
                print(message)#print the message whatever meg received from the server
        except:
            print('Error!')#handling any eroor py printing msg error
            client.close()
            break


def client_send():
    '''this function create for sending the message other client through the server'''

    while True:
        message = f'{alias}: {input("")}' #this is alias and message you wamt to type
        client.send(message.encode('utf-8')) #sending the message
#creating two thread one for client receive and client send

receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()