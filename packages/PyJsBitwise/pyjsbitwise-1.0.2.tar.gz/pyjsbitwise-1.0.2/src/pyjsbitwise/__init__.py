from functools import reduce as _reduce
from math import isnan as _isnan

def i32cast(n):
	"""Overlow behavior of signed 32-bit integer.
 	:param n: Number to be owerflowed. Int or float.
  	:return: The overflowed result. Int.
 	"""
	return 0 if n == None or _isnan(n) else (int(n) + 0x80000000) % 0x100000000 - 0x80000000

def lshift(n, i):
	"""JavaScript-flavored bitwise shift left (<<).
 	:param n: Number to be owerflowed. Int or float.
 	:param i: Number of bits to shift by. Int.
  	:return: The shift result. Int.
 	"""
	if n == None or _isnan(n):
		return 0
	n = int(n) & 0xFFFFFFFF
	i = 0 if i == None or _isnan(n) else int(i) & 0x1F
	return i32cast(n << i if i >= 0 else n >> -i)

def rshift(n, i):
	"""JavaScript-flavored shift right (>>).
 	:param n: Number to be owerflowed. Int or float.
 	:param i: Number of bits to shift by. Int.
  	:return: The shift result. Int.
 	"""
	if n == None or _isnan(n):
		return 0
	n = (int(n) & 0xFFFFFFFF) if type(n) is float else i32cast(n)
	i = 0 if i == None or _isnan(n) else int(i) & 0x1F
	return i32cast(n >> i if i >= 0 else n << -i)

def urshift(n, i):
	"""JavaScript-flavored unsigned shift right (>>>).
 	:param n: Number to be owerflowed. Int or float.
 	:param i: Number of bits to shift by. Int.
  	:return: The shift result. Int.
 	"""
	if n == None or _isnan(n):
		return 0
	n = int(n) & 0xFFFFFFFF
	i = 0 if i == None or _isnan(n) else int(i) & 0x1F
	return (n >> i if i >= 0 else -n << -i) & 0xffffffff

def bwnot(n):
	"""JavaScript-flavored bitwise not (~).
 	:param m: Number. Int or float.
  	:return: The bitwise-not result. Int.
 	"""
	return ~i32cast(n)

def bwand(*args):
	"""JavaScript-flavored bitwise and (&).
 	:param *args: Numbers. Int or float.
  	:return: The bitwise-and result. Int.
 	"""
	return _reduce(lambda m, n: i32cast(m) & i32cast(n), args)

def bwor(*args):
	"""JavaScript-flavored bitwise or (|).
 	:param *args: Numbers. Int or float.
  	:return: The bitwise-or result. Int.
 	"""
	return _reduce(lambda m, n: i32cast(m) | i32cast(n), args)

def bwxor(*args):
	"""JavaScript-flavored bitwise xor (^).
 	:param *args: Numbers. Int or float.
  	:return: The bitwise-xor result. Int.
 	"""
	return _reduce(lambda m, n: i32cast(m) ^ i32cast(n), args)
