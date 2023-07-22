import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]  # 1: listen and accept, 2: send commands
queue = Queue()
connections = []
addresses = []


def create_socket():
    try:
        global host
        global port
        global s

        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as e:
        print("Socket creation error " + str(e))


def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the Port: " + str(port))

        s.bind((host, port))
    except socket.error as e:
        print("Socket binding error " + str(e) + "\n" + ". Retrying...")
        bind_socket()


def socket_listen():
    s.listen(5)


def send_commands(connection):
    while True:
        cmd = input().strip()

        if cmd == "quit":
            connection.close()
            s.close()
            sys.exit()

        if len(cmd) == 0:
            continue

        connection.send(str.encode(cmd))
        client_response = str(connection.recv(1024), "utf-8")
        print(client_response, end="")


def accept_connection():
    for conn in connections:
        conn.close

    del connections[:]
    del addresses[:]

    while True:
        try:
            connection, address = s.accept()
            connection.setblocking(True)

            connections.append(connection)
            addresses.append(address)

            print("Connection has been ebstablished! IP: " + str(address[0]) + " PORT: " + str(address[1]))
        except socket.error as e:
            print("Error accepting connection " + str(e))


def main():
    create_socket()
    bind_socket()
    socket_listen()
    accept_connection()


main()
