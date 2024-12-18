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
    
    def run(self) -> None:
        while True:
            choice, arguments = self.menu.get_choice()
            
            if choice == Options.EXECUTE_FILE_COMMANDS:
                self.read_commands_from_file(*arguments)
                
            elif choice == Options.NEW_SPREADSHEET: 
                self.new_spreadsheet()
                
            elif choice == Options.EDIT_CELL:
                self.edit_cell(arguments)
                
            elif choice == Options.LOAD_SPREADHSEET: 
                self.sheet = self.load_spreadsheet(arguments)
                
            elif choice == Options.SAVE_SPREADHSEET:
                self.save_spreadsheet(arguments)
                
            elif choice == Options.EXIT_PROGRAM:
                print("Exiting program.")
                break
            
            print(self.sheet)
            print("\n")

    def read_commands_from_file(self, *args):
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
            
            
            

    def edit_cell(self, arguments: List[str]):
        """Función para añadir una nueva celda

        Args:
            arguments (List[str]): argumentos que definen la coordenada y el contenido
        """
        cell_coords, cell_content = arguments
        self.sheet[cell_coords] = cell_content
            
    def new_spreadsheet(self) -> Spreadsheet:
        """Funciión para generar un nuevo Spreadsheet vacio

        Returns:
            Spreadsheet: Devuelve un spreadsheet vacio
        """
        self.sheet = Spreadsheet()
        print("* Spreadhseet created!")
    
    def save_spreadsheet(self, arguments: List[str]) -> None:
        """Función para guardar un spreadsheet en un archivo

        Args:
            sheet (Spreadsheet): _description_
            path (str): _description_
        """
        return NotImplementedError
        
    def load_spreadsheet(self, arguments: List[str]) -> Spreadsheet:
        """Función para cargar un  spreadsheet de un archivo

        Args:
            path (str): _description_

        Returns:
            Spreadsheet: _description_
        """
        return NotImplementedError
    
    
if __name__ == "__main__":
    controller = SpreadsheetController()
    controller.run()


