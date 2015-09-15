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

"""
#local

keys = []
with open('twitter.txt','r') as my_file:
	keys = my_file.read().splitlines()

TWIT_KEY = keys[0]
TWIT_SECRET = keys[1]
OAUTH_TOKEN = keys[2]
OAUTH_TOKEN_SECRET = keys[3]
"""

twitter = Twython(TWIT_KEY, TWIT_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

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

### HORRORSCOPE IDLE (Every Hour on Scheduler) ##########################################################

def timedTweet():
	cur.execute("SELECT * FROM Idle ORDER BY RANDOM() LIMIT 1;")
	rows = cur.fetchall()
	timedR = rows[0][1]
	try:
		twitter.update_status(status=timedR)
		print timedR
	except TwythonError as e:
		print e

	
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
			body = re.sub(r'[^\w\s]','',data['text'].encode('utf-8').lower()) #sub all the punctuation, make it all lower case
			user = data['user']['screen_name'].encode('utf-8')

			command = "reading"
			signs = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn"]

			if command in body:
				reading = self.oracleSays()
				sign = '' 
				for s in signs:
					if s in body:
						sign = '#%s' % s
				toTweet = ".@%s: %s %s" % (user, reading, sign)
				print toTweet
				
				try:
					twitter.update_status(status=toTweet)
				except TwythonError as e:
					print e
				
			else:
				defR = self.oracleDefers()
				toNope = ".@%s: %s" % (user, defR)
				print toNope
				
				try:
					twitter.update_status(status=toNope)
				except TwythonError as e:
					print e
				
					
	def on_error(self, status_code, data):
		#print status_code
		pass

OrcStream = oracleStream(TWIT_KEY, TWIT_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
OrcStream.statuses.filter(track='@horrible_scope') #only works if you are public
