import unittest
from pathlib import Path

from pylinq.csv_linq import CsvLinq
import pylinq.csv_linq_cell_trims as trims

class TestCsvLinqTrims(unittest.TestCase):

    def setUp(self):
        self.csv_file = open(r"Tests\cities.csv", 'r').__enter__()

    def tearDown(self):
        self.csv_file.__exit__()

    def test_identity_trim(self):
        csv = CsvLinq(self.csv_file, trims.Identity())

        exp = ["   41","    5","   59",' "N"',"     80","   39","    0",' "W"',' "Youngstown"',' OH']
        act = csv[0]

        for i, e in enumerate(exp):
            self.assertEqual(e, act[i])


    def test_removal_trim(self):
        csv = CsvLinq(self.csv_file, trims.StripWhitespaces(), trims.RemoveChars('"', "Y"))

        exp = ["41","5","59","N","80","39","0","W","oungstown","OH"]
        act = csv[0]

        for i, e in enumerate(exp):
            self.assertEqual(e, act[i])