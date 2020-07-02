import sys
import stat
import wget
import platform
import requests
from tarfile import TarFile
from zipfile import ZipFile

class WebDriver(object):
	system=platform.system()
	machine=platform.machine()
	def download(driver):
		if WebDriver.machine.startswith('arm'):
			arch='arm'
		else:
			arch=WebDriver.machine[-2:].replace('86','32')
		links={
			'chrome':{
				'Windows':'https://chromedriver.storage.googleapis.com/{0}/chromedriver_win32.zip',
				'Linux':'https://chromedriver.storage.googleapis.com/{0}/chromedriver_linux64.zip',
				'Darwin':'https://chromedriver.storage.googleapis.com/{0}/chromedriver_mac64.zip'
			},
			'firefox':{
				'Windows':'https://github.com/mozilla/geckodriver/releases/download/{0}/geckodriver-{0}-win{1}.zip',
				'Linux':'https://github.com/mozilla/geckodriver/releases/download/{0}/geckodriver-{0}-linux{1}.tar.gz',
				'Darwin':'https://github.com/mozilla/geckodriver/releases/download/{0}/geckodriver-{0}-macos.tar.gz'
			}
		}
		if driver=='chrome':
			if arch=='arm' or (WebDriver.system!='Windows' and arch=='32'):
				print('Chromedriver does not support ARM and 32-bit Unix machines.')
				answer=input('Do you want to install Geckodriver (Firefox) instead [Y/N]? ').lower()
				if answer=='y':
					WebDriver.download('firefox')
				else:
					sys.exit(1)
			driver_version=requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE').content.decode()
		else:
			if arch=='arm':
				pass
			else:
				driver_version=requests.get('https://api.github.com/repos/mozilla/geckodriver/releases/latest').json()['tag_name']
		return wget.download(links[driver][WebDriver.system].format(driver_version,arch))
	def install(driver_file_path,driver):
		filename=WebDriver.download(driver)
		if filename.endswith('.zip'):
			open_archive=ZipFile
		else:
			open_archive=TarFile.open
		with open_archive(filename) as file:
			file.extractall(driver_file_path.parent)
		if WebDriver.system!='Windows':
			driver_file_path.chmod(stat.S_IRWXU)
