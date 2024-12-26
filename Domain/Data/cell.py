from __future__ import annotations
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from spreadsheet import Spreadsheet 

from .content import ContentFactory
from .coordinate import Coordinate
from Domain.Exception.exceptions import InvalidFormula

class Cell:    
    def __init__(self, 
                 coords: Coordinate, 
                 text: str = "", 
                 sheet: Spreadsheet = None
                ) -> None:
        self.coordinate = coords
        self.content = ContentFactory.get_content_type(str(text))
        self.content.set_spreadsheet(sheet)
        self.content.set_current_cell(self.coordinate)
        # err = self.value
    
    @property
    def value(self) -> str:
        try:
            return self.content.get_value()
        except InvalidFormula as e:
            return e.ERROR_CODE
        except Exception as e:
            raise e
    
    @property
    def content_str(self) -> str:
        return str(self.content.content)

        