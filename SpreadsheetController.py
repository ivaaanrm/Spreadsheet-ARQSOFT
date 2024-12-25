import os
from pathlib import Path
from typing import List, Tuple


from Interfaces.CommandInterface import CommandLineInterface
from Interfaces.UIInterface import UIInterface

from Domain.FileHandler.fileSaver import FileSaver
from Domain.FileHandler.fileParser import FileParser

from Domain.spreadsheet import Spreadsheet

class Options:
    EXECUTE_FILE_COMMANDS = "RF"
    NEW_SPREADSHEET = "C"
    EDIT_CELL = "E"
    LOAD_SPREADHSEET = "L"
    SAVE_SPREADHSEET = "S"
    EXIT_PROGRAM = "X"
    
class Menu:
    def __init__(self):
        self.options = {
            Options.EXECUTE_FILE_COMMANDS: "Read commands from File",
            Options.NEW_SPREADSHEET: "Create a New Spreadsheet",
            Options.EDIT_CELL: "Edit a cell",
            Options.LOAD_SPREADHSEET: "Load a Spreadsheet from a file",
            Options.SAVE_SPREADHSEET: "Save the Spreadsheet to a file",
            Options.EXIT_PROGRAM: "Exit"
        }

    def display(self) -> None:
        """Displays the menu options."""
        print("Menu:")
        for key, value in self.options.items():
            print(f"{key}: {value}")


    def get_choice(self) -> Tuple[str,List[str]]:
        """Prompts the user to select a menu option."""
        self.display()
        user_input = input("Select an option: ").strip()
        parts = user_input.split()
        choice = parts[0].upper()  # First part is the choice
        arguments = parts[1:] if len(parts) > 1 else []  # Remaining parts are arguments
        if choice in self.options:
            return choice, arguments

        else:
            print("Invalid choice. Please try again.")
            return self.get_choice()


class SpreadsheetController:
    def __init__(self):
        self.file_saver = FileSaver()
        self.file_loader = FileParser()
        self.menu = Menu()
        self.sheet: Spreadsheet = None

    def set_cell_content(self, coord: str, str_content: str) -> None:
        self.sheet[coord] = str_content
        a = self.get_cell_content_as_float(coord)
    
    def get_cell_content_as_float(self, coord: str) -> float:
        return self.sheet[coord].value
        
    def get_cell_content_as_string(self, coord: str) -> str:
        return self.sheet[coord].content_str
    
    def get_cell_formula_expression(self, coord: str) -> str:
        return self.sheet[coord].content_str
        
    def save_spreadsheet_to_file(self, s_name_in_user_dir: str) -> None:
        self.file_saver.save(self.sheet, s_name_in_user_dir)
    
    def load_spreadsheet_from_file(self, s_name_in_user_dir: str) -> None:
        self.sheet = self.file_loader.load(s_name_in_user_dir)

    def run(self) -> None:
        while True:
            choice, arguments = self.menu.get_choice()
            
            if choice == Options.EXECUTE_FILE_COMMANDS:
                self.__read_commands_from_file(*arguments)
                
            elif choice == Options.NEW_SPREADSHEET: 
                self.new_spreadsheet()
                
            elif choice == Options.EDIT_CELL:
                self.set_cell_content(arguments)
                
            elif choice == Options.LOAD_SPREADHSEET: 
                self.sheet = self.load_spreadsheet_from_file(arguments)
                
            elif choice == Options.SAVE_SPREADHSEET:
                self.save_spreadsheet_to_file(arguments)
                
            elif choice == Options.EXIT_PROGRAM:
                print("Exiting program.")
                break
            
            print(self.sheet)
            print("\n")
            
    def new_spreadsheet(self) -> Spreadsheet:
        """Funciión para generar un nuevo Spreadsheet vacio
        
        Returns:
            Spreadsheet: Devuelve un spreadsheet vacio
        """
        self.sheet = Spreadsheet()
        print("* Spreadhseet created!")

    def __read_commands_from_file(self, *args):
        if not args:
            return None
            
        filepath = Path(*args)
        
        if not filepath.exists():
            raise FileNotFoundError("File doesn't exists")
        
        with open(filepath, 'r') as f:
            raw_commands = f.readlines()
        
        for command in raw_commands:
            parts = command.split()
            choice = parts[0]  # First part is the choice
            arguments = parts[1:] if len(parts) > 1 else []  # Remaining parts are arguments
    
    
if __name__ == "__main__":
    controller = SpreadsheetController()
    # controller.run()

    controller.new_spreadsheet()
    controller.set_cell_content("A2","5")
    controller.set_cell_content("A11","=A2+A2")
    controller.set_cell_content("I1", "=(A5*4)/(A2+A2)+SUMA(A1;A2;3;4;5;A6:A12)")
    #controller.get_cell_content_as_float("A11")
    print(controller.get_cell_content_as_float("I1"))

