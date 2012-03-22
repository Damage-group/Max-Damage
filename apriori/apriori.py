#!/usr/bin/env python

import numpy
import sys
import random
import itertools

'''    
    These are the frequent itemsets for all k's.
    Keys are '1', ..., 'k' and values are sets of 
    n-membered sets for each key 'n' in [1, k].
'''
frequent_itemsets = dict()

'''
    Frequencies of all the itemsets. Keys are forzensets and values are floats.
'''
itemset_frequencies = dict()

'''    
    Percentage of the transactions which need to have certain itemset before it's
    considered 'frequent itemset'.
'''
threshold = 0.5

'''
    Map names to indexes.

    Parameters:
        filepath -    (absolute) path to file to read.
                      File should have one name / line.

    Returns dictionary with keys as course names and 
    values mapped to indexes starting from 0.
'''
def map_course_names(filepath = None):
    
    if filepath is None:
        raise ValueError("There was no filepath given to map_course_names.")
        return None

    names = []

    try:
        f = open(filepath, "r")
        lines = f.readlines()
        index = 0
    
        for l in lines:
            items = l.split()
            for item in items:
                if item not in names:
                    names.append(item)
                    index = index + 1
             
    except IOError:
        print("Could not read the file in %s" % (filepath))
        return None
    
    # Sort the names so that indices will come in lexicographical order.
    names.sort()
    name_map = dict()
    index = 0
    
    for n in names:
        name_map[n] = index
        index = index + 1
        
    return name_map

'''
    Read transactions to matrix using given name map.

    Supposes that given file contains one transaction 
    in line and each item in transaction is separated by 
    " ".

    Parameters:
        filepath -    (absolute) path to file to read.
        name_map - dictionary with keys as names and values
                   as column indexes for items. 
        strip - Lines with equal or less objects than this after split()
        		will be omitted.

    Returns transactions matrix with each transaction
    in one row and each column index representing item 
    that is mapped to that particular index in name_map.
'''
def read_transactions(filepath = None, name_map = None, strip = 2):
    
    if filepath is None:
        raise ValueError("There was no filepath given to read_transactions.")
        return None
    
    if name_map is None:
        raise ValueError("There was no name_map given to read_transactions.")
        return None
    
    f = None

    try:
        f = open(filepath, "r")    
    except IOError:
        print("Could not open the file in %s" % (filepath))
        return None
    
    lines = f.readlines()
    lines = [l for l in lines if len(l.split()) > strip]
    columns = len(name_map.keys())
    rows = len(lines)
    transactions = numpy.zeros((rows, columns), dtype = int)
    print ("%d course names and %d transactions" % (columns, rows))
    
    current_row = 0
    
    for l in lines:
        items = l.split()
        if len(items) > 2:
            for item in items:
                transactions[current_row][name_map[item]] = 1 
            current_row = current_row + 1

    return transactions

'''
    Sort the transactions (reverse-)lexicographically so that 
    transactions which have items in small indexes are 
    in the first rows. Resulting matrix could be something 
    like this for "boolean" values:

        [1, 1, 0, ..., 0, 1, 0]
        [1, 0, 1, ..., 1, 0, 1]
        [0, 1, 0, ..., 0, 0, 1]
        ...
        [0, 0, 0, ..., 1, 1, 1]

    Params:
        matrix - 2d numpy.matrix object
    
    Returns the sorted transactions matrix.
'''
def lexsort_2d_matrix(matrix = None):
    
    if matrix is None:
        raise ValueError("No matrix given as an argument for lexsort_2d_matrix.")
        return None
    
    # Generate sorting keys for numpy's lexsort.
    sort_keys = []
    item_count = matrix.shape[1]
    for x in range(item_count):
        sort_keys.append(matrix[:,x])
    
    sort_keys.reverse()
    
    # Get the indices by which the original matrix will be sorted
    # lexicographical order.
    indices = numpy.lexsort(sort_keys, axis = 0)
    
    # Flip the matrix to get it in right (ie. reversed) order.
    return numpy.flipud(matrix[indices])

'''
    Calculate frequency percentage in transactions for each k-itemset in 
    itemsets.

    Params:
        itemsets     - sequence of k-membered sets. Each member representing column.
        transactions - numpy.matrix from which the frequencies are 
                       calculated from.

    Returns dictionary with k-itemsets as keys and frequencies as values.
'''
def calculate_frequencies(itemsets = None, transactions = None):
    
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
        itemset_frequencies[itemset] = float(current_freq) / float(transactions_count)    

'''
    Prune off itemsets' which have lower frequency than threshold.
    Store rest to frequent_itemsets. All itemsets must have same amount
    of members.

    Params:
        itemsets    - set of itemset's to be pruned.
'''      
def prune_infrequent(itemsets = None, threshold = 0.5):  
    
    if len(itemsets) == 0:
        return None
    
    k = len(random.choice(list(itemsets)))
    
    if k not in frequent_itemsets:
        frequent_itemsets[k] = set()   

    for itemset in itemsets:
        if itemset_frequencies[itemset] > threshold:
            frequent_itemsets[k].add(itemset)     

'''       
    Generate k+1-itemsets from previous frequent itemsets.

    Params:
        k - positive integer. frequent_itemsets needs to have value for key k.

    Returns new k+1-itemsets which have all their subsets in frequent_itemsets[k].
'''
def generate_candidates(k):
    
    if not k in frequent_itemsets:
        return None
    
    if len(frequent_itemsets[k]) == 0:
        return None

    candidates = set()
    
    for itemsets in itertools.combinations(frequent_itemsets[k], 2):
        cur_set = itemsets[0].union(itemsets[1])
        
        # If sets union is k+1 then they have exatcly one different member.
        if len(cur_set) == k+1:
            # Test that all the subsets of the candidate are in 
            #frequent_itemsets.
            for subset in set(itertools.combinations(cur_set, k)):
                if subset not in frequent_itemsets[k]:
                    break
            candidates.add(cur_set)
                
    return candidates
     
    
'''
    Print the itemsets to std out.
'''    
def print_itemsets(k, names= None):

    for x in frequent_itemsets[k]:
        frequency = itemset_frequencies[frozenset(x)]
        cur_names = [names[i] for i in x]
        print "%d: %f \t %s " % (k, frequency, cur_names)

         
'''      
    Apriori logic
'''                         
def main():
    
    if len(sys.argv) < 3:
        print("Usage: %s input_file %%-threshold [strip]" % (sys.argv[0]))
        sys.exit(0)
    
    input_file = sys.argv[1]
    threshold = float(sys.argv[2])
    strip = 0
    
    if (len(sys.argv) >= 4):
        strip = float(sys.argv[3])
    
    name_map = map_course_names(input_file)
    transactions = read_transactions(input_file, name_map, strip)
    transactions = lexsort_2d_matrix(transactions)
    
    # Something stupid
    names = [i for i in range(len(name_map))]
    for key, value in name_map.items():
        names[value] = key
    
    # First create all 1-itemsets
    itemsets = set()
    for x in range(transactions.shape[1]):
        itemset = set()
        itemset.add(x)
        itemsets.add(frozenset(itemset))
        
    calculate_frequencies(itemsets, transactions)
    prune_infrequent(itemsets, threshold)
        
    # Then loop through the rest
    for k in range(1,5):
        candidates = generate_candidates(k) 
        if candidates is None:
            break
        calculate_frequencies(candidates, transactions)
        prune_infrequent(candidates, threshold)
        print_itemsets(k, names)
    
'''  
    make this runnable from commandline with arguments
'''  
if __name__ == "__main__":

    
    main()
    
    
    
        
        
    
    
    