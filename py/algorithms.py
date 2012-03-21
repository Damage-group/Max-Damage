"""Implementations of algorithms."""

#!/usr/bin/env python

import numpy
import sys
import random
import itertools
from blist import sortedlist

'''
    Calculate frequency percentage in transactions for each k-itemset in 
    itemsets.

    Params:
        itemsets     - sequence of k-membered sets. Each member representing column.
        transactions - numpy.matrix from which the frequencies are 
                       calculated from.

    Returns dictionary with k-itemsets as keys and frequencies as values.
'''
def calculate_frequencies(itemsets, transactions):
    
    transactions_count = transactions.shape[0] 
    
    for itemset in itemsets:
        # Extract only itemset's columns from transactions
        set_as_list = list(itemset)
        cur_columns = transactions[:, set_as_list]
        current_freq = 0
        for row in cur_columns:
            # If all columns in cur_columns are "true" add one into 
            # frequency counting.
            if row.all():
                current_freq = current_freq + 1
                
        # Store the percentage
        itemset.frequency = float(current_freq) / float(transactions_count)    

'''
    Prune off itemsets' which have lower frequency than threshold.

    Params:
        itemsets    - set of itemset's to be pruned.
'''      
def prune_infrequent(itemsets, threshold = 0.5):  
    # iterates from end to begin:
    i = 0
    while i < len(itemsets):
    	if itemsets[i].frequency < threshold:
    		del itemsets[i]
    	else:
    		i = i + 1

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

    candidates = sortedlist()
    
    #idea of a loop:
    #expects frequentitemsets to be lexicographically ordered. (1.itemsets souhld be ordered, the rest is ordered automatically)
    #example: ABCD, ABCE, ABCG --> prefix=ABC, items={D,E,G} when i=2,j=0
    #first_itemset = tuple(frequent_itemsets[k][0])
    #prefix = first_itemset[:-1]
    #items = set(first_itemset[-1])
    #for i in xrange(1,len(frequent_itemsets[k])):
    #    itemset = tuple(frequent_itemsets[k][i])
    #    if itemset[:-1] == prefix:
    #        items.add(itemset[-1])
    #    else:
    #        if len(items) >= 2:
    #            for item in items:
    #                candidate = prefix + item
    #                # handle candidate
    #        prefix = itemset[:-1]
    #        items = set()
    for set1, set2 in itertools.combinations(frequent_itemsets, 2):
        cur_set = set1.union(set2)
        
        # If sets union is k+1 then they have exatcly one different member.
        if len(cur_set) == k+1:
            # Test that all the subsets of the candidate are in 
            #frequent_itemsets.
            for subset in set(itertools.combinations(cur_set, k)):
                if subset not in frequent_itemsets:
                    break
            candidates.append(cur_set)
                
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
    frequent_itemsets = {k : sortedlist()}
    for x in range(transactions.shape[1]):
        frequent_itemsets[k].append(frozenset( (x,) )) # add 1-itemset {x}
        
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

def ap_rule_generation(frequent_itemsets, k):
	rules = []
	for itemset in frequent_itemsets[k]:
		ap_genrules(frequent_itemsets, rules, itemset, itemset)
	rules.sort(cmp=lambda x: 1 - x[2])
	return rules

def get_frequency(frequent_itemsets, itemset):
	return frequent_itemsets[len(itemset)].get(itemset).frequency

def ap_genrules(frequent_itemsets, rules, f, H):
	frequency = lambda itemset: get_frequency(frequent_itemsets, itemset)
	k = len(f)
	m = len(H)

	if k > m+1:
		candidates = generate_candidates(H, k)
		i = 0
		while i < len(candidates):
			# for rule X -> Y - X: confidence = support(Y) / support(Y - X)
			# frequencies can be used because of the division operation.
			confidence = frequency(f) / frequency(f - candidates[i])
			if confidence >= minConfidence:
				rules.apend( (f, f - candidates[i], confidence) )
				i = i + 1
			else:
				del candidates[i]
		ap_genrules(frequent_itemsets, rules, f, candidates)
