

import sys
import pandas as pd

from pathlib import Path
from dataclasses import field
from typing import Dict
from rich import print

sys.path.append(str(Path(__file__).parent))

from Data.coordinate import Coordinate
from Data.cell import Cell
from Exception.exceptions import InvalidCoordinate

class Spreadsheet:
    def __init__(self) -> None:
        self.__cells: Dict[Coordinate, Cell] = {}
    
    def __getitem__(self, cell_coords: str) -> Cell:
        try:
            coord = Coordinate.from_string(cell_coords)
            return self.__cells.get(coord, Cell(coords=coord, sheet=self))
        except InvalidCoordinate as e:
            return None

    def __setitem__(self, cell_coords: str, content: str) -> None:
        try:
            coord = Coordinate.from_string(cell_coords)
            self.__cells[coord] = Cell(coord, content, self)
        except InvalidCoordinate as e:
            pass

    def __repr__(self) -> str:
        return f"{self.to_dataframe(True)}"

    def items(self):
        return self.__cells.items()

    def to_dataframe(self, value: bool = False) -> pd.DataFrame:
        """ Show in terminal the Spreadsheet with excel format"""
        data = {}
        for coord, cell in self.__cells.items():
            row, col = coord.row, coord.column
            if row not in data:
                data[row] = {}
            data[row][col] = cell.value if value else cell.content
        
        if not data:
            return pd.DataFrame()
        
        df = pd.DataFrame.from_dict(data, orient='index')
        df = df.reindex(sorted(df.columns), axis=1)  # Ordenar columnas
        
        df.columns = [Coordinate.number_to_letter(col) for col in df.columns]  # Ajustar col a base 1
        return df.fillna("")


if __name__ == "__main__":    
    sheet = Spreadsheet()
    '''
    sheet['F1'] = "=D2"            # Texto simple
    sheet['F2'] = "Mundo"          # Texto simple
    sheet['G1'] = "1"              # Número como cadena
    sheet['G2'] = "1.00.00"        # Número decimal como cadena
    sheet['C1'] = "=G1+10"         # Fórmula válida
    sheet['D1'] = ""               # Celda vacía
    sheet['D2'] = 100              # Número sin comillas
    sheet['F3'] = "5"

    #! Testing functions:
    sheet['C5'] = 1
    sheet['D5'] = "10"
    sheet['C6'] = "100"
    sheet['D6'] = 1000
    sheet['C7'] = "=C5+D5+C6+D6"
    
    sheet['C8'] = "=SUMA(C5:D6;D2;5;MIN(C5:D6;D2;5);1)"
    '''
    #! Testing circular_dependencies:
    sheet['E1'] = 20
    sheet['E1'] = "=E1"

    sheet['E2'] = "=E3"
    sheet['E3'] = "=E2"
    sheet['E4'] = "=E4"
    sheet['E5'] = 20

    
    sheet['A6'] = "1"
    sheet['A7'] = "2"
    sheet['A8'] = "3"
    sheet['A9'] = "4"
    sheet['A10'] = "5"
    sheet['A11'] = "6"
    sheet['A12'] = "7"
    sheet['A13'] = "8"
    sheet['A14'] = "9"
    sheet['A1'] = "=A2+A3+A4+A5"
    sheet['A2'] = "=A6+A7+A8"
    sheet['A3'] = "=A9+A10+A11"
    sheet['A4'] = "=A12+A13"
    sheet['A5'] = "=A14+1"

    sheet["A2"] = "=A1+A7+A8"
    sheet["A11"] = "=A2+A5"
    sheet["A11"] = "=A1+A5"
    sheet["A6"] = "=A1+A5"
    
    print(sheet)
        
    
        
        
        
        
    