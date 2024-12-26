from Domain.FileHandler.fileSaver import FileSaver
from Domain.FileHandler.fileParser import FileParser
from Domain.spreadsheet import Spreadsheet

class SpreadsheetController:
    def __init__(self):
        self.file_saver = FileSaver()
        self.file_loader = FileParser()
        self.sheet: Spreadsheet = None

    def new_spreadsheet(self) -> Spreadsheet:
        self.sheet = Spreadsheet()
        print("* Spreadhseet created!")

    def set_cell_content(self, coord: str, str_content: str) -> None:
        prev_contnet = self.get_cell_content_as_string(coord)
        self.sheet[coord] = str_content
        try:
            a = self.get_cell_content_as_float(coord)
        except Exception as e:
            self.sheet[coord] = prev_contnet
            raise e
    
    def get_cell_content_as_float(self, coord: str) -> float:
        return self.sheet[coord].value
        
    def get_cell_content_as_string(self, coord: str) -> str:
        return self.sheet[coord].content_str
    
    def get_cell_formula_expression(self, coord: str) -> str:
        return self.sheet[coord].content_str
        
    def save_spreadsheet_to_file(self, s_name_in_user_dir: str) -> None:
        self.file_saver.save(self.sheet, s_name_in_user_dir)
    
    def load_spreadsheet_from_file(self, s_name_in_user_dir: str) -> None:
        self.sheet = self.file_loader.load(s_name_in_user_dir)

