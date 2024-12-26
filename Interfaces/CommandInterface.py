from abc import ABC, abstractmethod
from pathlib import Path
from typing import TYPE_CHECKING, List, Tuple 

if TYPE_CHECKING:
    from SpreadsheetController import SpreadsheetController

class Options:
    EXECUTE_FILE_COMMANDS = "RF"
    NEW_SPREADSHEET = "C"
    EDIT_CELL = "E"
    LOAD_SPREADHSEET = "L"
    SAVE_SPREADHSEET = "S"
    EXIT_PROGRAM = "X"
    
class Menu:
    def __init__(self):
        self.__options = {
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
        for key, value in self.__options.items():
            print(f"{key}: {value}")


    def get_choice(self) -> Tuple[str,List[str]]:
        """Prompts the user to select a menu option."""
        self.display()
        user_input = input("Select an option: ").strip()
        parts = user_input.split()
        choice = parts[0].upper()  # First part is the choice
        arguments = parts[1:] if len(parts) > 1 else []  # Remaining parts are arguments
        if choice in self.__options:
            return choice, arguments

        else:
            print("Invalid choice. Please try again.")
            return self.get_choice()

class UserInterface(ABC):
    @abstractmethod
    def run(self) -> None:
        pass
    
class Terminal(UserInterface):
    def __init__(self, controller: 'SpreadsheetController') -> None:
        self.menu = Menu()
        self.controller = controller

    def run(self) -> None:
        while True:
            choice, args = self.menu.get_choice()
            self.run_command(choice, args)
            print(self.controller.sheet)
            print("\n")
    
    def run_command(self, option: str, args: List[str]) -> None:
        if option == Options.EXECUTE_FILE_COMMANDS:
            self.__read_commands_from_file(*args)
            
        elif option == Options.NEW_SPREADSHEET: 
            self.controller.new_spreadsheet()
            
        elif option == Options.EDIT_CELL:
            self.controller.set_cell_content(args[0], args[1])
            
        elif option == Options.LOAD_SPREADHSEET: 
            self.sheet = self.controller.load_spreadsheet_from_file(args[0])
            
        elif option == Options.SAVE_SPREADHSEET:
            self.controller.save_spreadsheet_to_file(args[0])
            
        elif option == Options.EXIT_PROGRAM:
            print("Exiting program.")
            exit()
            
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
            
            self.run_command(choice, arguments)
    
    