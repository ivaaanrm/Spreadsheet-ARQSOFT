from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from Exception.exceptions import InvalidFormula, CircularDependency

from .Formula.formula import FormulaController

if TYPE_CHECKING:
    from spreadsheet import Spreadsheet
    from Data.cell import Cell
    from Data.coordinate import Coordinate 

class Content(ABC):
    def __init__(self):
        self.sheet = None
        self.content: str = None
    
    @abstractmethod
    def get_value(self) -> str:
        """Return the value of the content."""
        pass
    
    def set_spreadsheet(self, sheet: Spreadsheet):
        self.sheet = sheet
        
    def set_current_cell(self, coordinate: Coordinate):
        self.current_cell = coordinate


class ContentFactory:
    """Factory class to create Content instances based on the input text."""
    @staticmethod
    def get_content_type(text: str) -> Content:
        if ContentFactory.is_formula_content(text):  # Formula content  "=SUM(A1:A10)"
            return FormulaContent(text) 
        elif ContentFactory.is_numerical_content(text):  # Numerical content "123.45"
            if '.' in text:
                return NumericalContent(float(text))
            else:
                return NumericalContent(int(text))
        return TextContent(text)
    
    @staticmethod
    def is_formula_content(text: str) -> bool:
        return text.startswith("=")
    
    @staticmethod
    def is_numerical_content(text: str) -> bool:
        return text.replace('.', '', 1).isdigit()
    

class TextContent(Content):
    def __init__(self, text: str):
        self.content = text

    def get_value(self) -> str:
        return self.content

    def __repr__(self):
        return f"TextContent({self.content})"


class NumericalContent(Content):
    def __init__(self, number: float):
        self.content = number

    def get_value(self) -> float:
        return self.content
        
    def __repr__(self):
        return f"NumericalContent({self.content})"


class FormulaContent(Content):
    def __init__(self, expression: str):
        self.content = expression
        self.__cells_used = set()
        self.__formula = FormulaController(self.content, self.__cells_used)

    def get_value(self) -> str:
        return self.__formula.evaluate_formula(self.sheet, self.current_cell)


    def __repr__(self):
        return f"FormulaContnent({self.content=})"