import socket as sckt
import sys, os
import json

HOST = 'localhost'

def printName():
    print("\u001b[36m", end="")
    print(" _ _      _____   __     _ _   _____                                     ")
    print("\\ \\ \\    |  __ \\ / _|   (_) | /  ___|                             _     ")
    print(" \\_\\_\\__ | |__) | |_ ___ _| |_| (___   ___ _ ____   _____ _ __  __\\ '-.  ")
    print(" [______ |  ___/|  _/ _ \\ | |_ \\___ \\ / _ \\ '__\\ \\ / / _ \\ '__| __     > ")
    print(" / / /   | |    | ||  __/ | |  ____) |  __/ |   \\ V /  __/ |      /_.-'  ")
    print("/_/_/    |_|    |_| \\___|_|_| |_____/ \\___|_|    \\_/ \\___|_|         ")
    print("\u001b[0m")

def server(port):
    print("Starting server on %s port %d..." % (HOST, port))

    # Open socket
    socket = sckt.socket(sckt.AF_INET, sckt.SOCK_STREAM)
    address = (HOST, port)
    socket.bind(address)
    socket.listen(1)

    conn, addr = None, None

    # Constantly listen for connections
    while True:
        try:
            conn, addr = socket.accept()
            print("\nConnection from %s on port %d" % addr)

            data = None

            while data != b'':
                data = conn.recv(1024)
                if not data:
                    break

                request = json.loads(data.decode())

                if request["type"] == "request":
                    command, fileName = request["message"].split(' ')[:2]

                    print("Request: \u001b[35m", command, fileName, "\u001b[0m")

                    if command == 'get':
                        requestedFile = None

                        try:
                            requestedFile = open(fileName, "r")
                        except IOError:
                            package = {
                                "type":"response",
                                "status":"error",
                                "message":"File not found!"
                            }

                            conn.send(json.dumps(package).encode())

                        if requestedFile:
                            fileSize = os.path.getsize(fileName)
                            fileText = requestedFile.read()

                            package = {
                                "type":"response",
                                "status":"ok",
                                "length":fileSize
                            }

                            print("Sending file: %s (%d bytes)" % (fileName, fileSize))
                            conn.send((json.dumps(package)+fileText).encode())

                            requestedFile.close()

                            break

            print("Closing connection.")
            conn.close()
            conn, addr = None, None

        except KeyboardInterrupt:
            print("\nStopping server...")

            if conn:
                if addr:
                    print("Closing connection with %s on port %d" % (addr))

                conn.close()

            print("Closing socket...")
            socket.close()

            break

    print("Done.\n")

def main():
    if len(sys.argv) > 1 and sys.argv[1].isdigit() and int(sys.argv[1]) in range(1024,65535):
        printName()
        server(int(sys.argv[1]))
    else:
        print("Error! Usage: python3 server.py [port number]")

if __name__ == "__main__":
    main()