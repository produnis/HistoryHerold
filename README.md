# HistoryHerold
A python 3.x bot that post news according to the current date to Mastodon, Diaspora, Friendica

It could be of use for e.g. traditional clubs, companies or families that want to remind of their rich history. 

This bot is "just" for posting existing(!) stuff. You will have to create the content on your own!!! 

See "Usage" for details about the content.

## Requirements
This bot requieres
* python3
  * argparse
  * diaspy
  * Mastodon.py
  * requests

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
This bot looks up the current date as DD-MM (two digits day and two digits month). It looks up the current directory for txt-files named `DD-MM*.txt`. For example, if today is christmas, it will look for txt-files `24-12*.txt`, e.g. `24-12-1946_UncleBen.txt` or `24-12-2017_NewYork.txt`.
For every txt-file it found, it looks for mediafiles (jpg, png, mp4) that have the same basename. For example, if it found txt-file`24-12-2017_NewYork.txt`, it will look for mediafiles `24-12-2017_NewYork*` with suffix jpg, png or mp4.
The bot posts the content of the txt-file along with the pictures or videos it found to a given Mastodon, Diaspora and/or Friendica account. 
If there are no mediafiles, it posts the textmessage only.

So, your job is to fill the bot's directory with txt-files and pictures or videos. In the end, your directory could look like this:
```
17-01-1904_Event.txt
17-01-1904_Event.jpg
17-01-1904_Event2.jpg
18-03-1977_Hero.txt
24-12-1946_UncleBen.txt
24-12-1946_UncleBen.mp4
LICENSE
README
historyherold.py
```

The bot will manage an archive file called `archive-YYYY-*.txt` in the given directory (check for write permission). In this archive, filenames of txt-files already posted are stored (to avoid double posting). So, the bot looks up all txt-files in the given directory and compares their filenames with his archive. The bot won't post any txt of filenames included in  his archive.

### Parameters
You might want to edit `historyherold.py` and give the credentials of your accounts at Mastodon, Friendica and/or Diaspora.
This is recommended, however, you can set all credentials via parameters while calling the bot.
If you "hardcoded" your credentials, just call the bot like this:
```
cd /path/to/HistoryHerold
python3 historyherold.py -m -d -f
```
* The params:
  * `-m` tells the bot to post to Mastodon, using your hardcoded credentials
  * `-d` tells the bot to post to Diaspora, using your hardcoded credentials
  * `-f` tells the bot to post to Friendica, using your hardcoded credentials

If you want to post to e.g. Diaspora only, the call would be
```
python3 historyherold.py -d
```

If you want to do a test without posting at all, type in
```
python3 historyherold.py
```

If you want to run the bot "quiet" (without any output), use `-q`
```
python3 historyherold.py -d -m -q
```

Use `-h` for help and more parameters
```
python3 historyherold.py -h
```


### CronJob
This bot is ment to run via Cronjob

```
# example Cronjob to fire every day at 9 am and 7 pm
0 9,19 * * * cd /path/to/HistoryHerold; python3 historyherold.py -m -d -f

```

## Live Example
This bot runs on the following accounts in the fediverse:
* https://botsin.space/@schalkermythos
* https://diaspod.de/u/schalkermythos
