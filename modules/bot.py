import os
import signal
import logging
import platform
from pathlib import Path
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire.webdriver import Chrome,ChromeOptions,Firefox,FirefoxOptions

class Bot(object):
	def __init__(self,args,urls,browser,proxies,referers,user_agents):
		self.urls=urls
		self.browser=browser
		self.proxies=proxies
		self.referers=referers
		self.user_agents=user_agents
		self.driver=None
		self.running=True
	def run(self):
		signal.signal(signal.SIGINT,self.quit)
		logging.basicConfig(level=logging.CRITICAL)
		while self.running:
			try:
				seleniumwire_options={
					'proxy':{
						'http':f'http://{self.proxies.get()}',
						'https':f'https://{self.proxies.get()}',
						'no_proxy':'localhost,127.0.0.1'
					},
					'connection_timeout':None,
					'verify_ssl':False
				}
				if platform.system()=='Windows':
					file_extension='.exe'
				else:
					file_extension=''
				executable_path=Path(__file__).resolve().parent.parent/'drivers'
				if self.browser=='chrome':
					options=ChromeOptions()
					options.add_argument(f'--user-agent={self.user_agents.get()}')
					options.add_argument('--mute-audio')
					options.add_argument('--disable-extensions')
					options.add_argument('--disable-gpu')
					options.add_argument('--disable-dev-shm-usage')
					options.add_argument('--no-sandbox')
					options.add_argument('--headless')
					options.add_experimental_option('excludeSwitches',['enable-logging'])
					executable_file=executable_path/f'chromedriver{file_extension}'
					WebDriver=Chrome
				else:
					options=FirefoxOptions()
					options.preferences.update({
						'media.volume_scale':'0.0',
						'general.useragent.override':self.user_agents.get()
					})
					options.add_argument('--headless')
					executable_file=executable_path/f'geckodriver{file_extension}'
					WebDriver=Firefox
				self.driver=WebDriver(
					options=options,
					seleniumwire_options=seleniumwire_options,
					service_log_path=os.devnull,
					executable_path=executable_file
				)
				self.driver.header_overrides={
					'Referer':self.referers.get()
				}
				self.driver.set_page_load_timeout(60)
				url=self.urls.get()
				self.driver.get(url[0])
				if self.driver.title==url[1]:
					WebDriverWait(self.driver,10).until(EC.element_to_be_clickable((By.ID,'skip_bu2tton'))).send_keys(Keys.RETURN)
			except:
				pass
			finally:
				self.close()
	def close(self):
		try:
			self.driver.quit()
		except:
			pass
	def quit(self,*args):
		self.running=False
		self.close()
