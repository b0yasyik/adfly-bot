import os
import sys
import chardet

class File(object):
	def get_encoding(path):
		if os.access(path,os.R_OK):
			with open(path,'rb') as file:
				return chardet.detect(file.read())['encoding']
		else:
			print(f'Cannot read {path}')
			sys.exit(1)
	def safe_open(path):
		return open(path,encoding=File.get_encoding(path))
	def safe_read(path):
		with File.safe_open(path) as file:
			return file.read()

class Input(object):
	def get(name):
		try:
			return input(f'{name}: ')
		except KeyboardInterrupt:
			sys.exit(0)
	def select(name,options):
		options_string=' or '.join(options)
		while True:
			answer=Input.get(f'{name} ({options_string})').lower()
			if answer in options:
				return answer
			else:
				print(f'{name} has to be {options_string}')
