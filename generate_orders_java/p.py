import os
import sys

def main(args):
    pairs_file = args[1]    # File with pairs of test,field
    tests_file = args[2]

    # Read the pairs into a mapping
    pair_mapping = {}
    with open(pairs_file) as f:
        for line in f:
            test = line.split(',')[0]
            field = line.split(',')[1].strip()
            if not test in pair_mapping:
                pair_mapping[test] = set()
            pair_mapping[test].add(field)

    # Combine tests as pairs and check whether they have common fields
    tests = sorted(pair_mapping.keys())
    pairs = set()
    tests_in_pairs = set()
    counter = 0
    for i in range(len(tests)):
        for j in range(i + 1, len(tests)):
            if pair_mapping[tests[i]] & pair_mapping[tests[j]] != set():
                pairs.add((tests[i], tests[j]))
                pairs.add((tests[j], tests[i]))
                tests_in_pairs.add(tests[i])
                tests_in_pairs.add(tests[j])

    with open(tests_file) as f2:
        for line in f2:
            counter += 1

    # Print some stats
    print (len(pairs) * 100 / (counter * (counter - 1)), len(tests_in_pairs) * 100 / counter, len(pairs), counter * (counter - 1), len(tests_in_pairs), counter)

if __name__ == '__main__':
    main(sys.argv)
