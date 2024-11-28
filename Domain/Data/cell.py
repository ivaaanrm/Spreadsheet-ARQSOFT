from __future__ import annotations
from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from spreadsheet import Spreadsheet 

from dataclasses import dataclass, field

from .content import Content, ContentFactory

@dataclass
class Cell:
    content: Content = field(init=False)
    
    def __init__(self, text: str = "", sheet: Spreadsheet = None) -> None:
        self.content = ContentFactory.get_content_type(str(text))
        self.content.set_spreadsheet(sheet)
    
    @property
    def value(self) -> str:
        return self.content.get_value()
    
    def __hash__(self):
        return hash(self.content)

  
        
        