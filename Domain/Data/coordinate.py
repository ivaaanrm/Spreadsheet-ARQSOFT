

import sys
from pathlib import Path
from dataclasses import field
from typing import Dict

sys.path.append(str(Path(__file__).parent.parent))

import re
from dataclasses import astuple, dataclass
from typing import Tuple


from Exception.exceptions import InvalidCoordinate

@dataclass(frozen=True)
class Coordinate:
    row: int
    column: int

    @staticmethod
    def from_string(coord: str) -> 'Coordinate':
        # Use a regular expression to separate the letters and numbers
        match = re.match(r"([A-Za-z]+)([0-9]+)", coord)
        if not match:
            raise InvalidCoordinate(f"Invalid cell coordinate format: {coord}")

        column_str, row_str = match.groups()
        
        # Convert the column letters (e.g., A, B, ..., Z, AA, AB, ...) to a 1-based index
        column = 0
        for char in column_str.upper():
            column = column * 26 + (ord(char) - ord('A') + 1)
        
        # Convert the row string to an integer
        row = int(row_str)
        
        return Coordinate(row=row, column=column)
    
    @staticmethod
    def number_to_letter(n: int) -> str:
        """Convierte un número en su equivalente en letras (estilo columnas de Excel)."""
        return "" if n <= 0 else Coordinate.number_to_letter((n - 1) // 26) + chr((n - 1) % 26 + 65)




if __name__ == "__main__":
    
    letter = Coordinate.number_to_letter(1)
    print(letter)