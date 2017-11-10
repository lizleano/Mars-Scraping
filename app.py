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
def get_mars_info():
	# Create a connection to heroku mongodb database
	client = pymongo.MongoClient("mongodb://admin:adminadmin@ds143245.mlab.com:43245/heroku_hsr9k4sx")
	db = client.heroku_hsr9k4sx
	

    # Create a connection to localhost
	# conn = "mongodb://localhost:27017"
	# client = pymongo.MongoClient(conn)
	# db = client.mars_db


	# Create a connection and database
	# conn = "mongodb://localhost:27017"
	# client = pymongo.MongoClient(conn)
	# db = client.mars_db


	mars_info = db.mars_db
	results = list(db.mars_info.find().sort('date',pymongo.DESCENDING).limit(1))

	return results


@app.route("/")
def index():
	results = get_mars_info()
	print(len(results))
	if len(results) == 0:
		return render_template("default.html")
	else:
		return render_template("index.html", mars=results[0])


@app.route("/scrape")
def mars_scrape():
	"""Return a list of all passenger names"""
	# Query all passengers
	scrape()
	results = get_mars_info()
	return render_template("index.html", mars=results[0]) 


if __name__ == '__main__':
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(debug=True)
