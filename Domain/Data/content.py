from __future__ import annotations
import sys
from abc import ABC, abstractmethod
from typing import Any, TYPE_CHECKING, List
from pathlib import Path

# from .Formula.tokenizer import Tokenizer
from openpyxl.formula.tokenizer import Tokenizer, Token
from Exception.exceptions import InvalidFormula, CircularDependency

if TYPE_CHECKING:
    from spreadsheet import Spreadsheet
    from Data.cell import Cell
    from Data.coordinate import Coordinate 

class Content(ABC):
    def __init__(self):
        self.sheet = None
    
    @abstractmethod
    def get_value(self) -> str:
        """Return the value of the content."""
        pass
    
    def set_spreadsheet(self, sheet: Spreadsheet):
        self.sheet = sheet


class ContentFactory:
    """Factory class to create Content instances based on the input text."""
    @staticmethod
    def get_content_type(text: str) -> Content:
        if ContentFactory.is_formula_content(text):  # Formula content (e.g., "=SUM(A1:A10)")
            return FormulaContent(text) 
        elif ContentFactory.is_numerical_content(text):  # Numerical content (e.g., "123.45")
            return NumericalContent(float(text))
        return TextContent(text)
    
    @staticmethod
    def is_formula_content(text: str) -> bool:
        return text.startswith("=")
    
    @staticmethod
    def is_numerical_content(text: str) -> bool:
        return text.replace('.', '', 1).isdigit()
    

class TextContent(Content):
    def __init__(self, text: str):
        self.text = text

    def get_value(self) -> str:
        return self.text

    
    def __repr__(self):
        return f"TextContent({self.text})"


class NumericalContent(Content):
    def __init__(self, number: float):
        self.__number = number

    def get_value(self) -> float:
        return self.__number
    
    def __repr__(self):
        return f"NumericalContent({self.__number})"


class FormulaContent(Content):
    def __init__(self, expression: str):
        self.__expression = expression        
        self.__tokenizer = Tokenizer(self.__expression)
        self.__cells_used = set()

    def get_value(self) -> str:
        try:    
            return self.evaluate_formula()
            # TODO: Para la dependencia circular guardar en un set la celda con las coordenadas donde se ejecuta la formula
        except Exception as e:
            return e.ERROR_CODE
    
    def evaluate_formula(self):
        arguments = self.get_tokens()
        
        formula_expression = []
        
        for arg in arguments:
            cell = self.sheet[arg.value]
      
            # TODO: iterar por cada operador y devolver el valor sin los condicionales
            if cell is not None:
                formula_expression.append(str(cell.value))
            else:
                formula_expression.append(arg.value)
        
        try:
            formula_value = eval(''.join(formula_expression))
        except: 
            raise InvalidFormula
        
        return formula_value
                
    
    def get_tokens(self) -> List[Token]:
        # TODO: Implementar aqui el Tokenizer nuestro
        return self.__tokenizer.items
    
    def __repr__(self):
        return f"FormulaContnent({self.__expression=})"