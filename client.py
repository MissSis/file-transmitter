import socket
import os
from datetime import datetime

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

class Client:

    def __init__(self, files, ip_address, port):
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


    def sendFiles(self):
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