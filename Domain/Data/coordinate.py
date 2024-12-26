

import re
import sys

from pathlib import Path
from typing import List
from dataclasses import dataclass

sys.path.append(str(Path(__file__).parent.parent))

from Exception.exceptions import InvalidCoordinate


REGEX_PATTERN_CELL_RANGE = r"([A-Z]+)(\d+):([A-Z]+)(\d+)"

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

    @staticmethod
    def excel_col_to_index(col: str) -> int:
        """
        Convert an Excel column label (e.g., "A", "B", "AA") to a 1-based column index.
        """
        index = 0
        for char in col:
            index = index * 26 + (ord(char) - ord('A') + 1)
        return index

    @staticmethod
    def get_coordinates_in_range(range_str: str) -> List['Coordinate']:
        """
        Given a string representing a range in Excel notation (e.g., "A1:B2"),
        returns a list of Coordinate objects within the range.

        Args:
            range_str (str): The range in Excel notation (e.g., "A1:B2").

        Returns:
            List[Coordinate]: A list of Coordinate objects representing the range.
        """
        # Validate and parse the input string
        match = re.match(REGEX_PATTERN_CELL_RANGE, range_str.upper())
        if not match:
            raise ValueError(f"Invalid range format: {range_str}")
        
        col_start, row_start, col_end, row_end = match.groups()
        row_start, row_end = int(row_start), int(row_end)
        
        # Convert column letters to numeric indice
        col_start_idx = Coordinate.excel_col_to_index(col_start)
        col_end_idx = Coordinate.excel_col_to_index(col_end)
        
        # Normalize the range to ensure it's ordered
        col_start_idx, col_end_idx = sorted((col_start_idx, col_end_idx))
        row_start, row_end = sorted((row_start, row_end))
        
        # Generate all coordinates in the range
        return [
            Coordinate(row=row, column=col)
            for col in range(col_start_idx, col_end_idx + 1)
            for row in range(row_start, row_end + 1)
        ]


if __name__ == "__main__":
    
    ranges = [
        "A1:A5",
        "E2:A1",
        "A1:c3"
    ]
    
    for r in ranges:
        
        cells = Coordinate.get_coordinates_in_range(r)
        print(f"{r} -> {cells}\n")

