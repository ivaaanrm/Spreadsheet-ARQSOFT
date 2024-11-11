import sys
from pathlib import Path
import unittest
from rich import print

sys.path.append(str(Path(__file__).parent.parent))

from Domain.spreadsheet import Spreadsheet


class TestSpreadSheet(unittest.TestCase):
    
    def setUp(self):
        self.sheet = Spreadsheet()
    
    def test_create_spreadsheet(self):
        self.assertIsInstance(self.sheet, Spreadsheet)
    
    def test_set_value(self):
        self.sheet['a1'] = "Hola"
        self.assertEqual(self.sheet['a1'].contnet, "Hola")
    
    def test_update_value(self):
        self.sheet['a1'] = "Hola"
        self.assertEqual(self.sheet['a1'].contnet, "Hola")
        self.sheet['a1'] = "adios"
        self.assertEqual(self.sheet['a1'].contnet, "adios")


if __name__ == '__main__':
    unittest.main(verbosity=2)