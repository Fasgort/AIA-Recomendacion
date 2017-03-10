import unittest

from association_rule_tools import get_support, get_confidence, get_lift, get_conviction, rule_extractor


class AssociationRuleToolsTestCase(unittest.TestCase):
    def setUp(self):
        self.t_db = [{1, 3, 4}, {2, 3, 5}, {1, 2, 3, 5}, {2, 5}]

    def test_get_support_list(self):
        rule = [1, 3]
        expected = 1 / 2
        res = get_support(rule, self.t_db)
        self.assertEqual(expected, res)

    def test_get_support_set(self):
        rule = set([1, 3])
        expected = 1 / 2
        res = get_support(rule, self.t_db)
        self.assertEqual(expected, res)

    def test_get_support_frozenset(self):
        rule = frozenset([1, 3])
        expected = 1 / 2
        res = get_support(rule, self.t_db)
        self.assertEqual(expected, res)

    def test_get_confidence_list(self):
        rule = [[1, 3], 5]
        expected = (1 / 4) / (2 / 4)
        res = get_confidence(rule, self.t_db)
        self.assertEqual(expected, res)

    def test_get_confidence_set(self):
        rule = [{1, 3}, {5, }]
        expected = (1 / 4) / (2 / 4)
        res = get_confidence(rule, self.t_db)
        self.assertEqual(expected, res)

    def test_get_confidence_2(self):
        rule = [{5, 2}, {3, }]
        expected = (2 / 4) / (3 / 4)
        res = get_confidence(rule, self.t_db)
        self.assertEqual(expected, res)

    def test_get_lift(self):
        rule = [{1, 3}, {5, }]
        expected = (1 / 4) / ((2 / 4) * (3 / 4))
        res = get_lift(rule, self.t_db)
        self.assertEqual(expected, res)

    def test_get_conviction(self):
        rule = [{1, 3}, {5, }]
        expected = (1 - (3 / 4)) / (1 - ((1 / 4) / (2 / 4)))
        res = get_conviction(rule, self.t_db)
        self.assertEqual(expected, res)

    def test_rule_extractor(self):
        l_aux = ((1,), (2,), (3,), (5,))
        exp1 = list(frozenset(i) for i in l_aux)
        l_aux = ((1, 3), (2, 3), (2, 5), (3, 5))
        exp2 = list(frozenset(i) for i in l_aux)
        l_aux = ((2, 3, 5),)
        exp3 = list(frozenset(i) for i in l_aux)
        freq_item_set = set()
        [freq_item_set.add(rule) for rule in exp1 + exp2 + exp3]
        expected = [
            [[3, 5], [2]],
            [[2, 3], [5]],
            [[5], [2]],
            [[2], [5]],
            [[1], [3]] ]
        res = rule_extractor(freq_item_set, 1, self.t_db)
        self.assertEqual(expected, res)


if __name__ == '__main__':
    unittest.main()
