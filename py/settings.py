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
'''	
META_COLUMNS = [
	('FID', 'single'), 
	('NAME', 'single'),  
	('YEAR', 'set'),
	('TERM', 'set'),
	('LEVEL', 'single'),
	('COMPULSORY', 'single'),
	('CODE', 'single'),
	('SUBPROGRAM', 'single')	
]
# Don't use these columns.
OMIT_COLUMNS = ['TERM', 'CODE']
# Which column is used to link data file's objects to meta file.
# Should be 'single' valued column.
META_ID_COLUMN = 0

# Settings for itemsets.
FREQUENT_ITEMSET_THRESHOLD = 0.5	# Minimum %-frequency of frequent itemsets.
CLOSED_ITEMSETS = False	# Use closed itemsets.
MAXIMAL_ITEMSETS =  False # Use maximal itemsets.

# Settings for rule generation.
RULE_MIN_CONFIDENCE = 0.2 	# Minimum confidence of accepted rules.




