import sys
from input import *
from algorithms import *

def main(argv):
	# very simple main... must be improved
	fileName = argv[1]
	f = open(argv[2], "r")
	items = [line.split(' ')[0] for line in f.readlines() if line]
	f.close()

	matrix = to01Matrix(items, transactionsFromFile(fileName))
	frequent_itemsets = ap_frequent_itemsets(matrix)
	#rules = ap_generate_rules(frequent_itemsets, frequent_itemsets[k])

if __name__ == '__main__':
	main(sys.argv)
