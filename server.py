import socket
from datetime import date

numOfBytesForFileSize = 13

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

class Server:

    def __init__(self, destination):
        self.destination = destination

    def accept(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), port))
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