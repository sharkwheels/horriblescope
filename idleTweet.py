from twython import Twython, TwythonError
### db stuff  ###
import psycopg2
import urlparse
import os

### HORRORSCOPE IDLE (Every Hour on Scheduler) ##########################################################

TWIT_KEY = os.environ['TWIT_KEY']
TWIT_SECRET = os.environ['TWIT_SECRET']
OAUTH_TOKEN = os.environ['OAUTH_TOKEN']
OAUTH_TOKEN_SECRET = os.environ['OAUTH_TOKEN_SECRET']

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
	cur.execute("SELECT * FROM Idle ORDER BY RANDOM() LIMIT 1;")
	rows = cur.fetchall()
	timedR = rows[0][1]

	print "fetched idle status"
	print timedR

	
	try:
		twitter.update_status(status=timedR)
		print "tweeted!"
	except TwythonError as e:
		print e
	

except psycopg2.DatabaseError, e:
	if con:
		con.rollback()
	print 'Error %s' % e
finally:
	if con:
		con.close()
		print "closing connection"