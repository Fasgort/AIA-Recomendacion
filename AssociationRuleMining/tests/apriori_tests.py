import unittest

from apriori import generate_candidates, filter_candidates, apriori


class AprioriTestCase(unittest.TestCase):
    def setUp(self):
        self.t_db = [{1, 3, 4}, {2, 3, 5}, {1, 2, 3, 5}, {2, 5}]

    def test_generate_candidates_1(self):
        l_aux = ((1,), (2,), (3,), (4,), (5,))
        expected = ((1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5))
        l_set = set(frozenset(i) for i in l_aux)
        expected = set(frozenset(i) for i in expected)
        res = generate_candidates(l_set)
        self.assertEqual(expected, res)

    def test_generate_candidates_2(self):
        l_aux = ((1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5))
        expected = (
            (1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5), (1, 4, 5), (2, 3, 4), (2, 3, 5), (2, 4, 5),
            (3, 4, 5))
        l_set = set(frozenset(i) for i in l_aux)
        expected = set(frozenset(i) for i in expected)
        res = generate_candidates(l_set)
        self.assertEqual(expected, res)

    def test_generate_candidates_3(self):
        l_aux = (
            (1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5), (1, 4, 5), (2, 3, 4), (2, 3, 5), (2, 4, 5),
            (3, 4, 5))
        expected = ((1, 2, 3, 4), (1, 2, 3, 5), (1, 2, 4, 5), (1, 3, 4, 5), (2, 3, 4, 5))
        l_set = set(frozenset(i) for i in l_aux)
        expected = set(frozenset(i) for i in expected)
        res = generate_candidates(l_set)
        self.assertEqual(expected, res)

    def test_filter_candidates_1(self):
        l_aux = ((1,), (2,), (3,), (4,), (5,))
        expected = ((1,), (2,), (3,), (5,))
        l_set = set(frozenset(i) for i in l_aux)
        expected = set(frozenset(i) for i in expected)
        res = filter_candidates(l_set, self.t_db, 2)
        self.assertEqual(expected, res)

    def test_filter_candidates_2(self):
        l_aux = ((1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5), (3, 4), (3, 5), (4, 5))
        expected = ((1, 3), (2, 3), (2, 5), (3, 5))
        l_set = set(frozenset(i) for i in l_aux)
        expected = set(frozenset(i) for i in expected)
        res = filter_candidates(l_set, self.t_db, 2)
        self.assertEqual(expected, res)

    def test_filter_candidates_3(self):
        l_aux = (
            (1, 2, 3), (1, 2, 4), (1, 2, 5), (1, 3, 4), (1, 3, 5), (1, 4, 5), (2, 3, 4), (2, 3, 5), (2, 4, 5),
            (3, 4, 5))
        expected = ((2, 3, 5),)
        l_set = set(frozenset(i) for i in l_aux)
        expected = set(frozenset(i) for i in expected)
        res = filter_candidates(l_set, self.t_db, 2)
        self.assertEqual(expected, res)

    def test_filter_candidates_4(self):
        l_aux = ((1, 2, 3, 4), (1, 2, 3, 5), (1, 2, 4, 5), (1, 3, 4, 5), (2, 3, 4, 5))
        expected = frozenset()
        l_set = set(frozenset(i) for i in l_aux)
        res = filter_candidates(l_set, self.t_db, 2)
        self.assertEqual(expected, res)

    def test_apriori(self):
        l_aux = ((1,), (2,), (3,), (5,))
        exp1 = list(frozenset(i) for i in l_aux)
        l_aux = ((1, 3), (2, 3), (2, 5), (3, 5))
        exp2 = list(frozenset(i) for i in l_aux)
        l_aux = ((2, 3, 5),)
        exp3 = list(frozenset(i) for i in l_aux)
        expected = set()
        [expected.add(rule) for rule in exp1 + exp2 + exp3]
        res = apriori(self.t_db, 2/4)
        self.assertEqual(expected, res)


if __name__ == '__main__':
    unittest.main()
