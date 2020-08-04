# AdFly-Bot

**AdFly-Bot** is bot created for [adf.ly](https://adf.ly) website.

## Content

- [Content](#content)
- [Installation](#installation)
  - [Windows](#windows)
  - [Unix](#unix)
- [Usage](#usage)
- [Documentation](#documentation)
- [Disclaimer](#disclaimer)
- [Authors](#authors)
- [Contact](#contact)
- [License](#license)

## Installation

### Windows

* Install [Git](https://git-scm.com/download/win), [Python3.6+](https://www.python.org/downloads) and web browser ([Google Chrome](https://www.google.com/chrome) or [Firefox](https://www.mozilla.org/firefox/new)).
* [Download](https://github.com/DeBos99/adfly-bot/archive/master.zip) this repository or run following command in the command prompt:
```
git clone https://gitlab.com/DeBos/adfly-bot.git
```
* Open adfly-bot folder.
* Run install.bat

### Unix

* Run following commands in the terminal:
```
curl -fs https://gitlab.com/DeBos/mpt/raw/master/mpt.sh | sh -s install "git python"
git clone https://gitlab.com/DeBos/adfly-bot.git
cd adfly-bot
make
```

## Usage

* Run following command in the command prompt or the terminal:
```
python main.py [-h] [-u URL|FILE] [-p N] [-B firefox|chrome] [-P FILE] [-R REFERER|FILE] [-U USER_AGENT|FILE]
```

## Documentation

| Short               | Long                           | Description                                          | Default value           |
| :------------------ | :----------------------------- | :--------------------------------------------------: | :---------------------: |
| -h                  | --help                         | Show help message and exit.                          | :x:                     |
| -u URL\|FILE        | --urls URL\|FILE               | Set URL | Set path to file with URLs.                | :x:                     |
| -p N                | --processes N                  | Set number of processes.                             | 15                      |
| -B firefox\|chrome  | --browser firefox\|chrome      | Set browser.                                         | :x:                     |
| -P FILE             | --proxies FILE                 | Set path to proxies list.                            | Proxy list from API.    |
| -R REFERER\|FILE    | --referers REFERER\|FILE       | Set referer \| Set path to file with referers.       | https://google.com      |
| -U USER_AGENT\|FILE | --user-agents USER_AGENT\|FILE | Set user agent \| Set path to file with user agents. | Random user agent.      |

## Disclaimer

**AdFly-Bot** was created for educational purposes and I'm not taking responsibility for any of your actions.

## Authors

* **Michał Wróblewski** - Main Developer - [DeBos](https://gitlab.com/DeBos)

## Contact

* Telegram: [@DeBos99](https://t.me/DeBos99)
* Reddit: [DeBos99](https://www.reddit.com/user/DeBos99)
* Twitter: [@DeBos99](https://www.twitter.com/DeBos99)
* Instagram: [@DeBos98](https://www.instagram.com/DeBos98)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
