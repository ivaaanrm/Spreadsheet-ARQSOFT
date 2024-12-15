
from pathlib import Path
from ..spreadsheet import Spreadsheet
from ..Data.coordinate import Coordinate

SEPARATOR = ";"

class FileParser:
    def __init__(self) -> None:
        pass
    def load(self, file_path: str):
        if not Path(file_path).exists():
            raise FileNotFoundError
        
        with open(file_path, 'r') as file:
            lines = file.readlines()

        sheet = Spreadsheet()
        for row_idx, line in enumerate(lines, start=1):
            cells = line.strip().split(SEPARATOR)
            for col_idx, content in enumerate(cells):
                if content:
                    col = Coordinate.number_to_letter(col_idx)
                    coords = f"{col}{row_idx}"  # Convert to A1 notation
                    sheet[coords] = content
        
        return sheet