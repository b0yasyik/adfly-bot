import os
import sys
import platform
from argparse import ArgumentParser
from multiprocessing import Process

if os.name == 'nt':
    import win32api
elif os.name == 'posix':
    import signal

from modules.bot import Bot
from modules.lists import URLs, Proxies, Referers, UserAgents
from modules.helpers import Input
from modules.webdriver import Extension, WebDriver


class Program(object):
    browser = None
    processes = []

    def check_support():
        if os.name != 'nt' and os.name != 'posix':
            print('Your operating system is not supported.')
            sys.exit(1)
        if platform.machine().startswith('arm'):
            print('Your architecture is not supported.')
            sys.exit(1)
        if sys.version_info[:2] < (3, 6):
            print('Your Python version is not supported.')
            sys.exit(1)

    def run():
        supported_browsers = ['chrome',
                              'firefox']
        parser = ArgumentParser()
        parser.add_argument('-u', '--url',
                            help=('Set URL | ' 'Set path to URL list'),
                            metavar='URL|FILE')
        parser.add_argument('-p', '--processes',
                            default=15,
                            type=int,
                            help='Set number of processes',
                            metavar='N')
        parser.add_argument('-B', '--browser',
                            choices=supported_browsers,
                            help='Set browser',
                            metavar='BROWSER')
        parser.add_argument('-P', '--proxies',
                            help='Set path to proxy list',
                            metavar='FILE')
        parser.add_argument('-R', '--referer',
                            help='Set referer | Set path to referer list',
                            metavar='REFERER|FILE')
        parser.add_argument('-U', '--user-agent',
                            help='Set user agent | '
                                 'Set path to user agent list',
                            metavar='USER_AGENT|FILE')
        args = parser.parse_args()
        urls = URLs(args.url or Input.get('URL'))
        Program.browser = (args.browser or
                           Input.select('Browser', supported_browsers))
        print('For next options click ENTER to use [default value].')
        proxies = Proxies(args.proxies or
                          Input.get('Proxies [proxy list from API]'))
        referers = Referers(args.referer or
                            Input.get('Referers [https://google.com]'))
        user_agents = UserAgents(args.user_agent or
                                 Input.get('User agents [random user agent]'))
        executable_path = WebDriver.install_if_not_installed(Program.browser)
        extension_path = Extension.install_if_not_installed(Program.browser)
        Program.processes = [Process(target=Bot.run,
                                     args=(urls,
                                           Program.browser,
                                           proxies,
                                           referers,
                                           user_agents,
                                           executable_path,
                                           extension_path),
                                     daemon=True)
                             for _ in range(args.processes)]
        print(f'Starting {args.processes} processes...')
        for process in Program.processes:
            process.start()
        print(f'Started {args.processes} processes.')
        if os.name == 'nt':
            win32api.SetConsoleCtrlHandler(Program.quit)
        elif os.name == 'posix':
            signal.signal(signal.SIGINT, Program.quit)
        print(f'Click ctrl+c when you want to stop the bot.')
        for process in Program.processes:
            process.join()

    def main():
        Program.check_support()
        Program.run()

    def quit(*args):
        print(f'\rExiting the bot...')
        for process in Program.processes:
            process.terminate()
        for process in Program.processes:
            process.join()
        WebDriver.kill(Program.browser)
        sys.exit(0)


if __name__ == '__main__':
    Program.main()
