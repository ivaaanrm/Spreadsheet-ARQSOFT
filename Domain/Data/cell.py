from dataclasses import dataclass, field


from .content import Content, TextContent, FormulaContent, NumericalContent

class ContentFactory:
    """Factory class to create Content instances based on the input text."""
    @staticmethod
    def create_content(text: str) -> Content:
        if text.startswith("="):  # Formula content (e.g., "=SUM(A1:A10)")
            return FormulaContent(text[1:])  # Remove the "=" for processing
        
        elif text.replace('.', '', 1).isdigit():  # Numerical content (e.g., "123.45")
            return NumericalContent(float(text))
        
        else:  # Default to text content
            return TextContent(text)
        
        
@dataclass
class Cell:
    content: Content = field(init=False)

    def __init__(self, text: str = ""):
        self.content = ContentFactory.create_content(text)
        
    @property
    def value(self):
        return self.content.get_value()

  
        
        