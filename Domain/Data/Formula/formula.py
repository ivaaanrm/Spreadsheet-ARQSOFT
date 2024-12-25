from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List
import re
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from PythonProjectAutomaticMarkerForGroupsOf2.SpreadsheetMarkerForStudents.entities.circular_dependency_exception import CircularDependencyException

from Exception.exceptions import InvalidFormula, CircularDependency
from Data.coordinate import Coordinate

from .tokenizer import Tokenizer, Token

if TYPE_CHECKING:
    from spreadsheet import Spreadsheet
    from Data.cell import Cell
    from Data.coordinate import Coordinate 

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
            cell = sheet[arg.value]
            # TODO: iterar por cada operador y devolver el valor sin los condicionales
            if cell is not None:
                if cell.content.content == '':
                    cell.content.content = "0"

                if cell.coordinate in self.__cells_used:
                    raise CircularDependencyException
                formula_expression.append(str(cell.value))

            elif arg.value.startswith("SUMA"):
                values = []
                value = self.evaluate_function("SUMA", arg.value, sheet, values)
                formula_expression.append(str(value))
            elif arg.value.startswith("MIN"):
                values = []
                value = self.evaluate_function("MIN", arg.value, sheet, values)
                formula_expression.append(str(value))
            elif arg.value.startswith("MAX"):
                values = []
                value = self.evaluate_function("MAX", arg.value, sheet, values)
                formula_expression.append(str(value))
            elif arg.value.startswith("PROMEDIO"):
                values = []
                value = self.evaluate_function("PROMEDIO", arg.value, sheet, values)
                formula_expression.append(str(value))
            else:
                formula_expression.append(arg.value)
        
        try:
            formula_value = eval(''.join(formula_expression))
        except: 
            raise InvalidFormula
        
        self.__cells_used.remove(current_cell)
        
        return formula_value
    
    def evaluate_function(self, fname: str , formula: str, sheet: Spreadsheet, values):
        match = r"" + fname + "\((.*)\)"

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
                range = Coordinate.get_coordinates_in_range(arg)
                for coord in range:
                    column = Coordinate.number_to_letter(coord.column)
                    cell = column + str(coord.row)
                    values.append(sheet[cell].value)
            else:
                cell = sheet[arg]
                if cell is not None:
                    values.append(float(cell.value))
                else:
                    values.append(float(arg))

        if fname == 'SUMA':
            return sum(values)
        elif fname == 'MIN':
            return min(values)
        elif fname == 'MAX':
            return max(values)
        elif fname == 'PROMEDIO':
            return sum(values) / len(values)
    
    def get_tokens(self, formula):
        tokens = self.__tokenizer.tokenize(formula)
        return tokens