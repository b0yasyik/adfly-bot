import os
import sys
import signal
from argparse import ArgumentParser
from multiprocessing import Process
from modules.bot import Bot
from modules.lists import *
from modules.helpers import Input
from modules.webdriver import *

if __name__=='__main__':
	if sys.version_info[:2]<(3,6):
		print('You need at least Python3.6 to run this program.')
		sys.exit(1)
	supported_browsers=['chrome','firefox']
	parser=ArgumentParser()
	parser.add_argument('-u','--url',help='Set URL | Set path to URL list',metavar='URL|FILE')
	parser.add_argument('-p','--processes',default=15,type=int,help='Set number of processes',metavar='N')
	parser.add_argument('-B','--browser',choices=supported_browsers,help='Set browser',metavar='BROWSER')
	parser.add_argument('-P','--proxies',help='Set path to proxy list',metavar='FILE')
	parser.add_argument('-R','--referer',help='Set referer | Set path to referer list',metavar='REFERER|FILE')
	parser.add_argument('-U','--user-agent',help='Set user agent | Set path to user agent list',metavar='USER_AGENT|FILE')
	args=parser.parse_args()
	urls=URLs(args.url or Input.get('URL'))
	browser=args.browser or Input.select('Browser',supported_browsers)
	print('For next options click ENTER to use [default value].')
	proxies=Proxies(args.proxies or Input.get('Proxies [proxy list from API]'))
	referers=Referers(args.referer or Input.get('Referers [https://google.com]'))
	user_agents=UserAgents(args.user_agent or Input.get('User agents [random user agent]'))
	executable_path=WebDriver.install_if_not_installed(browser)
	extension_path=Extension.install_if_not_installed(browser)
	processes=[Process(target=Bot().run,args=(urls,browser,proxies,referers,user_agents,executable_path,extension_path),daemon=True) for _ in range(args.processes)]
	print(f'Starting {args.processes} processes...')
	for process in processes:
		process.start()
	print(f'Started {args.processes} processes.')
	print(f'Click ctrl+c when you want to stop the bot.')
	signal.signal(signal.SIGINT,signal.SIG_IGN)
	for process in processes:
		process.join()
	if WebDriver.system=='Windows':
		os.system(f'taskkill /IM {browser}.exe /T /F >NUL 2>&1')
	print(f'\rExiting the bot...')
	sys.exit(0)
