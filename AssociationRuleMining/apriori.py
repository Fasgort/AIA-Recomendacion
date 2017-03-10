# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import logging


def apriori(transaction_db, min_support):
    """Returns a set of transactions of the given database
    whose frequency of occurrence is higher than the given.

    Implements apriori algorithm which is for frequent
    item set mining and association rule learning over
    transactional databases.

    :param transaction_db: set of transactions
    :param min_support: minimum occurrence ratio for returned sets
    over the database
    :return: set of frequent transactions
    """
    min_occurrence = min_support * len(transaction_db)
    logging.info("Start apriori algorithm")
    items_in_transaction_db = set()
    [items_in_transaction_db.update(s) for s in transaction_db]
    l_0 = set()
    for i in items_in_transaction_db:
        unitary_transaction = frozenset([i])
        occurrence = 0
        for t in transaction_db:
            if unitary_transaction.issubset(t):
                occurrence += 1
                if occurrence >= min_occurrence:
                    l_0.add(unitary_transaction)
                    break
    l_k = frozenset(l_0)
    level = 0
    logging.debug("Level {} rules extracted. Length={}".format(str(level), len(l_0)))
    res = set()
    while len(l_k) > 0:
        [res.add(rule) for rule in l_k]
        level += 1
        candidates = generate_candidates(l_k)
        logging.debug("Level {} candidates created. Length={}".format(str(level), len(candidates)))
        l_k = filter_candidates(candidates, transaction_db, min_occurrence)
        logging.debug("Level {} rules extracted. Length={}".format(str(level), len(l_k)))
    return res


def generate_candidates(parents_set):
    """Generates a set of sets of size k + 1
            such that all its subsets of size k are in L

            :param parents_set: set of k-size sets to create larger-size candidate children
            :return: set of candidates set
            """
    res = set()
    for l in parents_set:
        for s in parents_set:
            c = l.union(s)
            if len(l ^ s) == 2 and (max(l) in (l & c) and max(s) in (s & c)):
                res.add(c)
    return res


def filter_candidates(candidates, transaction_db, min_support):
    """Filtrates all candidates that not reach the minimum support required in the given transaction database

                :param candidates: set of k-size sets
                :param transaction_db: database of transactions
                :param min_support: minimum support to validate candidates
                :return: sub-set of candidates such that candidates have more support
                 in the transaction database than the required minimum
                """
    n = dict([(c, 0) for c in candidates])
    for t in transaction_db:
        for c in candidates:
            if c.issubset(t):
                n[c] += 1
    l = frozenset([c for c, support in n.items() if support >= min_support])
    return l


