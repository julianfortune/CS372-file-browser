import socket as sckt
import sys, os
import json

HOST = 'localhost'

def printName():
    print("\u001b[36m", end="")
    print(" _ _      _____   __     _ _   ____                                            ")
    print("\\ \\ \\    |  __ \\ / _|   (_) | |  _ \\                                     _     ")
    print(" \\_\\_\\__ | |__) | |_ ___ _| |_| |_) |_ __ _____      _____  ___ _ __  __\\ '-.  ")
    print(" [______ |  ___/|  _/ _ \\ | |_|  _ <| '__/ _ \\ \\ /\\ / / __|/ _ \\ '__| __     > ")
    print(" / / /   | |    | ||  __/ | | | |_) | | | (_) \\ V  V /\\__ \\  __/ |      /_.-'  ")
    print("/_/_/    |_|    |_| \\___|_|_| |____/|_|  \\___/ \\_/\\_/ |___/\\___|_|             ")
    print("\u001b[0m")

def client(port):

    def getFile(request):
        assert len(request) < 100, "Send string too long!"

        print("Starting client...")
        socket = sckt.socket(sckt.AF_INET, sckt.SOCK_STREAM)

        print("Opening connection with:", "%s:%d" % (HOST, port))
        try:
            socket.connect((HOST, port))
        except:
            print("\u001b[35mError:\u001b[0m Connection failed. Make sure the server is running.\n")
            return

        # Send message to server with command
        print("Sending request:", "'%s'" % request)
        package = {
            "type":"request",
            "message":request
        }

        sendJSON = json.dumps(package)
        socket.send(sendJSON.encode())

        # Wait for response with file
        data = socket.recv(1024) # <- Buffer size
        dataString = data.decode()

        headerSize = dataString.find('}') + 1
        header = json.loads(dataString[:headerSize])

        # Inspect header
        if header["type"] != "response":
            return # Undefined response

        if header["status"] == "error":
            print("\u001b[35mError:\u001b[0m '%s'\n" % header["message"])
            return

        if header["status"] != "ok":
            return # Undefined status

        # File text starts after header
        fileText = dataString[headerSize:]
        fileLength = header["length"]

        print("Receiving file...")

        # Handle recieving the response from the server
        while len(fileText) < fileLength:
            data = socket.recv(1024) # <- Buffer size

            fileText += data.decode()

        print("File recieved.")
        if len(fileText.split('\n')) > 40:
            print("Preview:\n\n\u001b[35m" + '\n'.join(fileText.split('\n')[:20]) +
                  "\u001b[0m\n\n...\n\n\u001b[35m" +
                  '\n'.join(fileText.split('\n')[-20:]) + "\u001b[0m")
        else:
            print("Preview:\n\n\u001b[35m" + fileText + "\u001b[0m")
        print()

        fileName = commandString.split(' ')[1].split('/')[-1]

        if fileName == os.path.basename(__file__):
            print("\u001b[35mError:\u001b[0m Would overwrite this program. \n")
            return

        print("Saving file as %s..." % fileName)

        outputFile = open(fileName,"w+")
        outputFile.write(fileText)
        outputFile.close()

        print("Done.\n")

    socket = None

    while 1:
        try:
            commandString = input("> \u001b[33m")
            print("\u001b[0m", end="")

            if commandString == "quit" or commandString == "q":
                break

            if commandString.split(' ')[0] == "get" and len(commandString.split(' ')) > 1:
                getFile(commandString)
            else:
                print("\u001b[35mInvalid input!\u001b[0m", )
                usage()

        except KeyboardInterrupt:
            break

    if socket:
        print("Closing connection...")
        socket.close()  # close the connection

def usage():
    print("Usage: | get [file name] - requests (plain-text) file from server and saves")
    print("       | quit | q        - quits\n")

def main():
    if len(sys.argv) > 1 and sys.argv[1].isdigit() and int(sys.argv[1]) in range(1024,65535):
        printName()
        usage()

        client(int(sys.argv[1]))
    else:
        print("Error! Usage: python3 client.py [port number]")

if __name__ == "__main__":
    main()