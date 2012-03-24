import sys
from input import *
from algorithms import *
import settings 
import numpy

def main(argv):
	# very simple main... must be improved
	arg_count = len(argv)
	
	if arg_count >= 2:
		settings.DATA_FILE = argv[1]
	
	if arg_count >= 3:
		settings.META_FILE = argv[2]
		
	if arg_count >= 4:
		settings.FREQUENT_ITEMSET_THRESHOLD = float(argv[3])
		
	if arg_count >= 5:
		settings.RULE_MIN_CONFIDENCE = float(argv[4])
			
	variables_meta = read_meta_file()
	fids = [var.fid for var in variables_meta]

	matrix = to01Matrix(fids, transactionsFromFile(settings.DATA_FILE))
	frequent_itemsets = ap_frequent_itemsets(matrix, settings.FREQUENT_ITEMSET_THRESHOLD)
	res = []
	for k in frequent_itemsets:
		for S in frequent_itemsets[k]:
			res.append( (S, frequent_itemsets[k][S].frequency) )
	res.sort(cmp=lambda a,b: -1 if a[1] < b[1] else 1 if a[1] > b[1] else 0)
	for S,f in res:
		print "%s (%f)" % (' '.join(["%s:%s" % (variables_meta[j].fid, variables_meta[j].name) for j in S]), f)
	
	for k in xrange(2, len(frequent_itemsets)):	
		rules = ap_rule_generation(frequent_itemsets, k, settings.RULE_MIN_CONFIDENCE)
		for rule in rules:
			print "%s --> %s %f" % (" ".join([variables_meta[i].name for i in rule[0]]), " ".join([variables_meta[i].name for i in rule[1]]), rule[2])

if __name__ == '__main__':
	main(sys.argv)
