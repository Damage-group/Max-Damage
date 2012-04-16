#!/usr/bin/env python
"""Implementations of algorithms."""

import numpy
import sys
import random
import itertools

import settings
import input

freq_seqs = []
frequencies = {}

def exclude_first_event(seq):
	new_first_elem = seq[0][1:]
	if new_first_elem: return (new_first_elem,) + seq[1:]
	return seq[1:]

def exclude_last_event(seq):
	new_last_elem = seq[-1][:-1]
	if new_last_elem: return seq[:-1] + (new_last_elem,)
	return seq[:-1]

def all_pairs(seqs):
	for s in seqs:
		for t in seqs:
			yield (s,t)

def seq_candidate_generation(sequences, k):
	"""Candidate sequence generation.
	Parameters:
		sequences - (k-1)-sequences
		k - a positive integer, k > 1
	"""
	candidates = set()
	if k == 2:
		for s,t in itertools.combinations(sequences,2):
			e1 = s[0]
			e2 = t[0]
			candidates.add( ((e1[0],e2[0]),) )
		for s,t in all_pairs(sequences):
			candidates.add( (s[0],t[0]) )
		#candidates.sort()
		return candidates
	for s,t in all_pairs(sequences):
		if exclude_first_event(s) == exclude_last_event(t):
			event = t[-1][-1] # last event in the last element of t
			if len(t[-1]) == 1:
				c = s + ((event,),)  
			else:
				c = s[:-1] + (s[-1] + (event,),)
			# check for all contiguous (k-1)-subsequences and prune if one of them is infreq.
			infreq = False
			for e in xrange(len(c)):
				for i in xrange(len(c[e])):
					elem = c[e][:i] + c[e][i+1:]
					if elem: elem = (elem,)
					subseq = c[:e] + elem + c[e+1:]
					if subseq not in sequences:
						infreq = True
						break
			if not infreq: candidates.add(c)
	return candidates

def initial_supports(database):
	ret = set()
	supports = {}
	#print len(database)
	for row in database:
		encountered = []
		for e in row:
			#print "%s" % row
			for c in e:
				#print c
				if c not in encountered:
					encountered.append(c)
		#rint encounteredp
		for c in encountered:
			if (c,) not in supports: supports[(c,)] = 1
			else: supports[(c,)] = supports[(c,)] + 1
	
	
	#print supports
	for k, v in supports.items(): 
		f = float(v) / float(8465)
		#print "%s :%s" % (k, v)
		if f > settings.FREQUENT_SEQUENCE_THRESHOLD:
			#print f

			ret.append((k,))
			frequencies[(k,)] = f

	
	#print ret
	#freq_seqs[1] = ret
	freq_seqs.append([])
	freq_seqs.append(ret)
		#print freq_seqs
		#print "%s: %s" % (k, v)
	#print freq_seqs
		
	return freq_seqs
			
def frequent_sequences(database):
	# generate 1-sequences... to freq_seqs[1]
	freq_seqs = initial_supports(database) # dict: values of k as keys and sets of k-sequences as values
	# remove infreq 1-seqs from freq_seqs[1]
	for k in xrange(2,100):
		if len(freq_seqs[k-1]) == 0: break
		candidates = seq_candidate_generation(freq_seqs[k-1], k)
		freq_seqs.append([])
		for candidate in candidates:
			f = seq_frequency_fast(candidate, database)
			if  f >= settings.FREQUENT_SEQUENCE_THRESHOLD: 	
				print "%s: %s" % (candidate, f)
				freq_seqs[k].append(candidate)
	return (freq_seqs, frequencies)	


def is_subsequence(seq, super_seq, gap=-1):
    """
    [(2,3), (5)] s1
    [(4,5,6), (1,2,3)] s2

    """
    last = 0
    i = 0

    for s in seq:
        i = last
        for s2 in super_seq[last:]:
            if is_superevent(s, s2):
                last = i + 1
                break
            elif gap > -1 and last and i - last == gap:
                return False
            else:
                i = i + 1

        else:
            return False

    return True


def is_superevent(event, super_event):
    last = 0

    for e1 in event:
        i = last

        for e2 in super_event[last:]:
            if e1 == e2:
                last = i + 1
                break

            elif e1 < e2:
                return False

            i = i + 1
        else:
            return False

    return True


def seq_frequency(candidate, data):
	support = 0
	for transaction in data:
		if is_subsequence(candidate,transaction):
			support = support + 1
	#print support
	f = float(support) / float(8465)
	frequencies[candidate] = f
	#print f
	return f 


def seq_frequency_fast(candidate, data):
	s = numpy.sum([is_subsequence(candidate,transaction) for transaction in data])
	f = float(s) / float(8465)
	#print "%s: %s %s" % (candidate, s, f)
	frequencies[candidate] = f
	return f

def seq_genrules(frequentSeqs, minConf, data):
	rules = []
	for seq in frequentSeqs:
		lenSeq = len(seq)
		for i in range(1,lenSeq):
			cause = seq[0:lenSeq-i]
			consequent = seq[-i:lenSeq]
			confidence = seq_frequency(seq,data)/seq_frequency(cause,data)
			if confidence >= minConf:
				rules.append((cause,consequent,confidence))
				#print "%s->%s"%(cause,consequent)
	return rules
		

if __name__ == "__main__":
    s1 = [(52,75), (104,149), (101,), (101,)] #True
    s2 = [(52,75), (104,159), (101,), (101,)] #False
    s3 = [(101,),(101,)] # True
    s4 = [(101,),(101,), (101,)] # False
    s5 = [(52,103),(103,), (101,)] # True
    s6 = [(52,74), (234,)]
    s7 = [(52,74), (104,)]
    s8 = [(52,74), (101,)]


    superset = [(52, 52, 74, 75, 103), (31, 104, 149, 451), (5, 101, 103, 105), (101,), (234, 904)]
    data = [[(52, 52, 74, 75, 103), (31, 104, 149, 451), (5, 101, 103, 105), (101,)],[(52, 52, 74, 75, 103), (31, 104, 149, 451), (5, 101, 103, 105), (101,)]]

    assert(is_subsequence(s1, superset))
    assert(not is_subsequence(s2, superset))
    assert(is_subsequence(s3, superset))
    assert(not is_subsequence(s4, superset))
    assert(is_subsequence(s5, superset))
    assert(is_subsequence(s6, superset, 3))
    assert(not is_subsequence(s6, superset, 1))
    assert(not is_subsequence(s6, superset, 2))
    assert(is_subsequence(s7, superset, 0))
    assert(not is_subsequence(s8, superset, 0))

    #print seq_frequency_fast(s2,data)
    seq_genrules([s1,s3],0,data)
