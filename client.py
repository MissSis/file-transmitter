import socket
import os
from datetime import datetime
from PyQt5.QtCore import QThread


class Client(QThread):

    def __init__(self, files, ip_address, port):
        super(Client, self).__init__()
        self.files = files
        self.ip_address = ip_address
        self.port = port
        self.progress = 0

    def printDataRate(self, startingPoint, endingPoint, totalSize):
        seconds = (endingPoint - startingPoint).total_seconds()
        dataRate = (totalSize / (1000000 * seconds))
        print()
        print("The datarate of this transfer was: " + str(round(dataRate, 2)) + "MB/s,   transmitted " + 
        str(totalSize) + " Bytes in " + str(seconds) + " seconds")


    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.ip_address, self.port))

        fileList = [open(x, "rb") for x in self.files]
        fileSizes = [os.path.getsize(x) for x in self.files]
        fileNames = [os.path.basename(x) for x in self.files]
        totalSize = sum(fileSizes)

        sentBytes = 0
        i = 0
        startingPoint = datetime.now()
        s.send(bytes(f"{len(fileNames):03}", "utf-8"))

        for f in fileList:
            l = f.read(1024)
            infoLen, info = self.getFileInformation(fileSizes[i], fileNames[i])
            s.send(bytes(infoLen, "utf-8"))
            s.send(bytes(info, "utf-8"))
            while (l):
                s.send(l)
                sentBytes += 1024
                # printProgressBar(sentBytes, totalSize, prefix = 'Progress:', suffix = 'Complete', length = 50)
                self.progress = sentBytes / totalSize
                l = f.read(1024)
            i += 1
        endingPoint = datetime.now()
        self.printDataRate(startingPoint, endingPoint, totalSize)
        s.close()

    '''
    format for information: (fileSize, fileName)
    fileSize will be encoded in 13 bytes
    '''
    def getFileInformation(self, fileSize, fileName):
        information = f"{fileSize:013}" + fileName
        numOfBytes = len(bytes(information, "utf-8"))

        if numOfBytes > 999:
            raise Exception("The size of the file and the name were too long")
        infoLen = f"{numOfBytes:03}"
        return infoLen, information