"""A place for data transfromation processes."""
import numpy
from settings import *
from variable import variable
import inspect
import sys
import string

def readlines(fileName):
	return open(fileName, "r").readlines()

def splittedItemsets(iterable):
	"""A generator that splits lines to itemsets."""
	for item in iterable:
		yield [i.strip() for i in item.split(' ')]

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

def read_meta_file(filepath = None):
	""" Read data's meta information from file. 
	
		Method tries to be generic in the way that it reads what keys are 
		present in settings.META_COLUMNS and constructs instances of variable-
		class from those keys so that each key is set as an instance attribute.
	"""
	if filepath is None:
		filepath = META_FILE
		
	f = None
	try:
		f = open(filepath, "r")
		print "Reading meta file at %s." % (filepath)
	except:
		print "%s could not open \"%s\" in %s" % (inspect.stack()[0][3], filepath, __file__)
		sys.exit(0)
		
	lines = f.readlines()
	columns = META_COLUMNS
	keys = [c[0] for c in columns]
	variables = dict()
	i = 0
	for l in lines:
		i += 1
		meta = l.split()
		if len(meta) < len(columns):
			print "line %d: Too few variables in line. Expected at least %d, found %d." % (i, len(columns), len(meta))
			print "Leaving line %d out." % (i)
			continue
		else:
			ID = meta[META_ID_COLUMN]
			if ID not in variables:
				variables[ID] = dict()
			for x in range(0, len(columns)):
				if keys[x] not in OMIT_COLUMNS:
					if not keys[x] in variables[ID]:
						variables[ID][keys[x]] = []
						variables[ID][keys[x]].append(meta[x])
					else:
						if columns[x][1] == 'set': 
							if meta[x] not in variables[ID][keys[x]]:
								variables[ID][keys[x]].append(meta[x])
						elif columns[x][1] == 'multiset': 
							variables[ID][keys[x]].append(meta[x])
			
	variables_with_meta = []				
	for value in variables.values():
		current = variable(dictionary = value, id = keys[META_ID_COLUMN])
		print current
		variables_with_meta.append(variable)
		
		
	
	
				
#	for key, value in variables.items():
#		print "---- %s ----" % key
#		for k, v in value.items():
#			print "%s = %s" % (k, v)
					
if __name__ == "__main__":
	read_meta_file()
		
		
		
		
	
		
		