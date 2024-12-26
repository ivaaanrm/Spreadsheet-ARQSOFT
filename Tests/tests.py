import sys
import unittest
from rich import print
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from Domain.Data.content import FormulaContent
from Domain.spreadsheet import Spreadsheet
from Domain.Data.cell import Cell
# from Domain.Data.content import NumericalContent, FormulaContent, TextContent


class TestSpreadSheet(unittest.TestCase):
    
    def setUp(self):
        self.sheet = Spreadsheet()
    
    def test_create_spreadsheet(self):
        print(type(self.sheet))
        self.assertIsInstance(self.sheet, Spreadsheet)
    
    def test_set_value(self):
        self.sheet['a1'] = "Hola"
        self.assertEqual(self.sheet['a1'].value, "Hola")
    
    def test_update_value(self):
        self.sheet['a1'] = "Hola"
        self.assertEqual(self.sheet['a1'].value, "Hola")
        self.sheet['a1'] = "adios"
        self.assertEqual(self.sheet['a1'].value, "adios")
    
    def test_tokenizer(self):
        self.sheet['a1'] = "=1+1"
        self.sheet['a1'].content.get_value()
        
    # def test_formula_content(self):
    #     self.sheet['a1'] = "=1+1"
        
    #     print(type(self.sheet['a1'].content))
    #     self.assertIsInstance(self.sheet['a1'].content, FormulaContent)

if __name__ == '__main__':
    unittest.main(verbosity=2)