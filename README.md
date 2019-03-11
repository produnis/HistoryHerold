# HistoryHerold
A python 3.x bot that post news according to the current date to Mastodon, Diaspora, Friendica

## Requirements
This bot requieres
- python3
-- argparse
-- diaspy
-- Mastodon.py 
-- requests

## How to install
```
# install diaspy
git clone https://github.com/marekjm/diaspy.git
cd diaspy
sudo python3 setup.py install
cd ..
rm -r diaspy

# install Mastodon.py
sudo pip3 install -r Mastodon.py

# clone this repo
git clone https://github.com/produnis/HistoryHerold.git
```

## Usage


### CronJob
This bot is ment to run via Cronjob

```
# example Cronjob to fire every day at 9 am and 7 pm
0 9,19 * * * cd /path/to/HistoryHerold; python3 historyherold.py -m -d -f

```

