import os
import sys
import signal
import platform
from pathlib import Path
from argparse import ArgumentParser
from multiprocessing import Process
from modules.bot import *
from modules.lists import *
from modules.webdriver import *

if __name__=='__main__':
	if sys.version_info[:2]<(3,6):
		print('You need at least Python3.6 to run this program.')
		sys.exit(1)
	parser=ArgumentParser()
	parser.add_argument('-u','--url',help='Set URL | Set path to URL list',metavar='URL|FILE')
	parser.add_argument('-B','--browser',choices=['chrome','firefox'],help='Set browser',metavar='WEBDRIVER')
	parser.add_argument('-p','--processes',default=15,type=int,help='Set number of processes',metavar='N')
	parser.add_argument('-P','--proxies',help='Set path to proxy list',metavar='FILE')
	parser.add_argument('-R','--referer',help='Set referer | Set path to referer list',metavar='REFERER|FILE')
	parser.add_argument('-U','--user-agent',help='Set user agent | Set path to user agent list',metavar='USER_AGENT|FILE')
	args=parser.parse_args()
	try:
		if args.url:
			url=args.url
		else:
			url=input('URL: ')
		if args.browser:
			browser=args.browser
		else:
			while True:
				browser=input('Browser (chrome or firefox): ').lower()
				if browser in ['chrome','firefox']:
					break
				else:
					print('WebDriver has to be chrome or firefox.')
	except KeyboardInterrupt:
		sys.exit(0)
	drivers_path=Path(__file__).resolve().parent/'drivers'
	if not drivers_path.is_dir():
		drivers_path.mkdir()
	if browser=='firefox':
		driver_name='gecko'
	else:
		driver_name='chrome'
	if platform.system()=='Windows':
		file_extension='.exe'
	else:
		file_extension=''
	driver_file_path=drivers_path/f'{driver_name}driver{file_extension}'
	if not driver_file_path.is_file():
		WebDriver.install(driver_file_path,browser)
	urls=URLs(url)
	proxies=Proxies(args.proxies)
	referers=Referers(args.referer)
	user_agents=UserAgents(args.user_agent)
	processes=[Process(target=Bot(args,urls,browser,proxies,referers,user_agents).run,daemon=True) for _ in range(args.processes)]
	for process in processes:
		process.start()
	signal.signal(signal.SIGINT,signal.SIG_IGN)
	for process in processes:
		process.join()
	if platform.system()=='Windows':
		os.system(f'taskkill /IM {browser}.exe /T /F >NUL 2>&1')
	sys.exit(0)
