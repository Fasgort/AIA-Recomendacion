# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import logging

from tabulate import tabulate

from association_rule_tools import get_conviction, get_lift, get_confidence, get_support


def load_transaction_db(path, limit=0):
    logging.debug("Start loading transactions database")
    transaction_db = list()
    loaded = 0
    with open(path) as fd:
        for line in fd:
            transaction = frozenset([int(i_char) for i_char in line.split()])
            transaction_db.append(transaction)
            loaded += 1
            if 0 < limit <= loaded:
                break
    return transaction_db


def association_rules_report(rules, transaction_db):
    res = list()
    for r in rules:
        s = get_support((r[0]+r[1]), transaction_db)
        c = get_confidence(r, transaction_db)
        l = get_lift(r, transaction_db)
        conv = get_conviction(r, transaction_db)
        res.append(((sorted(r[0]),r[1]), s, c, l, conv))
    res = sorted(res, key=lambda x: (len(x[0][0]) * 100000000) + (x[0][0][0]), reverse=False)
    return tabulate(res, headers=['Rule X=>Y', 'Support', 'Confidence', 'Lift', 'Conviction'])


