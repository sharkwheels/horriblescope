
### sys stuff ###
import random, sys, json, datetime, re, os, unicodedata
from random import choice

### twython ###
from twython import Twython, TwythonError
from twython import TwythonStreamer

### GET KEYS (LAZY FUCKING LOCAL WAY) #########################################################################

keys = []
with open('twitter.txt','r') as my_file:
	keys = my_file.read().splitlines()

TWIT_KEY = keys[0]
TWIT_SECRET = keys[1]
OAUTH_TOKEN = keys[2]
OAUTH_TOKEN_SECRET = keys[3]

twitter = Twython(TWIT_KEY, TWIT_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

### HORRORSCOPE STUFF ##########################################################

# this is just pulled right off the twython docs: https://twython.readthedocs.org/en/latest/usage/streaming_api.html

class MyStreamer(TwythonStreamer):

	def oracleSays(self):
		sayings = ["one", "two", "three"]
		oneSaying = random.choice(sayings)
		return oneSaying

	def on_success(self, data):

		if 'text' in data:

			body = re.sub(r'[^\w\s]','',data['text'].encode('utf-8').lower()) #sub all the punctuation
			user = data['user']['screen_name'].encode('utf-8')

			command = "reading"
			sign = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn"]

			if command in body:
				reading = self.oracleSays()
				print "body: %s from: %s read: %s" % (body, user, reading) 
				
			else:
				print "I do not understand what you request of me." 
				# do nothing ? 	

	def on_error(self, status_code, data):
		#print status_code
		pass

stream = MyStreamer(TWIT_KEY, TWIT_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
stream.statuses.filter(track='@horrible_scope') 

