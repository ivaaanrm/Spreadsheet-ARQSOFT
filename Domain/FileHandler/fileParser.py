
import sys
from pathlib import Path
from ..spreadsheet import Spreadsheet
from ..Data.coordinate import Coordinate

SEPARATOR = ";"

class FileParser:
    def __init__(self) -> None:
        pass

    def __resolve_file_path(self, file_path: str) -> Path:
        # Get the directory of the script that was first executed
        entry_script_path = Path(sys.argv[0]).resolve()
        script_parent_dir = entry_script_path.parent

        # Resolve file_path relative to the entry script's parent directory
        file_path = Path(file_path)
        if not file_path.is_absolute():
            file_path = script_parent_dir / file_path

        return file_path

    def load(self, file_path: str) -> Spreadsheet:
        file_path = self.__resolve_file_path(file_path)

        # Assert the file exists
        assert file_path.exists(), FileNotFoundError(f"File {file_path} doesn't exist")
        
        with open(file_path, 'r') as file:
            lines = file.readlines()

        sheet = Spreadsheet()
        for row_idx, line in enumerate(lines):
            cells = line.strip().split(SEPARATOR)
            for col_idx, content in enumerate(cells):
                if content:
                    col = Coordinate.number_to_letter(col_idx+1)
                    coords = f"{col}{row_idx+1}"  # Convert to A1 notation
                    sheet[coords] = content.replace(",", ";")
        
        print(f"Spreadsheet loaded from {file_path.name}")
        return sheet