# Module Dependency
import pymongo
import datetime
from flask import Flask, jsonify,render_template
from scrape_mars import *

# Import Flask
from flask import Flask

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def mars_info():
	# Create a connection
	conn = "mongodb://localhost:27017"
	# conn = 'mongodb://db_user:admin@ds143245.mlab.com:43245/heroku_hsr9k4sx'
	client = pymongo.MongoClient(conn)

	# define datbase and collection
	db = client.mars_db
	mars_info = db.mars_db
	results = list(db.mars_info.find().sort('date',pymongo.DESCENDING).limit(1))[0]
	
	return render_template("index.html", mars=results)


@app.route("/scrape")
def mars_scrape():
	"""Return a list of all passenger names"""
	# Query all passengers
	scrape()
	mars_info()   


if __name__ == '__main__':
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(debug=True)
