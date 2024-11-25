

import sys
import pandas as pd

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
        self.__cells: Dict[Coordinate, Cell] = {}
        
    def set_cell(self, coords: str, content: str):
        try:
            coord = Coordinate.from_string(coords)
            self.__cells[coord] = Cell(content)
        except InvalidCoordinate as e:
            pass

    def __getitem__(self, cell_coords: str) -> Cell:
        try:
            coord = Coordinate.from_string(cell_coords)
            return self.__cells.get(coord, Cell())
        except InvalidCoordinate as e:
            print(f"Invalid coordinate: {e}")
            return None

    def __setitem__(self, cell_coords: str, content: str) -> None:
        try:
            coord = Coordinate.from_string(cell_coords)
            self.__cells[coord] = Cell(content)
        except InvalidCoordinate as e:
            print(f"Invalid coordinate: {e}")


    def to_dataframe(self, value: bool = False) -> pd.DataFrame:
        """ Show in terminal the Spreadsheet with excel format"""
        data = {}
        for coord, cell in self.__cells.items():
            row, col = coord.row, coord.column
            if row not in data:
                data[row] = {}
            data[row][col] = cell.value if value else cell.content
        
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.reindex(sorted(df.columns), axis=1)  # Ordenar columnas
        
        df.columns = [Coordinate.number_to_letter(col) for col in df.columns]  # Ajustar col a base 1
        return df.fillna("")

    def __repr__(self) -> str:
        return f"{self.to_dataframe()}\n\n{self.to_dataframe(True)}"
    
    

if __name__ == "__main__":
    
    sheet = Spreadsheet()
    
    sheet['A1'] = "Hola"
    sheet['B2'] = "100.00"
    sheet['C3'] = "=B2+1"
    
    print(sheet)

        
        
        
        
        
        
    