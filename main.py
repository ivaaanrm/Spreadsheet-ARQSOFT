import argparse
from SpreadsheetController import SpreadsheetController
from Interfaces.CommandInterface import Terminal
from Interfaces.UIInterface import UI

class Program:
    def __init__(self, use_ui):
        self.__controller = SpreadsheetController()
        self.use_ui = use_ui
        
    def start(self):
        if self.use_ui:
            self.ui = UI(self.__controller)
            self.ui.run()
        else:
            self.terminal = Terminal(self.__controller)
            self.terminal.run()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the program with UI or terminal interface.")
    parser.add_argument('--ui', action='store_true', help="Run the program with UI interface.")
    args = parser.parse_args()
    
    Program(use_ui=args.ui).start()
