

from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Any

class Content(ABC):
    @abstractmethod
    def get_value(self) -> Any:
        """Return the value of the content."""
        pass


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

    def get_value(self) -> str:
        # Here, implement formula evaluation logic. Simplified as a string for now.
        return f"Compute({self.expression})"
    
    def __repr__(self):
        return f"FormulaContnent({self.expression=})"