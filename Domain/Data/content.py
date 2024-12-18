from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from openpyxl.formula.tokenizer import Tokenizer as TokenizerOpenpyxl
from openpyxl.formula.tokenizer import Token as TokenOpenpyxl

from .Formula.tokenizer import Tokenizer, Token
from Exception.exceptions import InvalidFormula, CircularDependency

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
        self.content = text

    def get_value(self) -> str:
        return self.content

    def __repr__(self):
        return f"TextContent({self.text})"


class NumericalContent(Content):
    def __init__(self, number: float):
        self.content = number

    def get_value(self) -> float:
        return self.content
        
    def __repr__(self):
        return f"NumericalContent({self.__number})"


class FormulaContent(Content):
    def __init__(self, expression: str):
        self.content = expression        
        self.__tokenizer_openpyxl = TokenizerOpenpyxl(self.content)
        self.__tokenizer = Tokenizer(self.content)
        self.__cells_used = set()

    def get_value(self) -> str:
        try:    
            return self.evaluate_formula()
            # TODO: Para la dependencia circular guardar en un set la celda con las coordenadas donde se ejecuta la formula
        except Exception as e:
            return e.ERROR_CODE
    
    def evaluate_formula(self):
        self.__cells_used.add(self.current_cell)
        arguments = self.get_tokens()

        formula_expression = []
        
        for arg in arguments:
            cell = self.sheet[arg.value]
            # TODO: iterar por cada operador y devolver el valor sin los condicionales
            if cell is not None:
                if cell.coordinate in self.__cells_used: 
                    raise CircularDependency
                
                formula_expression.append(str(cell.value))
            else:
                formula_expression.append(arg.value)
        
        try:
            formula_value = eval(''.join(formula_expression))
        except: 
            raise InvalidFormula
        
        return formula_value
                
    
    def get_tokens(self) -> List[TokenOpenpyxl]:
        # TODO: Implementar aqui el Tokenizer nuestro
        return self.__tokenizer_openpyxl.items
    
    def __repr__(self):
        return f"FormulaContnent({self.content=})"