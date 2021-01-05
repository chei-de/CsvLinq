import unittest
from pylinq.linq_gen import LinqGenerator

class TestCsvLinqBasics(unittest.TestCase):

    def gen_data(self): 
        return [0,1,2,3,4,5,6,7,8,9,10]

    def test_bare_gen(self):
        actual = self.gen_data()
        for idx, v in enumerate(LinqGenerator.new(actual)):
            self.assertEqual(actual[idx], v)

    def test_filter_one(self):
        criterion = lambda x : x % 2 == 0
        actual = [x for x in self.gen_data() if criterion(x)]

        for idx, v in enumerate(LinqGenerator.new(actual).where(criterion)):
            self.assertEqual(actual[idx], v)

    def test_filter_two(self):
        criterion = lambda x : x > 5
        actual = [x for x in self.gen_data() if criterion(x)]

        for idx, v in enumerate(LinqGenerator.new(actual).where(criterion)):
            self.assertEqual(actual[idx], v)

    def test_filter_no_res(self):
        criterion = lambda x : x < 0
        actual = [x for x in self.gen_data() if criterion(x)]

        for idx, v in enumerate(LinqGenerator.new(actual).where(criterion)):
            self.assertEqual(actual[idx], v)

    def test_filter_transform_to_float(self):
        transform = lambda x : x + 0.5
        actual = self.gen_data()
        expected = [transform(x) for x in actual]

        for idx, v in enumerate(LinqGenerator.new(actual).select(transform)):
            self.assertEqual(expected[idx], v)

    def test_filter_transform_to_str(self):
        transform = lambda x : "Hallo {}".format(str(x))
        actual = self.gen_data()
        expected = [transform(x) for x in actual]

        for idx, v in enumerate(LinqGenerator.new(actual).select(transform)):
            self.assertEqual(expected[idx], v)

    def test_multi_statement(self):
        data = [1,2,3,4,5,6,7,8]
        expected = ["2p", "3p", "5p", "7p"]

        def is_prime(num):
            if num <= 1:
                return False

            if num == 2:
                return True

            if num % 2 == 0:
                return False

            for n in range(3, num, 2):
                if n * n > num:
                    break

                if num % n == 0:
                    return False

            return True

        for idx, v in enumerate(LinqGenerator.new(data).where(is_prime).select(lambda x : "{}p".format(x))):
            self.assertEqual(expected[idx], v)



        
        
