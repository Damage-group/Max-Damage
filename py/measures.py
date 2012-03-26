#!/usr/bin/python
import sys
import itertools
from algorithms import *
import math


#measure method:I(A,B) = s(A,B)/(s(A)*s(B)) = c(A->B)/s(B)
#input parameter:
#       frequent_itemsets
#       rules:for rule X -> Y -X: the corresponding item in rules is (X,Y-X,c(X->Y-X))
#output parameter:
#       rules_lift:(X,Y-X,lift_value)
def interest_factor(frequent_itemsets,rules):
        rules_lift = []
        frequency = lambda itemset: get_frequency(frequent_itemsets,itemset)
        for rule in rules:
                rules_lift.append((rule[0],rule[1],rule[2]/frequency(rule[1])))
        return rules_lift

#measure method:IS(A,B) = S(A,B)/sqrt(s(A)*s(B)) = c(A->B)*sqrt(s(A)/s(B))
#innput parameter:
#       frequent_itemsets
#       rules:for rule X -> Y -X: the corresponding item in rules is (X,Y-X,c(X->Y-X))
#output parameter:
#       rules_lift:(X,Y-X,lift_value)
def IS(frequent_itemsets,rules):
        frequency = lambda itemset: get_frequency(frequent_itemsets,itemset)
        rules_IS = []
        for rule in rules:
                rules_IS.append((rule[0],rule[1],rule[2]*math.sqrt(frequency(rule[0])/frequency(rule[1]))))
        return rules_IS

#measure method: Mutual Information(M) = [(S00log(S00/(S0+S+0))) +(S01log(S01/(S0+S+1))) + (S10log(S10/(S1+S+0))) + (S11log(S1/(S1+S+1)))]/(-S0+log(S0+)-S1+log(S1+))
#innput parameter:
#       frequent_itemsets
#       #       rules:for rule X -> Y -X: the corresponding item in rules is (X,Y-X,c(X->Y-X))
#       #output parameter:
#              rules_MI:(X,Y-X,MI_value)
def mutual_information(frequent_itemsets,rules):
        frequency = lambda itemset: get_frequency(frequent_itemsets,itemset)
        rules_MI = []
        for rule in rules:
                S_1 = frequency(rule[1])
                S1_ = frequency(rule[0])
                S11 = rule[2]*S1_
                S00 = 1 - S_1 - S1_ + S11
                S_0 = S1_ - S11 + S00
                S0_ = S_1 - S11 + S00
                S01 = S0_ - S00
                S10 = S1_ - S11
                M = S00 * math.log(S00/(S0_ * S_0))
                M = M + S01 * math.log(S01/(S0_ * S_1))
                M = M + S10 * math.log(S10/(S1_ * S_0))
                M = M + S11 * math.log(S11/(S1_ * S_1))
                M = M /(-S0_ * math.log(S0_) - S1_ * math.log(S1_))
                rules_MI.append((rule[0],rule[1],M))
        return rules_MI

#measure method: certainty factor(F) = (S11/S1+ - S+1)/(1-S+1)
#innput parameter:
#       frequent_itemsets
#       #       rules:for rule X -> Y -X: the corresponding item in rules is (X,Y-X,c(X->Y-X))
#       #output parameter:
#       #       rules_F:(X,Y-X,F_value)
def certainty_factor(frequent_itemsets,rules):
        frequency = lambda itemset: get_frequency(frequent_itemsets,itemset)
        rules_F = []
        for rule in rules:
                F = (rule[2] - frequency(rule[1]))/(1 - frequency(rule[1]))
                rules_F.append((rule[0],rule[1],F))
        return rules_F
        
