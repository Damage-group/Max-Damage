"""Implementations of algorithms."""

#!/usr/bin/env python

import numpy
import sys
import random
import itertools
#from blist import sortedlist

def first_item(iterable):
	"""Returns a first item of an iterable."""
	try:
		return iterable.__iter__().next()
	except StopIteration:
		return None

class FreqSet(dict):
	class Info(object):
		def __init__(self, frequency=0):
			self.frequency = frequency

	def __init__(self, iterable=None):
		dict.__init__(self)
		if iterable:
			for i in iterable:
				self[i] = FreqSet.Info()
	def append(self, X):
		self[X] = FreqSet.Info()
	add = append
	
'''
	Calculate frequency percentage in transactions for each k-itemset in
	itemsets.

	Params:
		itemsets	 - sequence of k-membered sets. Each member representing column.
		transactions - numpy.matrix from which the frequencies are
					   calculated from.

	Returns dictionary with k-itemsets as keys and frequencies as values.
'''
def calculate_frequencies(itemsets, transactions):
	if not itemsets: return	
	transactions_count = transactions.shape[0]
	# if itemsets are 1-itemsets:
	if len(itemsets.__iter__().next()) == 1:
		support = sum(transactions)
		for itemset in itemsets:
			itemsets[itemset].frequency = float(support[tuple(itemset)[0]]) / transactions_count
		return
	for itemset in itemsets:
		# Extract only itemset's columns from transactions
		set_as_list = list(itemset)
		cur_columns = transactions[:, set_as_list]
		current_freq = numpy.sum(sum(cur_columns.T) == len(set_as_list))
				
		# Store the percentage
		itemsets[itemset].frequency = float(current_freq) / float(transactions_count)	

'''
	Prune off itemsets' which have lower frequency than threshold.

	Params:
		itemsets	- set of itemset's to be pruned.
'''	
def prune_infrequent(itemsets, threshold = 0.5):
	for j in [i for i in itemsets if itemsets[i].frequency < threshold]:
		del itemsets[j]

''' (update this)	
	Generate k+1-itemsets from previous frequent itemsets.

	Params:
		frequent_itemsets - k-itemsets
		k - positive integer.

	Returns new k+1-itemsets which have all their subsets in frequent_itemsets[k].
'''
def generate_candidates(frequent_itemsets, k):
	
	if len(frequent_itemsets) == 0:
		return None

	candidates = FreqSet()
	
	#idea of a loop:
	#expects frequentitemsets to be lexicographically ordered. (1.itemsets souhld be ordered, the rest is ordered automatically)
	#example: ABCD, ABCE, ABCG --> prefix=ABC, items={D,E,G} when i=2,j=0
	#first_itemset = tuple(frequent_itemsets[k][0])
	#prefix = first_itemset[:-1]
	#items = set(first_itemset[-1])
	#for i in xrange(1,len(frequent_itemsets[k])):
	#	itemset = tuple(frequent_itemsets[k][i])
	#	if itemset[:-1] == prefix:
	#		items.add(itemset[-1])
	#	else:
	#		if len(items) >= 2:
	#			for item in items:
	#				candidate = prefix + item
	#				# handle candidate
	#		prefix = itemset[:-1]
	#		items = set()
	for set1, set2 in itertools.combinations(frequent_itemsets, 2):
		cur_set = set1.union(set2)
		
		# If sets union is k+1 then they have exatcly one different member.
		if len(cur_set) == k+1:
			# Test that all the subsets of the candidate are in
			#frequent_itemsets.
			accept = True
			for subset in set(itertools.combinations(cur_set, k)):
				if frozenset(subset) not in frequent_itemsets:
					accept = False
					break
			if accept: candidates.append(cur_set)
				
	return candidates

def ap_frequent_itemsets(transactions, minSupport=0.5):
	'''Apriori algorithm for frequent itemsets.
	Returns frequent itemsets in a dict where the key means that value contains list of k-itemsets.
	
	Params:
		transactions - a 0/1 matrix
		minSupport - minimum support value accepted
	'''

	# First create all 1-itemsets
	k = 1
	frequent_itemsets = {k : FreqSet()}
	for x in range(transactions.shape[1]):
		frequent_itemsets[k].append( frozenset( (x,) ) )
		
	calculate_frequencies(frequent_itemsets[k], transactions)
	prune_infrequent(frequent_itemsets[k], minSupport)

	# Then loop through the rest
	for k in range(2,100):
		candidates = generate_candidates(frequent_itemsets[k-1], k-1)
		if candidates is None:
			break
		calculate_frequencies(candidates, transactions)
		prune_infrequent(candidates, minSupport)
		frequent_itemsets[k] = candidates
	return frequent_itemsets

def ap_max_frequent_itemsets(freqset):
	keys = sorted(freqset, reverse=True)
	maxsets = freqset[keys[0]]

	for k in keys[1:]:
		newmaxsets = {}
		for s,info in freqset[k].items():
			for max_set in maxsets:
				if s.issubset(max_set):
					break
			else:
				newmaxsets[s] = info
		maxsets = dict(newmaxsets.items() + maxsets.items())
	
	#transform into a k:<FreqSet> dictionary structure
	return_dict = {}
	for s,info in maxsets.items():
		if not return_dict.has_key(len(s)):
			return_dict[len(s)] = FreqSet()
			
		return_dict[len(s)].append(s)
		return_dict[len(s)][s] = info

	return return_dict


def ap_closed_frequent_itemsets(freqset):
	keys = freqset.keys()
	closedsets = { keys[0]: freqset[keys[0]] }
	prev_k = keys[0]
	
	for k in keys[1:]:
		for s,info in freqset[k].items():
			for s2,info2 in closedsets[prev_k].items():
				if s2.issubset(s) and info.frequency == info2.frequency:
					del closedsets[prev_k][s2]
					
		closedsets[k] = freqset[k]
		prev_k = k
					
	return closedsets


def ap_rule_generation(frequent_itemsets, k, minConfidence):
	rules = []
	for itemset in frequent_itemsets[k]:
		ap_genrules(frequent_itemsets, rules, minConfidence, itemset, [frozenset( (A,) ) for A in itemset])
	rules.sort(cmp=lambda a,b: -1 if a[2] < b[2] else 1 if a[2] > b[2] else 0)
	return rules

def get_frequency(frequent_itemsets, itemset):
	return frequent_itemsets[len(itemset)][itemset].frequency

def ap_genrules(frequent_itemsets, rules, minConfidence, f, H):
	frequency = lambda itemset: get_frequency(frequent_itemsets, itemset)
	if not H: return

	k = len(f)
	m = len(first_item(H))

	toRemove = []
	for c in H:
		# for rule X -> Y - X: confidence = support(Y) / support(Y - X)
		# frequencies can be used because of the division operation.
		confidence = frequency(f) / frequency(f - c)
		if confidence >= minConfidence:
			rules.append( (f - c, c, confidence) )
		else:
			toRemove.append(c)
	for c in toRemove: del c
	if k > m+1:
		candidates = generate_candidates(H, k)
		ap_genrules(frequent_itemsets, rules, minConfidence, f, candidates)
