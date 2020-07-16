import sys
import stat
import wget
import platform
import requests
from pathlib import Path
from tarfile import TarFile
from zipfile import ZipFile
from .helpers import Input

class Extension(object):
	extensions_path=Path(__file__).resolve().parent.parent/'extensions'
	def install_if_not_installed(browser):
		if browser=='chrome':
			extension_path=Extension.extensions_path/'Easy WebRTC Block.crx'
			if not extension_path.is_file():
				print(f'Installing extension for {browser}...')
				Extension.extensions_path.mkdir(exist_ok=True)
				wget.download(
					'https://clients2.google.com/service/update2/crx?response=redirect&prodversion=9999&acceptformat=crx2,crx3&x=id%3Dcmjcmogcdofcljpojplgmfpheblcaehh%26uc',
					out=str(extension_path),
					bar=wget.bar_thermometer
				)
				print(f'\nInstalled extension for {browser}.')
			return extension_path

class WebDriver(object):
	system=platform.system()
	machine=platform.machine()
	drivers_path=Path(__file__).resolve().parent.parent/'drivers'
	def get_executable_path(browser):
		if browser=='firefox':
			driver_name='gecko'
		else:
			driver_name='chrome'
		if WebDriver.system=='Windows':
			file_extension='.exe'
		else:
			file_extension=''
		return WebDriver.drivers_path/f'{driver_name}driver{file_extension}'
	def download(browser):
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
		if browser=='chrome':
			if arch=='arm' or (WebDriver.system!='Windows' and arch=='32'):
				print('Chromedriver does not support ARM and 32-bit Unix machines.')
				answer=Input.get('Do you want to install Geckodriver (Firefox) instead [Y/N]? ').lower()
				if answer=='y':
					WebDriver.download('firefox')
				else:
					sys.exit(0)
			driver_version=requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE').content.decode()
		else:
			if arch=='arm':
				pass
			else:
				driver_version=requests.get('https://api.github.com/repos/mozilla/geckodriver/releases/latest').json()['tag_name']
		return wget.download(links[browser][WebDriver.system].format(driver_version,arch),bar=wget.bar_thermometer)
	def install_if_not_installed(browser):
		executable_path=WebDriver.get_executable_path(browser)
		if not executable_path.is_file():
			print(f'Installing webdriver for {browser}...')
			filename=WebDriver.download(browser)
			if filename.endswith('.zip'):
				open_archive=ZipFile
			else:
				open_archive=TarFile.open
			WebDriver.drivers_path.mkdir(exist_ok=True)
			with open_archive(filename) as file:
				file.extractall(WebDriver.drivers_path)
			Path(filename).unlink()
			if WebDriver.system!='Windows':
				executable_path.chmod(stat.S_IRWXU)
			print(f'\nInstalled webdriver for {browser}.')
		return executable_path
