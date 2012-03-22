"""A place for data transfromation processes."""
import numpy

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
