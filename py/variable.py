'''
	"Generic" variable class implementation.
'''
import string
import collections


class variable(dict):
	# Allow variable.foo notation.
	__getattr__= dict.__getitem__
	__setattr__= dict.__setitem__
	__delattr__= dict.__delitem__
	
	def __init__(self, dictionary = None, id = None):
		if not dictionary is None: 
			for (key, value) in zip(dictionary.keys(), dictionary.values()):
				self.__dict__[str.lower(key)] = value[0] if len(value) == 1 else value
		
		if not id is None:
			self.__dict__['id'] = self.__dict__[str.lower(id)]
	
	def __str__(self):
		class_str = ''
		for name, value in self.__class__.__dict__.items() + self.__dict__.items(): 
			class_str += string.ljust(name, 15) + '\t' + str(value) + '\n'
		return class_str
	
	def passes_restriction(self, restriction, key):
		if type(restriction) is type(tuple()):
			return self.in_interval(restriction, key)
		else:
			return self.is_exact(restriction, key)
	
	def in_interval(self, restriction, key):
		value = self.__dict__[str.lower(key)]
		start, end = restriction
		
		if type(value) == type(list()): 
			for val in value:
				if val >= start and val <= end:
					#print "%s <= %s <= %s" % (start, val, end)
					return True
		else:
			if value >= start and value <= end:
				#print "%s <= %s <= %s" % (start, value, end)
				return True
			
		return False
	
	def is_exact(self, restriction, key):
		value = self.__dict__[str.lower(key)]
		
		if type(value) == type(list()): 
			for val in value:
				if val == restriction:
					#print "%s == %s" % (val, restriction)
					return True
		else:
			if value == restriction:
				#print "%s == %s" % (value, restriction)
				return True
			
		return False
		
		
		
		
			
		