import sys
from input import *
from algorithms import *
import numpy


def print_help(argv):
	print '''
	TROLOLOGGER X9000 - HYPER EDITION v3.2
	
	Usage: %s [args]
	Example: %s data=./data.txt meta=./meta.txt t=0.2 c=0.3 
	
	You can either edit settings.py to handle algorithms variables or use 
	command line arguments (key=value). Command line arguments override  
	attribute values defined in settings.py in runtime. 
	
	General command line arguments are:
		data    : data filepath. One row per transaction, items separated by whitespaces.
		meta    : meta filepath. One row per meta_information. Informations are 
		          grouped together by id-column. 
		strip   : Only take account transactions that have more items than this.
		          This transaction stripping is done after any meta file spesific
		          restrictions take place.
		t       : Minimum support for itemsets considered frequent. ie. \'0.2\'
		c       : Minimum confidence of accepted rules. ie. \'0.1\' 
		closed  : Use closed itemsets. True/False 
		max     : Use maximal itemsets. True/False
	
	Meta file spesific arguments: 
		\'column=restriction\'
		column      : Column name as spesified in settings.py META_COLUMN_NAMES. 
		restriction : Restriction applied to this column. Only variables that  
		              pass all the restrictions are accepted as transaction items.
	 
		At the moment there are two types of restrictions:
		exact       : Take only those variables which have exactly this value in them.
		              ie. id=100.
		interval    : Take values which have values in the given interval. 
		              Interval is parsed by splitting the value from '-'. For 
		              example year=1999-2005 would yield closed interval [1999, 2005].
	''' % (argv[0], argv[0])
	

def validate_argv(argv):
	''' Validate that command line arguments are in right format. '''
	
	for x in range(1, len(argv)):
		arg = argv[x].split("=", 2)
		
		if arg[0] == 'help':
			print_help(argv)
			sys.exit(0)
			
		if len(arg) !=2:
			print "Argument \'%s\' in wrong format. Use \'key=value\'." % (arg[0])
			print "For more instructions try \'%s help\'" % (argv[0])
			sys.exit(0)

		
def main(argv):
	validate_argv(argv)
	# Read command line arguments to settings.
	read_argv(argv)
	
	print "\n"		
	# Read and transform data
	all_meta = read_meta_file()
	
	print "\n"
	pruned_meta = prune_variables(all_meta)
	print "%d variables after applying restrictions." % (len(pruned_meta))	
	
	fids = [var.fid for var in pruned_meta]
	matrix = to01Matrix(fids, transactionsFromFile(settings.DATA_FILE))
	
	stripped_rows = []
	for index, row in enumerate(matrix):
		if row.sum(0) > settings.STRIP:
			stripped_rows.append(index)
	
	matrix = matrix[stripped_rows,:]
	print "%d transactions after removing transactions with %d <= items \n" % (matrix.shape[0], settings.STRIP)

	# Calculate frequent itemsets and generate rules.
	frequent_itemsets = ap_frequent_itemsets(matrix, settings.FREQUENT_ITEMSET_THRESHOLD)
	res = []
	
	if settings.CLOSED_ITEMSETS:
		frequent_itemsets = ap_closed_frequent_itemsets(frequent_itemsets)
		print "\n *** Closed frequent item sets with minimum support %f **** \n" % (settings.FREQUENT_ITEMSET_THRESHOLD)
	elif settings.MAXIMAL_ITEMSETS:
		frequent_itemsets = ap_max_frequent_itemsets(frequent_itemsets)
		print "\n *** Maximal frequent item sets with minimum support %f **** \n" % (settings.FREQUENT_ITEMSET_THRESHOLD)
	else:
		print "\n *** Frequent item sets with minimum support %f **** \n" % (settings.FREQUENT_ITEMSET_THRESHOLD)
	
	for k in frequent_itemsets:
		for S in frequent_itemsets[k]:
			res.append( (S, frequent_itemsets[k][S].frequency) )
	res.sort(cmp=lambda a,b: -1 if a[1] < b[1] else 1 if a[1] > b[1] else 0)
	for S,f in res:
		print "%s (%f)" % (' '.join(["%d: %s" % (j, pruned_meta[j].name) for j in S]), f)


	#rule generation fails for closed/maximal sets due how frequency computation works.
	#should we generate rules for all frequent item sets only anyway?
	if not(settings.CLOSED_ITEMSETS or settings.MAXIMAL_ITEMSETS):
		print "\n *** Rules with minimum confidence %f **** \n" % (settings.RULE_MIN_CONFIDENCE)
		for k in xrange(2, len(frequent_itemsets)):	
			rules = ap_rule_generation(frequent_itemsets, k, settings.RULE_MIN_CONFIDENCE)
			for rule in rules:
				print "%s --> %s %f" % (" ".join([pruned_meta[i].name for i in rule[0]]), " ".join([pruned_meta[i].name for i in rule[1]]), rule[2])


	
if __name__ == '__main__':
	main(sys.argv)
	
	
	
