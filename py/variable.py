'''
	"Generic" variable class implementation.
'''
import string


class variable(dict):
	# Allow course.foo notation.
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