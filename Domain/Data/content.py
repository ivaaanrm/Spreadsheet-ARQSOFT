

from dataclasses import dataclass
from abc import ABC, abstractmethod


class Content(ABC):
    
    @abstractmethod
    def get_value():
        pass
    


class TextContent(Content):
    
    def get_value():
        pass