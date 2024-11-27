from abc import ABC, abstractmethod
from typing import Any

# from .Formula.tokenizer import Tokenizer
from openpyxl.formula.tokenizer import Tokenizer

class Content(ABC):
    @abstractmethod
    def get_value(self) -> Any:
        """Return the value of the content."""
        pass


class ContentFactory:
    """Factory class to create Content instances based on the input text."""
    @staticmethod
    def create_content(text: str) -> Content:
        if ContentFactory.is_formula_content(text):  # Formula content (e.g., "=SUM(A1:A10)")
            return FormulaContent(text)  # Remove the "=" for processing
        elif ContentFactory.is_numerical_conentn(text):  # Numerical content (e.g., "123.45")
            return NumericalContent(float(text))
        return TextContent(text)
    
    @staticmethod
    def is_formula_content(text: str) -> bool:
        return text.startswith("=")
    
    @staticmethod
    def is_numerical_conentn(text: str) -> bool:
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
        self.number = number

    def get_value(self) -> float:
        return self.number
    
    def __repr__(self):
        return f"NumericalContent({self.number})"


class FormulaContent(Content):
    def __init__(self, expression: str):
        self.expression = expression        
        self.tokenizer = Tokenizer(self.expression)

    def get_value(self) -> str:
        arguments = self.get_tokens()
        # Here, implement formula evaluation logic. Simplified as a string for now.
        return f"Computed{self.expression}"
    
    def compute_formula(self):
        pass
    
    def get_tokens(self):
        # TODO: Implementar aqui el Tokenizer nuestro
        return self.tokenizer.items
    
    def __repr__(self):
        return f"FormulaContnent({self.expression=})"