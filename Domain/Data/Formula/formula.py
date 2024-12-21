from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from openpyxl.formula.tokenizer import Tokenizer as TokenizerOpenpyxl
from openpyxl.formula.tokenizer import Token as TokenOpenpyxl

from Exception.exceptions import InvalidFormula, CircularDependency

from .tokenizer import Tokenizer, Token

if TYPE_CHECKING:
    from spreadsheet import Spreadsheet
    from Data.cell import Cell
    from Data.coordinate import Coordinate 

class FormulaController:
    def __init__(self, formula, cells_used):
        self.formula = formula
        self.__cells_used = cells_used
        self.__tokenizer = TokenizerOpenpyxl(self.formula)
        #self.__tokenizer = Tokenizer(self.formula)

    def evaluate_formula(self, sheet: Spreadsheet, current_cell: Cell):
        self.__cells_used.add(current_cell)
        arguments = self.get_tokens()

        formula_expression = []
        
        for arg in arguments:
            cell = sheet[arg.value]
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
        return self.__tokenizer.items