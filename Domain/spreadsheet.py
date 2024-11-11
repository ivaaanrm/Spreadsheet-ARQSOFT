
import sys
from pathlib import Path
from dataclasses import field
from typing import Dict
from rich import print

sys.path.append(str(Path(__file__).parent))

from Data.cooridante import Coordinate
from Data.cell import Cell
from Exception.exceptions import InvalidCoordinate

class Spreadsheet:
    def __init__(self) -> None:
        self.cells: Dict[Coordinate, Cell] = {}

    def __getitem__(self, cell_coords: str) -> Cell:
        try:
            coord = Coordinate.from_string(cell_coords)
            return self.cells.get(coord, Cell())
        except InvalidCoordinate as e:
            print(f"Invalid coordinate: {e}")
            return None

    def __setitem__(self, cell_coords: str, content: str) -> None:
        try:
            coord = Coordinate.from_string(cell_coords)
            self.cells[coord] = Cell(content)
        except InvalidCoordinate as e:
            print(f"Invalid coordinate: {e}")

    def __repr__(self) -> str:
        return f"{self.cells}"


if __name__ == "__main__":
    
    sheet = Spreadsheet()
    
    sheet['A1'] = "hola"
    # spreadsheet['AA1'] = "hola"
    # spreadsheet['1'] = "hola"
    
    print(sheet['A1'])
    
    # print(spreadsheet['1'])
    
    # print(spreadsheet)
        
        
        
        
        
        
    