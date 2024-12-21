from enum import Enum
from typing import List, Optional
import re

class TokenType(Enum):
    OPERAND = "OPERAND"
    OPERATOR = "OPERATOR"
    
class OperandType(Enum):
    NUMBER = "NUMBER"
    CELL_REF = "CELL_REF"
    RANGE = "RANGE"
    FUNCTION = "FUNCTION"
    STRING = "STRING"

class Token:
    def __init__(self, value: str, token_type: TokenType, operand_type: Optional[OperandType] = None):
        self.value = value
        self.token_type = token_type
        self.operand_type = operand_type
    
    def __str__(self):
        if self.operand_type:
            return f"Token({self.value}, {self.token_type.value}, {self.operand_type.value})"
        return f"Token({self.value}, {self.token_type.value})"

class Tokenizer:
    OPERATORS = set(['+', '-', '*', '/', '^', '=', '>', '<', '>=', '<=', '<>', '&'])
    PARENTHESES = set(['(', ')'])
    
    def __init__(self):
        self.tokens = []
        self.current_pos = 0
        self.formula = ""
        
    def _is_cell_reference(self, value: str) -> bool:
        # Match patterns like A1, $A$1, AA123, etc.
        return bool(re.match(r'^\$?[A-Za-z]+\$?\d+$', value))
    
    def _is_range(self, value: str) -> bool:
        # Match patterns like A1:B2, $A$1:$B$2, etc.
        parts = value.split(':')
        return len(parts) == 2 and all(self._is_cell_reference(part) for part in parts)
    
    def _is_number(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def _is_function(self, value: str) -> bool:
        # Basic check for function names (can be expanded)
        common_functions = {'SUM', 'AVERAGE', 'COUNT', 'MAX', 'MIN', 'IF', 'VLOOKUP'}
        return value.upper() in common_functions
    
    def tokenize(self, formula: str) -> List[Token]:
        self.formula = formula.strip()
        self.current_pos = 0
        self.tokens = []
        
        while self.current_pos < len(self.formula):
            self._skip_whitespace()
            
            if self.current_pos >= len(self.formula):
                break
            
            char = self.formula[self.current_pos]
            
            if char in self.OPERATORS:
                self._handle_operator()
            elif char in self.PARENTHESES:
                self._handle_parenthesis()
            elif char == '"':
                self._handle_string()
            elif char.isalpha() or char == '$':
                self._handle_identifier()
            elif char.isdigit() or char == '.':
                self._handle_number()
            elif char == ',':
                self.tokens.append(Token(',', TokenType.OPERATOR))
                self.current_pos += 1
            else:
                raise ValueError(f"Invalid character in formula: {char}")
        
        return self.tokens
    
    def _skip_whitespace(self):
        while (self.current_pos < len(self.formula) and 
               self.formula[self.current_pos].isspace()):
            self.current_pos += 1
    
    def _handle_operator(self):
        # Handle multi-character operators
        if (self.current_pos + 1 < len(self.formula) and 
            self.formula[self.current_pos:self.current_pos + 2] in self.OPERATORS):
            operator = self.formula[self.current_pos:self.current_pos + 2]
            self.current_pos += 2
        else:
            operator = self.formula[self.current_pos]
            self.current_pos += 1
        
        self.tokens.append(Token(operator, TokenType.OPERATOR))
    
    def _handle_parenthesis(self):
        self.tokens.append(Token(self.formula[self.current_pos], TokenType.OPERATOR))
        self.current_pos += 1
    
    def _handle_string(self):
        start_pos = self.current_pos
        self.current_pos += 1  # Skip opening quote
        
        while (self.current_pos < len(self.formula) and 
               self.formula[self.current_pos] != '"'):
            self.current_pos += 1
        
        if self.current_pos >= len(self.formula):
            raise ValueError("Unterminated string literal")
        
        self.current_pos += 1  # Skip closing quote
        value = self.formula[start_pos:self.current_pos]
        self.tokens.append(Token(value, TokenType.OPERAND, OperandType.STRING))
    
    def _handle_identifier(self):
        start_pos = self.current_pos
        
        while (self.current_pos < len(self.formula) and 
               (self.formula[self.current_pos].isalnum() or 
                self.formula[self.current_pos] in '$:')):
            self.current_pos += 1
        
        value = self.formula[start_pos:self.current_pos]
        
        if self._is_range(value):
            token_type = OperandType.RANGE
        elif self._is_cell_reference(value):
            token_type = OperandType.CELL_REF
        elif self._is_function(value):
            token_type = OperandType.FUNCTION
        else:
            raise ValueError(f"Invalid identifier: {value}")
        
        self.tokens.append(Token(value, TokenType.OPERAND, token_type))
    
    def _handle_number(self):
        start_pos = self.current_pos
        
        while (self.current_pos < len(self.formula) and 
               (self.formula[self.current_pos].isdigit() or 
                self.formula[self.current_pos] == '.')):
            self.current_pos += 1
        
        value = self.formula[start_pos:self.current_pos]
        if not self._is_number(value):
            raise ValueError(f"Invalid number: {value}")
        
        self.tokens.append(Token(value, TokenType.OPERAND, OperandType.NUMBER))
        


if __name__ == "__main__":
    tokenizer = Tokenizer()
    formula = "=SUM(A1:B2)+42.5*C1"
    tokens = tokenizer.tokenize(formula)

    for token in tokens:
        print(token)