import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import json
import os
from client import Client
from server import Server


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__() # Call the inherited classes __init__ method
        # uic.loadUi('testgui.ui', self) # Load the .ui file
        uic.loadUi(os.path.join(sys.path[0], "testgui.ui"), self) # Load the .ui file

        # load in the prefs
        self.ipAddressInput.addItems(prefs["ip_addresses"])
        self.portInput.setText(str(prefs["port"]))

        # set button listener
        self.clientButton.clicked.connect(self.clientButtonListener)
        self.serverButton.clicked.connect(self.serverButtonListener)

        self.show() # Show the GUI

    def clientButtonListener(self):
        self.client = Client() # get the arguements out of the gui
        self.client.start()

    def serverButtonListener(self):
        self.server = Server() # get the arguements out of the gui
        self.server.start()
    

if "prefs.json" not in os.listdir(sys.path[0]):
    prefs = {
        "port": 1234,
        "ip_addresses": [],
        "destination": sys.path[0]
    }
    out_file = open(os.path.join(sys.path[0], "prefs.json"), "w")
    json.dump(prefs, out_file)
else:
    prefs = json.load(open(os.path.join(sys.path[0], "prefs.json"), "r"))

app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui_MainWindow() # Create an instance of our class
app.exec_() # Start the application