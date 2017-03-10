# -*- coding: utf-8 -*-
# !/usr/bin/env python3
import argparse
import logging
import os
import sys
import time

from apriori import apriori
from association_rule_tools import rule_extractor
from utils import load_transaction_db, association_rules_report

__date__ = '2017.03.08'

"""
AIA - T3 - Association rule mining
"""

_DATA_PATH = './data/retail.dat'


def main(args):
    logging.info("Association rules extraction")
    logging.debug("Verbose mode enabled")
    t0 = time.time()
    t_db_max_size = args.limit
    transaction_db = load_transaction_db('data/retail.dat', t_db_max_size)
    min_support = args.min_support
    freq_item_set = apriori(transaction_db, min_support)
    t1 = time.time()
    logging.info(
        "End. Frequent item set discovered count = {}\tElapsed time = {}".format(len(freq_item_set), str(t1 - t0)))
    # l=sorted([sorted(i) for i in rules])
    # l.sort(key = len)
    min_confidence = args.min_confidence
    rules = rule_extractor(freq_item_set, min_confidence, transaction_db)
    r_report = association_rules_report(rules, transaction_db)
    print(r_report)
    with open('out.txt', 'w') as fd:
        fd.write("Association rules extraction\n")
        fd.write("Transaction database size = {}\n".format(len(transaction_db)))
        fd.write("Minimum support accepted = {}\n".format(min_support))
        fd.write("Minimum confidence accepted = {}\n".format(min_confidence))
        fd.write("Apriori algorithm.\nFrequent sets discovered count = {}\tElapsed time = {}\n".format(len(rules),
                                                                                                       str(t1 - t0)))
        fd.write("Association rules discovered\n")
        fd.writelines(r_report)


def check_positive_limit(value):
    value = int(value)
    if value < 0:
        raise argparse.ArgumentTypeError("{} is an invalid limit int value".format(value))
    return value


def check_probability(value):
    value = float(value)
    if value < 0 or value > 1:
        raise argparse.ArgumentTypeError("{} is an invalid probability value".format(value))
    return value


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="AIA - T3 - Association rule mining")
    parser.add_argument(
        "-d",
        "--data",
        help="data path",
        default=_DATA_PATH, type=str)
    parser.add_argument(
        "-l",
        "--limit",
        help="load limit of transactions",
        default=0, type=check_positive_limit)
    parser.add_argument(
        "-s",
        "--min-support",
        help="minimum accepted support for frequent transaction set discover",
        default=0.01, type=check_probability)
    parser.add_argument(
        "-c",
        "--min-confidence",
        help="minimum accepted confidence for rule extraction",
        default=0.5, type=check_probability)
    parser.add_argument(
        "-v",
        "--verbose",
        help="increase output verbosity",
        action="store_true")
    args = parser.parse_args()
    if not os.path.exists(args.data):
        sys.exit("Data was no found at:{}".format(args.data))
    # Setup logging
    if args.verbose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=log_level)
    main(args)
