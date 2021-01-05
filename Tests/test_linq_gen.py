import unittest
from pylinq.linq_gen import LinqGroupByGen, LinqGenerator

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

    def test_group_by_gen_simple(self):
        test_data = [('c', 1, 6.231), ('c', 1, 6.231), ('a', 1, 54.231), ('v', 6, 6.231)]

        gb_order_first_keys_counts = { 'c': 2, 'a': 1, 'v': 1 }
        gb_order_second_keys_counts = { 1 : 3, 6 : 1 }
        gb_order_third_keys_counts = { 6.231 : 3, 54.231 : 1 }

        gb_gen = LinqGroupByGen.new(test_data, lambda x : x[0])

        for key in gb_gen:
            self.assertTrue(key in gb_order_first_keys_counts)
            self.assertEqual(len(gb_gen[key]), gb_order_first_keys_counts[key])   


        gb_gen = LinqGroupByGen.new(test_data, lambda x : x[1])
        for key in gb_gen:
            self.assertTrue(key in gb_order_second_keys_counts)
            self.assertEqual(len(gb_gen[key]), gb_order_second_keys_counts[key])  


        gb_gen = LinqGroupByGen.new(test_data, lambda x : x[2])
        for key in gb_gen:
            self.assertTrue(key in gb_order_third_keys_counts)
            self.assertEqual(len(gb_gen[key]), gb_order_third_keys_counts[key])  


    def test_group_by_gen_chained(self):
        test_data = [('x', 1), ('x', 23), ('c', 34), ('c', 35), ('x', 24), ('a', 23), ('x', 1)]
        expected = { 
            'x' : ["Test 23", "Test 24"], 
            'c' : ["Test 34", "Test 35"], 
            'a' : ["Test 23"]
        }

        gen = LinqGenerator.new(test_data).where(lambda x : x[1] > 1).group_by(lambda x : x[0])
        for k in gen:
            tmp = gen[k].select(lambda x : "Test {}".format(x[1]))

            self.assertTrue(k in expected)
            for val in tmp:
                self.assertTrue(val in expected[k])

    def test_group_by_gen_count(self):
        test_data = [('x', 1), ('x', 23), ('c', 34), ('c', 35), ('x', 24), ('a', 23), ('x', 1)]
        expected = { 
            'x' : 2, 
            'c' : 2, 
            'a' : 1
        }

        gen = LinqGenerator.new(test_data).where(lambda x : x[1] > 1).group_by(lambda x : x[0])
        for k in gen:
            tmp = gen[k].select(lambda x : "Test {}".format(x[1]))

            self.assertTrue(k in expected)
            for val in tmp:
                self.assertEqual(expected[k], val.count())

    def test_group_by_gen_sum_int(self):
        test_data = [('x', 12), ('x', 23), ('c', 34), ('c', 35), ('x', 24), ('a', 23), ('x', 1)]
        expected = { 
            'x' : 12 + 23 + 24 + 1, 
            'c' : 34 + 35, 
            'a' : 23
        }

        gen = LinqGenerator.new(test_data).group_by(lambda x : x[0])
        for k in gen:
            self.assertTrue(k in expected)
            for val in gen[k]:
                self.assertEqual(expected[k], val.sum(lambda x : x[1]))

        

        