import unittest
from pathlib import Path

from pylinq.csv_linq import CsvLinq

class TestCsvLinqBasics(unittest.TestCase):

    def setUp(self):
        csv_path = Path(r"Tests\cities.csv")
        self.csv_file = open(csv_path, 'r').__enter__()
        self.csv = CsvLinq(self.csv_file)

    def tearDown(self):
        self.csv_file.__exit__()

    def test_file_found(self):
        self.assertIsNotNone(self.csv)

    def test_len_correct(self):
        self.assertEqual(128, len(self.csv))

    def test_indexer_zero(self):
        exp = ["41","5","59","N","80","39","0","W","Youngstown","OH"]
        act = self.csv[0]

        for idx, exp in enumerate(exp):
            self.assertEqual(exp, act[idx])
         
    def test_indexer_last(self):
        exp = ["41","9","35","N","81","14","23","W","Ravenna","OH" ]
        act = self.csv[len(self.csv) - 1]

        for idx, exp in enumerate(exp):
            self.assertEqual(exp, act[idx])

    def test_indexer_oor(self):
        with self.assertRaises(IndexError):
            _ = self.csv[130]