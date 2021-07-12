import socket
from datetime import date
from PyQt5.QtCore import QThread

numOfBytesForFileSize = 13


class Server(QThread):

    def __init__(self, destination):
        super(Server, self).__init__()
        self.destination = destination

    def run(self):
        port = 1234
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", port))
        s.listen(1)
    
        clientsocket, address = s.accept()

        numOfFiles = clientsocket.recv(3)
        numOfFiles = int(numOfFiles.decode("utf-8"))
        print("[Server] about to receive " + str(numOfFiles) + " files")

        for i in range(numOfFiles):
            msg = clientsocket.recv(3)
            headerSize = int(msg.decode("utf-8"))
            header = clientsocket.recv(headerSize).decode("utf-8")

            fileSize, fileName = self.extractInformation(header)
            print("[Server] Received header:", str(fileSize), fileName)
            f = open(self.createFileName(fileName), "wb")
            pendingBytes = fileSize
            while pendingBytes > 0:
                if pendingBytes >= 1024:
                    l = clientsocket.recv(1024)
                    pendingBytes -= 1024
                else:
                    l = clientsocket.recv(pendingBytes)
                    pendingBytes = 0
                f.write(l)
        
            print("[Server] Successfully received file:", fileName)
            f.close()
        
        clientsocket.close()
        s.close()

    def extractInformation(self, header):
        size = int(header[:numOfBytesForFileSize])
        name = header[numOfBytesForFileSize:]
        return size, name

    def createFileName(self, fileName):
        dotIndex = fileName.rfind(".")
        firstPart, lastPart = fileName[:dotIndex], fileName[dotIndex:]
        return self.destination + firstPart + "-" + date.today().strftime("%b-%d-%Y") + lastPart


# server = Server(dest)
# server.accept(1234)