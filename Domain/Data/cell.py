from __future__ import annotations
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from spreadsheet import Spreadsheet 

from dataclasses import dataclass, field

from .content import ContentFactory
from .coordinate import Coordinate

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
        
    
    @property
    def value(self) -> str:
        return self.content.get_value()
    
    def __hash__(self):
        return hash(self.content)    
    
    def __eq__(self, cell: Cell):
        return self.value == cell.value