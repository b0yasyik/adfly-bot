import os
import sys
import stat
import platform
from tarfile import TarFile
from zipfile import ZipFile

import wget
import requests
from pathlib import Path

from modules.helpers import Input


class Extension(object):
    extensions_path = Path(__file__).resolve().parent.parent / 'extensions'

    def install_if_not_installed(browser):
        if browser == 'chrome':
            extension_path = (
                Extension.extensions_path / 'Easy WebRTC Block.crx'
            )
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
    system = platform.system()
    drivers_path = Path(__file__).resolve().parent.parent / 'drivers'

    def get_driver_name(browser):
        if browser == 'chrome':
            driver_name = 'chrome'
        elif browser == 'firefox':
            driver_name = 'gecko'
        return f'{driver_name}driver'

    def get_executable_path(browser):
        driver_name = WebDriver.get_driver_name(browser)
        if os.name == 'nt':
            file_extension = '.exe'
        elif os.name == 'posix':
            file_extension = ''
        return WebDriver.drivers_path / f'{driver_name}{file_extension}'

    def download(browser):
        arch = platform.machine()[-2:].replace('86',
                                               '32')
        urls = {
            'chrome': {
                'Windows': 'https://chromedriver.storage.googleapis.com/{0}/chromedriver_win32.zip',
                'Linux': 'https://chromedriver.storage.googleapis.com/{0}/chromedriver_linux64.zip',
                'Darwin': 'https://chromedriver.storage.googleapis.com/{0}/chromedriver_mac64.zip',
            },
            'firefox': {
                'Windows': 'https://github.com/mozilla/geckodriver/releases/download/{0}/geckodriver-{0}-win{1}.zip',
                'Linux': 'https://github.com/mozilla/geckodriver/releases/download/{0}/geckodriver-{0}-linux{1}.tar.gz',
                'Darwin': 'https://github.com/mozilla/geckodriver/releases/download/{0}/geckodriver-{0}-macos.tar.gz',
            },
        }
        if browser == 'chrome':
            if os.name == 'posix' and arch == '32':
                print('Chromedriver does not support 32-bit Unix machines.')
                answer = Input.get(
                    'Do you want to install Geckodriver (Firefox) instead [Y/N]? '
                ).lower()
                if answer == 'y':
                    WebDriver.download('firefox')
                else:
                    sys.exit(0)
            driver_version = requests.get(
                'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
            ).content.decode()
        else:
            driver_version = requests.get(
                'https://api.github.com/repos/mozilla/geckodriver/releases/latest'
            ).json()['tag_name']
        return wget.download(
            urls[browser][WebDriver.system].format(driver_version,
                                                   arch),
            bar=wget.bar_thermometer
        )

    def install_if_not_installed(browser):
        executable_path = WebDriver.get_executable_path(browser)
        if not executable_path.is_file():
            print(f'Installing webdriver for {browser}...')
            filename = WebDriver.download(browser)
            if filename.endswith('.zip'):
                open_archive = ZipFile
            elif filename.endswith('.tar.gz'):
                open_archive = TarFile.open
            WebDriver.drivers_path.mkdir(exist_ok=True)
            with open_archive(filename) as file:
                file.extractall(WebDriver.drivers_path)
            Path(filename).unlink()
            if os.name == 'posix':
                executable_path.chmod(stat.S_IRWXU)
            print(f'\nInstalled webdriver for {browser}.')
        return executable_path

    def kill(browser):
        if os.name == 'nt':
            command_template = (
                'taskkill /IM {0}.exe /IM {1}.exe /T /F >NUL 2>&1'
            )
        elif os.name == 'posix':
            command_template = 'killall -eqs KILL {0} {1}'
        driver_name = WebDriver.get_driver_name(browser)
        os.system(command_template.format(driver_name,
                                          browser))
