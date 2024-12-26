import sys
from pathlib import Path
from ..spreadsheet import Spreadsheet
from ..Data.coordinate import Coordinate

SEPARATOR = ";"

class FileSaver:
    def __init__(self) -> None:
        pass

    def _resolve_file_path(self, file_path: str) -> Path:
        """
        Resolves the file path relative to the entry script's directory.
        
        Args:
            file_path (str): The input file path
            
        Returns:
            Path: The resolved absolute Path object
        """
        entry_script_path = Path(sys.argv[0]).resolve()
        script_parent_dir = entry_script_path.parent
        
        file_path = Path(file_path)
        if not file_path.is_absolute():
            file_path = script_parent_dir / file_path
        
        return file_path

    def save(self, spreadsheet: Spreadsheet, file_path: str) -> None:
        """
        Saves the spreadsheet content to a file.
        
        Args:
            spreadsheet: The Spreadsheet object to save
            file_path: Path where to save the file
        """
        resolved_path = self._resolve_file_path(file_path)
        
        data = {}
        max_row = 0
        max_col = 0
        
        # Get max dimensions and store data
        for coord, cell in spreadsheet.items():
            max_row = max(max_row, coord.row)
            max_col = max(max_col, coord.column)
            
            if coord.row not in data:
                data[coord.row] = {}
            data[coord.row][coord.column] = cell.content_str.replace(';', ',') if cell.content_str else ''
        
        # Write to file
        with open(resolved_path, 'w') as file:
            for row in range(1, max_row + 1):
                row_data = []
                # Find the last column with content in this row
                last_col_with_content = 0
                for col in range(1, max_col + 1):
                    content = data.get(row, {}).get(col, '')
                    if content:  # If there's content, update last column
                        last_col_with_content = col
                    row_data.append(content)
                
                # Only include cells up to the last one with content
                if last_col_with_content > 0:
                    file.write(SEPARATOR.join(row_data[:last_col_with_content]) + '\n')
                else:
                    file.write('\n')  # Empty row
        
        if resolved_path.exists():
            print(f"Spreadsheet saved to {resolved_path.name}")
        else:
            print(f"Failed to save spreadsheet to {resolved_path.name}")