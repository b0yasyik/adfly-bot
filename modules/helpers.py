import os
import sys
import chardet

class File(object):
	def get_encoding(path):
		with open(path,'rb') as file:
			return chardet.detect(file.read())['encoding']
	def safe_read(path):
		if os.access(path,os.R_OK):
			with open(path,encoding=File.get_encoding(path)) as file:
				return file.read()
		else:
			print(f'Cannot read {path}')
			sys.exit(1)
