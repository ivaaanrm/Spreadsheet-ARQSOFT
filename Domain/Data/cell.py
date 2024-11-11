from dataclasses import dataclass, field


from .content import Content, TextContent


@dataclass
class Cell:
    contnet: Content = field(default="")
    
    @property
    def value(self):
        return self.contnet