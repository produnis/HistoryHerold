#!/usr/bin/env python3
#............................
import argparse
import datetime	
import diaspy # git clone https://github.com/marekjm/diaspy.git ; cd diaspy; sudo python3 setup.py install
import glob
from mastodon import Mastodon # sudo pip3 install Mastodon.py
import os
import requests
import sys
from urllib.parse import quote
#---------------------------------------------
# 		CHANGE TO FIT YOUR SETTINGS
#---------------------------------------------
botarchivefile   = "herold_my_club.txt"	# archive where to store already posted messages
standardmessage = '#cool #hashtag'	# message posted with each photo, e.g. "#nsfw"
bequiet 	= False  # should the script give some output on stdr? Set True to post nothing

# Mastodon
#---------
postmastodon  = False # we do NOT post in default
mastodonurl 		= 'https://botsin.space'	# The URL of your account's pod
mastodonvisibility 	= "public"			# "direct", "private", "unlisted", "public"
mastodontoken 		= "7203....foobar.foobar.....9bbbf"	# The acces-token is needed to login/post to your account
mastodonmaxletter 	= 420  # how many letters per post are allowed at your intance?
numberofmedia		= 4 	# how many mediafiles are we allowed to post (default = 4)
#---------------------------------------------

# Diaspora
#----------
postdiaspora = False # we do NOT post in default
podurl 			= 'https://diasp.eu' 	# The URL of your account's pod
poduser 		= 'test'		# Username	
poduserpwd 		= 'SUPERSECRETPWD'	# Password
diasporavisibility 	= "public"		# = (2431, 3423) # Aspect numbers

# Friendica
#-----------
postfriendica = False
friendicaurl 		= 'libranet.de' 	# The URL of your account's pod WITHOUT "https://"
friendicauser 		= 'testuser'		# Username	
friendicauserpwd 	= 'SUPERSECRETPWD'	# Password  # ist %23
friendicavisibility 	= "public"
#########################################################
# no need to change anything after here
#---------------------------------------------

#-------------------------------------------------------\\
## Functions
#-----------
def printOrNot(text):
	# we only print status messages, if "-q" ist NOT set
	if bequiet == False:
		print(text)
	return
#---------------------

################################################################################
# argparse
#---------
parser = argparse.ArgumentParser()

parser.add_argument("-q", "--quiet", action="store_true", help="print nothing out") # get argument with "args.quiet"
parser.add_argument("-ba", "--botarchivefile", help="filename to store archive")		
parser.add_argument("-nm", "--numberofmedia", help="max. number of mediafiles to post")	

parser.add_argument("-m", "--mastodon", action="store_true", help="post to mastodon")	
parser.add_argument("-mat", "--mastodonaccesstoken", help="Maston Access Token")	
parser.add_argument("-murl", "--mastodonurl", help="Maston instance url")	
parser.add_argument("-mmax", "--mastodonmaxletter", help="How many letters per post are allowed by your instance?")	
parser.add_argument("-mvis", "--mastodonvisibility", help="Visibility: direct, private, unlisted, public")	

parser.add_argument("-d", "--diaspora", action="store_true", help="post to diaspora")		
parser.add_argument("-du", "--diasporauser", help="username at diaspora")		
parser.add_argument("-dpw", "--diasporapwd", help="password at diaspora")		
parser.add_argument("-dpod", "--diasporapod", help="password at diaspora")		
parser.add_argument("-dvis", "--diasporavisibility", help="public or (aspectnumber, aspectnumber)")		

parser.add_argument("-f", "--friendica", action="store_true", help="post to friendica")		
parser.add_argument("-fu", "--friendicauser", help="username at friendica")		
parser.add_argument("-fpw", "--friendicapwd", help="password at friendica")		
parser.add_argument("-fpod", "--friendicaurl", help="password at friendica")	
parser.add_argument("-fvis", "--friendicavisibility", help="public")		

args = parser.parse_args()
#-------------------------------------------------------//

if args.quiet:
	bequiet = True

if args.botarchivefile:
	botarchivefile = args.botarchivefile
	printOrNot("Scheme for archive file is set to %s" % botarchivefile)

if args.numberofmedia:
	numberofmedia = args.numberofmedia
	
#---------
if args.mastodon:
	postmastodon = True
	printOrNot("Posting to Mastodon!")
	
if args.mastodonaccesstoken:
	mastodontoken = args.mastodonaccesstoken

if args.mastodonurl:
	mastodonurl = args.mastodonurl
	
if args.mastodonmaxletter:
	mastodonmaxletter = args.mastodonmaxletter
	
if args.mastodonvisibility:
	mastodonvisibility = args.mastodonvisibility

#------------
if args.diaspora:
	postdiaspora = True
	printOrNot("Posting to Diaspora!")

if args.diasporauser:
	poduser = args.diasporauser
	
if args.diasporapwd:
	poduserpwd = args.diasporapwd
	
if args.diasporapod:
	podurl = args.diasporapod
	
if args.diasporavisibility:
	diasporavisibility = args.diasporavisibility

#------------
if args.friendica:
	postfriendica = True
	printOrNot("Posting to Friendica")
	
if args.friendicauser:
	friendicauser = args.friendicauser
	
if args.friendicapwd:
	friendicauserpwd = args.friendicapwd
	
if args.friendicaurl:
	friendicaurl = args.friendicaurl
	
if args.friendicavisibility:
	friendicavisibility = args.friendicavisibility

#-----------------------------------------------------------
# end of argparse
################################################################################	

### setting up some variables
right_now 	= 	datetime.datetime.now()
jahr 		= right_now.year
monat 		= "%02d" % right_now.month
heute 		= "%02d" % right_now.day
picdir 		= os.getcwd()
botarchivlogfile	= "%s/archive-%s-%s" % (picdir , jahr , botarchivefile)
post_mediafile 		= "None"
ismp4file 			= "No"
friendicapwd		= quote(friendicauserpwd)
###########----------------------------



printOrNot('Source directory is %s' % (picdir))

# check if we have a archive file for this year
printOrNot("Herold archiv file is %s" % (botarchivlogfile))
if not os.path.exists(botarchivlogfile):
	printOrNot('creating herold archive-log in %s' % (botarchivlogfile))
	f=open(botarchivlogfile,"w")
	f.close()

# read already posted pics from archive_posted.txt
archiveposted = open(botarchivlogfile).read()

# getting todays date dd-mm
heuteist = "%s-%s" % (heute, monat)
printOrNot("Today ist %s" % (heuteist))

news = sorted(os.listdir(picdir))
for anekdote in news:
	if anekdote.lower().endswith(('.txt')):
		# check if news was already posted
		if anekdote in archiveposted:
			printOrNot('Anekdote already posted: %s' % (anekdote))
		else:
			# is it news of the current day?
			if (anekdote[0:5] != heuteist):
				printOrNot("this file is NOT for today!")
			else: 
				printOrNot("This news is for today! We will post this!")
			
				printOrNot('Ready to post new Anekdote: %s' % (anekdote))
				pic_path = '%s/%s' % (picdir, anekdote)
				news_txt = open(anekdote).read()
				textmessage= '%s \n%s' % (news_txt, standardmessage)
				images2post = []
				videos2post = []

				# check if there is a picture or video for the message to post with
				pic_base = os.path.splitext(pic_path)[0] # remove suffix from filename
				for mediafile in glob.glob("%s*" % (pic_base)):
					printOrNot(mediafile)
					if mediafile.endswith(".jpg") or mediafile.endswith(".JPG") or mediafile.endswith(".png")  or mediafile.endswith(".PNG") :
						images2post.append(mediafile)
						printOrNot("This pic will be posted: %s" % mediafile)

					if mediafile.endswith(".MP4") or mediafile.endswith(".mp4") :
						videos2post.append(mediafile)
						printOrNot("This vid will be posted: %s" % mediafile)
				printOrNot("Number of Pictures for this Post: %s" % len(images2post))
				printOrNot("Number of Videos for this Post: %s" % len(videos2post))

				## -------------------------------
				## post to mastodon here
				if postmastodon == True:
					# Login to Mastodon
					printOrNot("Login to Mastodon...")
					mastodon = Mastodon(
						access_token = mastodontoken,
						api_base_url = mastodonurl
					)
					
					mastodontextmessage = textmessage
					# shorten if text is too long for mastodon
					if (len(textmessage) > mastodonmaxletter):
						x = mastodonmaxletter-len(standardmessage)-1
						mastodontextmessage = '%s \n%s' % (news_txt[0:x], standardmessage)
						printOrNot("Message too long, using short message: %s" % mastodontextmessage)

					# post pictures first
					x = 0
					mastopicid = []
					
					# post video if available (only 1 video possible)
					if videos2post:
						mastid = mastodon.media_post(media_file = videos2post[0], description=mastodontextmessage)
						mastopicid.append(mastid)
						
					# cannot post videos along with images
					elif images2post:
						for post_mediafile in images2post:
							if x != numberofmedia:
								mastid = mastodon.media_post(media_file = post_mediafile, description=mastodontextmessage)
								mastopicid.append(mastid)
								x = x+1

					# post status with pictures to mastodon
					mastodon.status_post(status=mastodontextmessage, media_ids=mastopicid, visibility=mastodonvisibility)
				## --------------------------------------



				## --------------------------------------
				##  post to Diaspora here
				if postdiaspora == True:
					printOrNot("Login to Diaspora...")
					connection = diaspy.connection.Connection(pod=podurl, username=poduser, password=poduserpwd)
					connection.login()
					token = repr(connection)
					stream = diaspy.streams.Stream(connection)
					
					# post pictures first
					diasporapicid = []
					for post_mediafile in images2post:
						photoid = stream._photoupload(filename=post_mediafile)
						diasporapicid.append(photoid)
					
					# post message along with pictures
					stream.post(photos=diasporapicid, text=textmessage, aspect_ids=diasporavisibility)

				## --------------------------------------
				##  post to Friendica here
				if postdiaspora == True:
					printOrNot("posting to Friendica...")
					posturl = "https://{}:{}@{}//api/statuses/update.xml".format(friendicauser, friendicapwd, friendicaurl)
					
					# we can only post 1 picture, nothing more / else
					if images2post:
						postphoto = open(images2post[0], 'rb')
						multipart_form_data = {'media': postphoto }
					else:
						multipart_form_data = ""
					postparams = {
						'source': "HistoryHerold",
						'status': textmessage
					}
					
					requests.post(posturl, data=postparams, files=multipart_form_data)
										
				## --------------------------------------
				## write pic's filename to archive log
				f=open(botarchivlogfile,"a")
				f.write(anekdote)
				f.write('\n')
				f.close()

	else:
		printOrNot('This file has no valid suffix: %s' % (anekdote))	
printOrNot("\n\nI am done. Have a nice day")  
#-------------
# END OF FILE!
