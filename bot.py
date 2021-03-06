### IMPORTS  #########################################################################

### sys stuff ###
import random, sys, json, datetime, re, os, unicodedata
from random import choice

### twython ###
from twython import Twython, TwythonError
from twython import TwythonStreamer

### db stuff  ###
import psycopg2
import urlparse

### GET KEYS  #########################################################################

### heroku ###

TWIT_KEY = os.environ['TWIT_KEY']
TWIT_SECRET = os.environ['TWIT_SECRET']
OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['OAUTH_TOKEN_SECRET']

twitter = Twython(TWIT_KEY, TWIT_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
twitter.verify_credentials()

### DATABASE CONNECTION ################################################################


urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

try:

	con = psycopg2.connect(
	    database=url.path[1:],
	    user=url.username,
	    password=url.password,
	    host=url.hostname,
	    port=url.port
	)
	cur = con.cursor()
except psycopg2.DatabaseError, e:
	if con:
		con.rollback()
	print 'Error %s' % e


### HORRORSCOPE RESPONSE STREAM ##########################################################

class oracleStream(TwythonStreamer):

	def oracleSays(self):
		cur.execute("SELECT * FROM Readings ORDER BY RANDOM() LIMIT 1;") 
		rows = cur.fetchall()
		fetchedR = rows[0][1]
		print fetchedR
		return fetchedR

	def oracleDefers(self):
		cur.execute("SELECT * FROM Deferrs ORDER BY RANDOM() LIMIT 1;")
		rows = cur.fetchall()
		fetchedD = rows[0][1]
		print fetchedD
		return fetchedD


	def on_success(self, data): 

		if 'text' in data:
			### get your data
			body = data['text'].encode('utf-8')
			user = data['user']['screen_name'].encode('utf-8')

			### set your command signs and account
			command = "reading"
			signs = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn"]
			acct = "@horrible_scope"

			#### TWEET A READING TO A USER  ######################################

			### if tweet starts with the account AND contains the word reading ###
			if body.startswith(acct) and command in body:
				### strip the text
				bodyStrip = re.sub(r'[^\w\s]','',body.lower())

				### get your reading
				reading = self.oracleSays()
				
				### check which sign it is
				sign = '' 
				for s in signs:
					if s in bodyStrip:
						sign = '#%s' % s
				toTweet = "@%s: %s %s" % (user, reading, sign)
				print toTweet

				### tweet back a reading
				try:
					twitter.update_status(status=toTweet)
				except TwythonError as e:
					print e
			
			### TWEET A DEFERRAL TO A USER ##################################

			### else if the body starts w/ the account but has no command. 

			elif body.startswith(acct) and command not in body:
				### get a deferral
				defR = self.oracleDefers()
				toNope = "@%s: %s" % (user, defR)
				print toNope

				### tweet the deferral
				try:
					twitter.update_status(status=toNope)
				except TwythonError as e:
					print e

			### If neither of these are met....do nothing ###################
			else:
				print "Neither condition was met. Do nothing."
				
					
	def on_error(self, status_code, data):
		print status_code


OrcStream = oracleStream(TWIT_KEY, TWIT_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
OrcStream.statuses.filter(track="@horrible_scope") #only works if you are public
