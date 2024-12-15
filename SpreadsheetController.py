import os
from pathlib import Path


from Interfaces.CommandInterface import CommandLineInterface
from Interfaces.UIInterface import UIInterface

from Domain.FileHandler.fileSaver import FileSaver
from Domain.FileHandler.fileParser import FileParser

from Domain.spreadsheet import Spreadsheet

class Menu:
    SAVE_FILE = "Save file"
    LOAD_FILE = "Load file"
    NEW_SPREADSHEET = "New spreadsheet"
    
    def __init__(self):
        self.options = {
            "0": "Save File",
            "1": "Load File",
            "2": "New Spreadsheet",
            "3": "Exit",
        }

    def display(self) -> None:
        """Displays the menu options."""
        print("Menu:")
        for key, value in self.options.items():
            print(f"{key}: {value}")

    def get_choice(self) -> str:
        """Prompts the user to select a menu option."""
        self.display()
        choice = input("Select an option: ").strip()
        if choice in self.options:
            return choice
        else:
            print("Invalid choice. Please try again.")
            return self.get_choice()


class SpreadsheetController:
    def __init__(self):
        self.file_saver = FileSaver()
        self.file_loader = FileParser()
        self.menu = Menu()
        self.sheet: Spreadsheet = None
    
    def run(self) -> None:
        while True:
            choice = self.menu.get_choice()

            if choice == "0":  # Save File
                self.save_spreadsheet()
            elif choice == "1":  # Load File
                path = input("Enter file path:")
                self.sheet = self.load_spreadsheet(path)
            elif choice == "2":  # New Spreadsheet
                self.new_spreadsheet()
            elif choice == "3":  # Exit
                print("Exiting program.")
                break
            
            print(self.sheet)
            
    def new_spreadsheet(self) -> Spreadsheet:
        return Spreadsheet()
    
    def save_spreadsheet(self, sheet: Spreadsheet, path: str) -> None:
        self.file_saver.save(sheet, path)
        
    def load_spreadsheet(self, path: str) -> Spreadsheet:
        return self.file_loader.load(path)
    
    
if __name__ == "__main__":
    
    controller = SpreadsheetController()
    
    controller.run()


