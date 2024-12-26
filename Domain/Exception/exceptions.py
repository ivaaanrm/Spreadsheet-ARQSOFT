


class InvalidCoordinate(Exception):
    ERROR_CODE = "#COORD!"

class InvalidFormula(Exception):
    ERROR_CODE = "#NAME?"
    
class ZeroDivision(Exception):
    ERROR_CODE = "#DIVO?"
    
class CircularDependency(Exception):
    ERROR_CODE = "#REF!"