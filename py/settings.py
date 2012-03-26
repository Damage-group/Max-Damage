'''
	Small config file to alter local run configurations.
	Some of the configurations can be altered when run.
'''
import os

# Settings for different file operations.
DATA_FILE =  os.path.join(os.path.dirname(__file__), 'courses_num.txt')
META_FILE =  os.path.join(os.path.dirname(__file__), 'courses_details.txt')

'''
	Meta file's column (ie. key) names.
	These should be in the order they are presented in file.
	
	Each column has key which is set as an attribute name for variable class's
	instance and information if only single (first) occurence of this key
	should be stored or set/multiset of all different values of the key. 
	Both set and multiset are stored in class as sequences. 
	
	Last element in tuple references to columns values. Possible values are
	'string', 'int' and 'float'. File reading tries to convert all the columns
	values to given type, but fails silently and does not convert values that
	raise ValueError with float(val) or int(val).
'''	
META_COLUMNS = [
	('FID', 'single', 'string'), 
	('NAME', 'single', 'string'),  
	('YEAR', 'set', 'int'),
	('TERM', 'set', 'string'),
	('LEVEL', 'single', 'string'),
	('COMPULSORY', 'single', 'string'),
	('CODE', 'single', 'string'),
	('SUBPROGRAM', 'single', 'string')	
]
# Don't use these columns.
OMIT_COLUMNS = ['TERM', 'CODE']
# Which column is used to link data file's objects to meta file.
# Should be 'single' valued column.
META_ID_COLUMN = 0

# Restrictions to variable meta information. Only variables
# which pass all the restrictions are counted into transactions.
VARIABLE_RESTRICTIONS = {}

# Strip transactions which have at most this many items. Transactions are 
# stripped before any variable restrictions take place.
STRIP = 0

# Settings for itemsets.
FREQUENT_ITEMSET_THRESHOLD = 0.1	# Minimum %-frequency of frequent itemsets.
CLOSED_ITEMSETS = False	# Use closed itemsets.
MAXIMAL_ITEMSETS =  False # Use maximal itemsets.

# Settings for rule generation.
RULE_MIN_CONFIDENCE = 0.1 	# Minimum confidence of accepted rules.
#Settings fro the measure method
Lift = True
IS = False
MutualInfo = False
CertaintyFactor = False

		
	






