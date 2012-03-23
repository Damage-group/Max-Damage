import sys
from input import *
from algorithms import *

def main(argv):
	# very simple main... must be improved
	fileName = argv[1] #transactions (courses-nums)
	f = open(argv[2], "r") #course details
	items = [line.split('\t')[0] for line in f.readlines() if line]
	f.close()
	
	threshold = 0
	confidence = 0
	
	if len(argv) >= 4:
		threshold = float(argv[3])
		
	if len(argv) >= 5:
		confidence = float(argv[4])

	matrix = to01Matrix(items, transactionsFromFile(fileName))
	frequent_itemsets = ap_frequent_itemsets(matrix, threshold)
	res = []
	for k in frequent_itemsets:
		for S in frequent_itemsets[k]:
			res.append( (S, frequent_itemsets[k][S].frequency) )
	res.sort(cmp=lambda a,b: -1 if a[1] < b[1] else 1 if a[1] > b[1] else 0)
	for S,f in res:
		print "%s (%f)" % (' '.join([items[j] for j in S]), f)
	
	for k in xrange(2, len(frequent_itemsets)):	
		rules = ap_rule_generation(frequent_itemsets, k, confidence)
		for rule in rules:
			print "%s --> %s %f" % (" ".join([str(i) for i in rule[0]]), " ".join([str(i) for i in rule[1]]), rule[2])

if __name__ == '__main__':
	main(sys.argv)
