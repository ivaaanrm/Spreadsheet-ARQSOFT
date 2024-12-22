

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
    
    def set_cell(self, coords: str, content: str):
        try:
            coord = Coordinate.from_string(coords)
            self.__cells[coord] = Cell(coord, content, self)
        except InvalidCoordinate as e:
            pass

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

    def __repr__(self) -> str:
        return f"{self.to_dataframe(True)}"

    def items(self):
        return self.__cells.items()

if __name__ == "__main__":    
    sheet = Spreadsheet()
    
    sheet['A1'] = "=D2"            # Texto simple
    sheet['A2'] = "Mundo"          # Texto simple
    sheet['B1'] = "1"              # Número como cadena
    sheet['B2'] = "1.00.00"        # Número decimal como cadena
    sheet['C1'] = "=B1+10"         # Fórmula válida
    sheet['D1'] = ""               # Celda vacía
    sheet['D2'] = 100              # Número sin comillas
    sheet['F1'] = "=F1"
    sheet['A3'] = "5"
    sheet['F3'] = "=100/(A3+(A3*A3/5))"

    #! Testing functions:
    sheet['A5'] = 1
    sheet['B5'] = "10"
    sheet['A6'] = "100"
    sheet['B6'] = 1000
    sheet['C7'] = "=A5+B5+A6+B6"
    sheet['C8'] = "=SUMA(A5:B6;D2;5;MIN(A5:B6;D2;5);1)"
    
    # TODO: Esto no funciona todavía
    # sheet['E1'] = "=E2"           
    # sheet['E2'] = "=E1"            
    
    #print(sheet['A1'] == sheet['C1'])

    print(sheet)

        
    
        
        
        
        
    