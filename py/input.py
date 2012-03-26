"""A place for data transfromation processes."""
import collections
import numpy
import settings
from variable import variable
import inspect
import sys

def readlines(fileName):
	return open(fileName, "r").readlines()

def splittedItemsets(iterable):
	"""A generator that splits lines to itemsets."""
	for item in iterable:
		yield [i.strip() for i in item.split()]

def transactionsFromFile(fileName):
	return splittedItemsets(readlines(fileName))

def to01Matrix(items, iterable):
	"""Generates 0/1 matrix.
	Parameters:
		rowCount - number of rows
		items - an iterable of the possible items
		iterable - an iterable containing transactions
	"""
	mapping = {}
	for i,col in enumerate(items):
		mapping[col] = i

	L = list(iterable) # read transactions to alist, because we need the number of transactions
	transactions = numpy.zeros((len(L), len(items)), dtype = int)
	
	for i,row in enumerate(L):
		for item in row:
			try:
				transactions[i][mapping[item]] = 1
			except KeyError: pass 

	return transactions

def convert(value, vtype = 'string'):
	
	if vtype == 'float':
		try: value = float(value)
		except: pass
	
	if vtype == 'int':
		try: value = int(value)
		except: pass
	
	return value


def register_restriction(key, value):
	
	for col in settings.META_COLUMNS:
		if str.lower(key) == str.lower(col[0]):
			values = value.split('-', 2)	
			if len(values) == 1:
				settings.VARIABLE_RESTRICTIONS[col[0]] = convert(values[0], col[2])
			else:
				start = convert(values[0], col[2])
				end = convert(values[1], col[2])			
				settings.VARIABLE_RESTRICTIONS[col[0]]= (start, end)
			return
		
	print "Unidentified meta column key %s." % (key)
	
def	read_argv(argv):

	attributes = {
		'data': 'DATA_FILE',
		'meta': 'META_FILE',
		'strip': 'STRIP',
		't' : 'FREQUENT_ITEMSET_THRESHOLD',
		'c' : 'RULE_MIN_CONFIDENCE',
		'closed' : 'CLOSED_ITEMSETS',	
		'max' : 'MAXIMAL_ITEMSETS',	
                'lift': 'Lift',
                'IS': 'IS',
                'MI': 'MutualInfo',
                'CF': 'CertaintyFactor'
		}
	
	for x in range(1, len(argv)):
		key, value = argv[x].split("=", 2)

		if key in ['strip', 'c', 't']:
			value = float(value)
			
		if key in ['closed', 'max']:
			if value.lower() == 'true':
				value = True
			else:
				value = False

		if key in attributes:
			settings.__dict__[attributes[key]] = value
		else: 
			register_restriction(key, value)			


def read_meta_file(filepath = None):
	""" Read data's meta information from file. 
	
		Method tries to be generic in the way that it reads what keys are 
		present in settings.META_COLUMNS and constructs instances of variable-
		class from those keys so that each key is set as an instance attribute.
	"""
	if filepath is None:
		filepath = settings.META_FILE
		
	f = None
	try:
		f = open(filepath, "r")
		print "Reading meta file at %s." % (filepath)
	except:
		print "%s could not open \"%s\" in %s" % (inspect.stack()[0][3], filepath, __file__)
		sys.exit(0)
		
	lines = f.readlines()
	col_info = settings.META_COLUMNS
	keys = [c[0] for c in col_info]
	id_col = settings.META_ID_COLUMN
	variables = dict()
	i = 0
	for l in lines:
		i += 1
		meta = l.split()
		if len(meta) < len(col_info):
			print "line %d: Too few variables in line. Expected at least %d, found %d." % (i, len(col_info), len(meta))
			print "Leaving line %d out." % (i)
			continue
		else:
			ID = meta[id_col]
			if ID not in variables:
				variables[ID] = dict()
			for x in range(0, len(col_info)):
				# Convert possible number values 
				value = convert(meta[x], col_info[x][2])

				if keys[x] not in settings.OMIT_COLUMNS:
					if not keys[x] in variables[ID]:
						variables[ID][keys[x]] = []
						variables[ID][keys[x]].append(value)
					else:
						if col_info[x][1] == 'set': 
							if value not in variables[ID][keys[x]]:
								variables[ID][keys[x]].append(value)
						elif col_info[x][1] == 'multiset': 
							variables[ID][keys[x]].append(value)
			
	variables_with_meta = []				
	for value in variables.values():
		current = variable(dictionary = value, id = keys[id_col])
		variables_with_meta.append(current)
		#print current
	
	print "File reading done. Found %d variables with meta information." % (len(variables_with_meta))
		
	return variables_with_meta

	
def prune_variables(variables = None):
	''' Remove variables that don't pass variable restrictions in settings.py '''
	
	to_remove = []
	for var in variables:
		for key, restriction in settings.VARIABLE_RESTRICTIONS.items():
			if not var.passes_restriction(restriction, key):
				if var.fid not in [v.fid for v in to_remove]:
					to_remove.append(var)

	pruned_variables = []
	for var in variables:
		if var.fid not in [v.fid for v in to_remove]:
			pruned_variables.append(var)

	return pruned_variables
	
							
if __name__ == "__main__":
	read_meta_file()
		
		
		
		
	
		
		
