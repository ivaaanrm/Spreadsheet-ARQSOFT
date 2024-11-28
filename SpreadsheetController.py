import os
from pathlib import Path


from Interfaces.CommandInterface import CommandLineInterface
from Interfaces.UIInterface import UIInterface

from Domain.FileHandler.fileSaver import FileSaver
from Domain.FileHandler.fileParser import FileParser

from Domain.spreadsheet import Spreadsheet


class SpreadsheetController:
    def __init__(self):
        self.command_interface = CommandLineInterface()
        self.ui_interface = UIInterface()
        self.file_saver = FileSaver()
        self.file_loader = FileParser()
        
        self.sheet: Spreadsheet = None
    
    def run():
        
        raise NotImplementedError

    def init_empty_spreadsheet(self):
        return Spreadsheet()
    
    def save_spreadsheet(self, sheet: Spreadsheet, path: str):
        self.file_saver.save(sheet, path)
        
    def load_spreadsheet(self, path: str):
        return self.file_loader.load(path)
    
    



if __name__ == "__main__":
    
    controller = SpreadsheetController()
    
    sheet = controller.init_empty_spreadsheet()

    sheet['a2'] = "hola"
    print(sheet)

