import sys
from input import *
from algorithms import *

def main(argv):
	# very simple main... must be improved
	fileName = argv[1]
	f = open(argv[2], "r")
	items = [line.split('\t')[0] for line in f.readlines() if line]
	f.close()

	matrix = to01Matrix(items, transactionsFromFile(fileName))
	frequent_itemsets = ap_frequent_itemsets(matrix, 0.10)
	res = []
	for k in frequent_itemsets:
		for S in frequent_itemsets[k]:
			res.append( (S, frequent_itemsets[k][S].frequency) )
	res.sort(cmp=lambda a,b: a[1] < b[1])
	for S,f in res:
		print "%s (%f)" % (' '.join([items[j] for j in S]), f)
	rules = ap_rule_generation(frequent_itemsets, 3, 0.2)
	for rule in rules:
		print rule

if __name__ == '__main__':
	main(sys.argv)
