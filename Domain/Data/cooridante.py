

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
    def from_string(cell_name: str) -> 'Coordinate':
        # Use a regular expression to separate the letters and numbers
        match = re.match(r"([A-Za-z]+)([0-9]+)", cell_name)
        if not match:
            raise InvalidCoordinate(f"Invalid cell coordinate format: {cell_name}")

        column_str, row_str = match.groups()
        
        # Convert the column letters (e.g., A, B, ..., Z, AA, AB, ...) to a 1-based index
        column = 0
        for char in column_str.upper():
            column = column * 26 + (ord(char) - ord('A') + 1)
        
        # Convert the row string to an integer
        row = int(row_str)
        
        return Coordinate(row=row, column=column)

