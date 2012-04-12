#!/usr/bin/env python
"""Implementations of algorithms."""

import numpy
import sys
import random
import itertools

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
	candidates = []
	if k == 2:
		for s,t in itertools.combinations(sequences,2):
			e1 = s[0]
			e2 = t[0]
			candidates.append( ((e1[0],e2[0]),) )
		for s,t in all_pairs(sequences):
			candidates.append( (s[0],t[0]) )
		candidates.sort()
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
			if not infreq: candidates.append(c)
	return candidates

def frequent_sequences(database):
	# generate 1-sequences... to freq_seqs[1]
	freq_seqs = {} # dict: values of k as keys and sets of k-sequences as values
	# remove infreq 1-seqs from freq_seqs[1]
	for k in xrange(2,100):
		candidates = seq_candidate_generation(freq_seqs[k-1], k)
		for candidate in candidates:
			if seq_frequency(candidate) >= minsupp:
				freq_sets[k].append(candidate)
	return freq_seqs	

