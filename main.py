

from SpreadsheetController import SpreadsheetController
from Interfaces.CommandInterface import Terminal
from Interfaces.UIInterface import UI

COMMAND_LINE_INTERFACE = True

class Program:
    def __init__(self):
        self.__controller = SpreadsheetController()
        
    def start(self):
        if COMMAND_LINE_INTERFACE:
            self.terminal = Terminal(self.__controller)
            self.terminal.run()
        else:
            self.ui = UI(self.__controller)
            self.ui.run()
        
if __name__ == "__main__":
    Program().start()
    