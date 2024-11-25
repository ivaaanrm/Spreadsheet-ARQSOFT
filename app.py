

from Interfaces.CommandInterface import CommandLineInterface
from Interfaces.UIInterface import UIInterface
from Domain.spreadsheet import Spreadsheet




if __name__ == "__main__":
    
    sheet = Spreadsheet()
    sheet['a2'] = "=hola"
    print(sheet)

