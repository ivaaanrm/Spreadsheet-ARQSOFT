

from SpreadsheetController import SpreadsheetController
from Interfaces.CommandInterface import Terminal
from Interfaces.UIInterface import UI

COMMAND_LINE_INTERFACE = True

class Program:
    def __init__(self):
        self.__controller = SpreadsheetController()
        self.terminal = Terminal(self.__controller)
        self.ui = UI(self.__controller)
        
    def start(self):
        if COMMAND_LINE_INTERFACE:
            self.terminal.run()
        else:
            self.ui.run()
        

if __name__ == "__main__":
    Program().start()
    