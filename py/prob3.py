import sys
from input import *
from algorithms import *
from measures import *
import numpy
import cProfile
import sequences


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
                lift    : use lift(interest factor) to qualify the rule
                IS      : use IS measure to qualify the rule
                MI      : output the mutual information of the rule 
                CF      : output the certainty factor of the rule

	
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


def seq2str(seq, meta_dict):
	str = ""
	for e in seq:
		str += "("
		for elem in e:
			course = meta_dict["%s" % elem]
			str += "%s:%s " % (elem, course.name)
		str += ")"
	return str
		
def main(argv):
	validate_argv(argv)
	# Read command line arguments to settings.
	read_argv(argv)
	
	print "\n"		
	# Read and transform data
	all_meta = read_meta_file()
	meta_dict = {}
	meta = prune_variables(all_meta)
	
	for a in meta:
		meta_dict[a.fid] = a
	
	print "\n"
	
	transactions = list(transactionsFromFile(settings.DATA_FILE, meta_dict))
	
	seqs = []
	for t in transactions:
		if len(t[0]) > settings.STRIP:
			seqs.append(t)
	
	print "%d transactions after applying restrictions. \n" % len(seqs)
	
	results = sequences.frequent_sequences(seqs)
	seq = results[0]
	f = results[1]
	
	for s in seq[1:-1]:
		for sequence in s:
			str = seq2str(sequence, meta_dict)
			str += ": %s" % (f[sequence])	
			print str
			
	print "Generated rules are:"
	
	rules = sequences.seq_genrules(seq, settings.FREQUENT_SEQUENCE_THRESHOLD, seqs)
	
	for r in rules:
		print "%s -> %s: %s" % (seq2str(r[0], meta_dict), seq2str(r[1], meta_dict), r[2])
					

	

if __name__ == '__main__':
	main(sys.argv)
	
	