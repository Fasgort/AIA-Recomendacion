import os
import unittest

import shutil

from utils import load_transaction_db, association_rules_report


class LoaderTestCase(unittest.TestCase):
    def setUp(self):
        self.db_filename = '../data/' + 'retail.dat'
        self.db_test = './data/test.dat'
        self.test_db = [{1, 3, 4}, {2, 3, 5}, {1, 2, 3, 5}, {2, 5}]
        if not os.path.exists('./data'):
            os.makedirs('./data')
        with open(self.db_test, 'w') as fd:
            for transaction in self.test_db:
                tran_str = ''
                for item in transaction:
                    tran_str += str(item) + ' '
                fd.writelines(tran_str + '\n')

    def tearDown(self):
        if os.path.exists(self.db_test):
            os.remove(self.db_test)
            # shutil.rmtree(self.db_test)

    def test_load_test_db(self):
        t_db = load_transaction_db(self.db_test)
        self.assertEqual(self.test_db, t_db)

    def test_load_production_db(self):
        t_db = load_transaction_db(self.db_filename)
        self.assertEqual(88162, len(t_db))


class OutputTestCase(unittest.TestCase):
    def setUp(self):
        self.t_db = [{1, 3, 4}, {2, 3, 5}, {1, 2, 3, 5}, {2, 5}]

    def test_print_association_rules(self):
        rule = ((1, 2),)
        association_rules_report(rule, self.t_db)

    def test_print_association_rules(self):
        rule = [
            [[3, 5], [2]],
            [[2], [5]],
            [[2, 3], [5]],
            [[5], [2]],
            [[1], [3]] ]
        report = association_rules_report(rule, self.t_db)
        print(report)


if __name__ == '__main__':
    unittest.main()
