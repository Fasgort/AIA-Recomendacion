Association rule mining using Apriori algorithm for frequent association rule extraction.

Execute:
    python main.py

Options:
    -h  Show help message
    -d  Path where data is located
    -s  Minimum support to discover frequent item set
    -c  Minimum confidence to extract association rules
    -v  Enable verbose mode

Note:
    Defaults:
        -d ./data/retail.dat
        -s 0.01
        -c 0.5

Requirements:
    # Python 3.6
    numpy==1.12.0
    tabulate==0.7.7
    pyparsing==2.1.10

