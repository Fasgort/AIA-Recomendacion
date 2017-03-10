import logging


def get_support(item_set, transaction_db):
    logging.debug("Calculating item set support: {}".format(item_set))
    if type(item_set) in [set, frozenset]:
        r = item_set
    else:
        r = frozenset(item_set)
    return len([1 for s in transaction_db if r.issubset(s)]) / len(transaction_db)


def get_confidence(rule, transaction_db):
    logging.debug("Calculating rule confidence: {}".format(rule))
    if type(rule) in [list, tuple, set, frozenset] and len(rule) == 2:
        antecedent_set = list(rule[0]) if type(rule[0]) in [list, tuple, set, frozenset] else [rule[0], ]
        consequent_set = list(rule[1]) if type(rule[1]) in [list, tuple, set, frozenset] else [rule[1], ]
    else:
        logging.error("Invalid rule given to get confidence: {}".format(rule))
        return 0
    s = get_support(set(antecedent_set + consequent_set), transaction_db)
    antecedent_s = get_support(set(antecedent_set), transaction_db)
    return s / antecedent_s


def get_lift(rule, transaction_db):
    logging.debug("Calculating rule lift: {}".format(rule))
    if type(rule) in [list, tuple, set, frozenset] and len(rule) == 2:
        antecedent_set = list(rule[0]) if type(rule[0]) in [list, tuple, set, frozenset] else [rule[0], ]
        consequent_set = list(rule[1]) if type(rule[1]) in [list, tuple, set, frozenset] else [rule[1], ]
    else:
        logging.error("Invalid rule given to get lift: {}".format(rule))
        return 0
    s = get_support(set(antecedent_set + consequent_set), transaction_db)
    antecedent_s = get_support(set(antecedent_set), transaction_db)
    consequent_s = get_support(set(consequent_set), transaction_db)
    return s / (antecedent_s * consequent_s)


def get_conviction(rule, transaction_db):
    logging.debug("Calculating rule conviction: {}".format(rule))
    if type(rule) in [list, tuple, set, frozenset] and len(rule) == 2:
        consequent_set = list(rule[1]) if type(rule[1]) in [list, tuple, set, frozenset] else [rule[1], ]
    else:
        logging.error("Invalid rule given to get conviction: {}".format(rule))
        return 0
    confidence = get_confidence(rule, transaction_db)
    consequent_s = get_support(set(consequent_set), transaction_db)
    if confidence == 1:
        return 0
    else:
        return (1 - consequent_s) / (1 - confidence)


def rule_extractor(frequent_sets, min_confidence, transaction_db):
    logging.info("Start rule extractor. Minimum confidence: {}".format(min_confidence))
    rules = list()
    for item_set in frequent_sets:
        if len(item_set) > 1:
            for consequent in item_set:
                antecedent = list(item_set)
                antecedent.remove(consequent)
                rule_aux = [antecedent, [consequent]]
                confidence = get_confidence(rule_aux, transaction_db)
                if confidence >= min_confidence:
                    rules.append(rule_aux)
    return rules
