from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
from person import Person
# GLOBAL CONSTANTS
HOST = 'localhost'
PORT = 999
ADDR = (HOST, PORT)
MAX_CONNECTIONS = 10
BUFSIZ =1024

#GLOBAL VARIABLES
persons = []
# INTIALIZE SERVER
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR) #set  up server


def broadcast(msg,name):
    """
    send new message to all clients
    :param msg:bytes["utf-8"]
    :param name:str
    :return:
    """
    for person in persons:
        client = person.client
        client.send(bytes(name + " : " , "utf-8" + msg))



def client_communication(person):
    """
    Thread to handle all messages from client
    :param client:PERSON
    :return:None
    """
    run = True
    client = person.client
    addr = person.addr

    #get persons name
    name = client.recv(BUFSIZ.decode('utf-8 '))
    msg = f"{name} has joined the chat"
    broadcast(msg)
    while run:
        msg = client.recv(BUFSIZ)
        if msg !=bytes("{quit}",'utf-8'):
            client.send(bytes("{quit}","utf-8"))
            client.close()
            persons.remove(person)
        else:
            client.send(msg)




def wait_for_connection(SERVER):
    """
    wait for connection from new clients, start new thread once commited
    :param SERVER:SOCKET
    :return:None
    """
    run = True
    while run:
        try:
            client,addr = SERVER.accept()
            person = Person(addr,client)
            persons.append(person)
            print(f"[CONNECTION] {addr} connected to the server at {time.time()}")
            Thread(target=client_communication, args=(person,)).start()
        except Exception as err:
            print("Faliure")
            run = False
    print("SERVER CRASHED")


if __name__ =='__main__':
    SERVER.listen(10) # LISTEN FOR CONNECTIONS
    print("[STARTED]Waiting for connections.......")
    ACCEPT_THREAD = Thread(target=wait_for_connection)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()