import re
import random
import chardet
import requests
import user_agent
from bs4 import BeautifulSoup
from .helpers import File

class CustomList(object):
	def __init__(self,path):
		self.list=list(filter(bool,File.safe_read(path).splitlines()))
	def get(self):
		return random.choice(self.list)

class URLs(CustomList):
	def __init__(self,url):
		if re.match(r'^https?://',url):
			self.list=[url]
		else:
			super().__init__(url)
		self.list=[[url,BeautifulSoup(requests.get(url).text,'html5lib').title.text] for url in self.list]

class Proxies(CustomList):
	def __init__(self,path):
		if path:
			super().__init__(path)
		else:
			data=''
			urls=[
				'https://api.proxyscrape.com?request=getproxies&proxytype=http&timeout=5000&anonymity=anonymous&ssl=true',
				'https://api.proxyscrape.com?request=getproxies&proxytype=http&timeout=5000&anonymity=elite&ssl=true'
			]
			for url in urls:
				data+=requests.get(url).text
			self.list=list(filter(bool,data.splitlines()))

class Referers(CustomList):
	def __init__(self,referer):
		if referer:
			if re.match(r'^https?://',referer):
				self.list=[referer]
			else:
				super().__init__(referer)
		else:
			self.list=['https://google.com']

class UserAgents(CustomList):
	def __init__(self,path):
		if path:
			super().__init__(path)
		else:
			self.list=None
	def get(self):
		if self.list:
			return super().get()
		else:
			return user_agent.generate_user_agent()
