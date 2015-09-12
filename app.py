### IMPORTS ####################################################################

### flask ###

from flask import Flask, render_template, request, redirect, url_for, flash

import bot

### FLASK SETUP  ####################################################################
app = Flask(__name__, static_folder='static',static_url_path='/static')
app.config['DEBUG'] = True
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
app.config.from_pyfile('keys.cfg')
app.secret_key = app.config['APP_KEY']

### APP VIEWS ####################################################################

@app.route("/",methods=['GET','POST'])

def main():
	# maybe I'll make a "X number of people served"
	# display the latest tweet or something
	# a little about this tiny app
	pass


### RUN IT ####################################################################

if __name__ == '__main__': # If we're executing this app from the command line
    app.run("127.0.0.1", port = 3000, debug=True, use_reloader=False)
