from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List, Dict
import re
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from PythonProjectAutomaticMarkerForGroupsOf2.SpreadsheetMarkerForStudents.entities.circular_dependency_exception import CircularDependencyException
from Exception.exceptions import InvalidFormula, CircularDependency
from Data.coordinate import Coordinate
from .tokenizer import Tokenizer, Token, TokenType, OperandType

if TYPE_CHECKING:
    from spreadsheet import Spreadsheet
    from Data.cell import Cell
    from Data.coordinate import Coordinate

class Function(ABC):
    """Abstract base class for function strategies"""
    @abstractmethod
    def evaluate(self, values: List[float]) -> float:
        pass

class Suma(Function):
    def evaluate(self, values: List[float]) -> float:
        return sum(values)

class Min(Function):
    def evaluate(self, values: List[float]) -> float:
        return min(values)

class Max(Function):
    def evaluate(self, values: List[float]) -> float:
        return max(values)

class Promedio(Function):
    def evaluate(self, values: List[float]) -> float:
        return sum(values) / len(values)

class FunctionContext:
    """Context class that manages function strategies"""
    _functions: Dict[str, Function] = {
        'SUMA': Suma(),
        'MIN': Min(),
        'MAX': Max(),
        'PROMEDIO': Promedio()
    }

    @classmethod
    def evaluate_function(cls, function_name: str, values: List[float]) -> float:
        strategy = cls._functions.get(function_name)
        if not strategy:
            raise InvalidFormula(f"Unknown function: {function_name}")
        return strategy.evaluate(values)

class FormulaController:
    def __init__(self, formula, cells_used):
        self.formula = formula
        self.__cells_used = cells_used
        self.__tokenizer = Tokenizer()

    def evaluate_formula(self, sheet: Spreadsheet, current_cell: Cell):
        if current_cell in self.__cells_used:
            raise CircularDependencyException(f'Circular dependency:{self.formula}')
        
        self.__cells_used.add(current_cell)
        arguments = self.get_tokens(self.formula)
        formula_expression = []
        
        for arg in arguments:
            
            if arg.operand_type == OperandType.CELL_REF:
                cell = sheet[arg.value]
        
                if cell.coordinate in self.__cells_used:
                    raise CircularDependencyException(f'Circular dependency:{self.formula}')
                
                value = cell.value if cell.content_str != '' else 0
                formula_expression.append(str(value))
            
            elif arg.operand_type == OperandType.FUNCTION:
                values = []
                function_name = arg.value[:arg.value.find('(')]
                try:
                    value = self.evaluate_function(function_name, arg.value, sheet, values)
                except Exception as e:
                    raise InvalidFormula(f"Invalid formula: {self.formula}")
                formula_expression.append(str(value))
                
            else:
                formula_expression.append(arg.value)
        
        try:
            formula_value = eval(''.join(formula_expression))
        except:
            raise InvalidFormula
        
        self.__cells_used.remove(current_cell)
        return formula_value
    
    def evaluate_function(self, fname: str, formula: str, sheet: Spreadsheet, values: List[float]) -> float:
        match = r"" + fname + r"\((.*)\)"
        if not match:
            raise InvalidFormula
    
        sequence = re.search(match, formula).group(1)
        arguments = []
        paren_count = 0
        start_idx = 0
        
        for i, char in enumerate(sequence):
            if char == '(':
                paren_count += 1
            elif char == ')':
                paren_count -= 1
            elif char == ';' and paren_count == 0:
                arguments.append(sequence[start_idx:i].strip())
                start_idx = i + 1
        
        arguments.append(sequence[start_idx:].strip())

        for arg in arguments:
            if '(' in arg:
                index = arg.find('(')
                fname2 = arg[:index]
                value = self.evaluate_function(fname2, arg, sheet, [])
                values.append(value)
            elif ':' in arg:
                range_coords = Coordinate.get_coordinates_in_range(arg)
                for coord in range_coords:
                    cell = sheet.get(coord)
                    value = float(cell.value) if cell.content_str != '' else 0
                    values.append(value)
            else:
                cell = sheet[arg]
                if cell is not None:
                    value = float(cell.value) if cell.content_str != '' else 0
                    values.append(value)
                else:
                    values.append(float(arg))

        return FunctionContext.evaluate_function(fname, values)

    def get_tokens(self, formula):
        return self.__tokenizer.tokenize(formula)