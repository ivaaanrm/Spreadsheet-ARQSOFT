from dataclasses import dataclass, field


from .content import Content, ContentFactory

        
@dataclass
class Cell:
    content: Content = field(init=False)
    
    def __init__(self, text: str = ""):
        self.content = ContentFactory.create_content(str(text))
    
    @property
    def value(self):
        return self.content.get_value()

  
        
        