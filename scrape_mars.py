
# coding: utf-8

# In[1]:

# Dependencies
import requests as requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import requests

# Module Dependency
import pymongo
import datetime

# Import Flask
from flask import Flask
app = Flask(__name__)



# Define static routes
# scrape different websites and load database

def scrape():
	# import details to a python dictionary
	# Nasa Mars News
# Create a connection to our database
	# conn = 'mongodb://db_user:admin@ds143245.mlab.com:43245/heroku_hsr9k4sx'
	conn = "mongodb://localhost:27017"
	client = pymongo.MongoClient(conn)

	# define datbase and collection
	db = client.mars_db
	mars_info = db.mars_db

	news = get_mars_news_title()
	print(news)

	# featured image
	featured_image = get_mars_featured_image()
	print(featured_image)

	# mars weather
	mars_weather = get_mars_weather()
	print(mars_weather)

	# mars facts
	mars_facts_filename = get_mars_facts()
	htmlFile = open(mars_facts_filename, 'r')
	marsHtml = htmlFile.read()
	print(marsHtml)

	mars_hemisphere = get_mars_hemisphere()
	print(mars_hemisphere)

	# post = {
	#     "news": news,
	#     "featured_image":featured_image,
	#     # "mars_facts": mars_facts_filename,
	#     "mars_weather": mars_weather,
	#     # "mars_facts": marsHtml,
	#     # "mars_hemisphere": mars_hemisphere,
	#     'date': datetime.datetime.utcnow()
	#   }

	print("done")

	# db.mars_info.insert_one(post)

def get_mars_news_title():
    # URL of page to scrape
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page 
    response = requests.get(url)

    # Create Beautiful Soup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')

    latest_news = soup.body.find('div', class_='slide')

    # find title and text
    title = latest_news.find('div', class_="content_title")
    text = latest_news.find('div', class_="rollover_description_inner")

    # return a dictionary 
    news = {"title": title.text.strip(),
            "text": text.text.strip()}

    return news


def get_mars_featured_image():
	executable_path = {'executable_path': 'chromedriver.exe'}
	browser = Browser('chrome', **executable_path)
	base_url = 'https://www.jpl.nasa.gov'
	url = '%s/spaceimages/?search=&category=Mars' % base_url
	browser.visit(url)


	html = browser.html
	soup = bs(html, 'html.parser')

	# click FULL IMAGE to get medium image
	browser.click_link_by_partial_text('FULL IMAGE')

	time.sleep(5)

	html = browser.html
	soup = bs(html, 'html.parser')

	# click more info to get larger size
	browser.click_link_by_partial_text('more info')
	# browser.find_link_by_partial_text('more info').click()


	html = browser.html
	soup2 = bs(html, 'html.parser')

	# mars_large_url = soup.find('a', 'href')
	images = soup2.find('figure', class_='lede')
	mars_large = images.a['href']
	mars_link = '%s%s' % (base_url, mars_large)


	return mars_link

def get_mars_weather():
	url = 'https://twitter.com/marswxreport?lang=en'

	# Retrieve page 
	response = requests.get(url)

	# Create Beautiful Soup object; parse with 'html.parser'
	soup = bs(response.text, 'html.parser')


	content = soup.find('div', class_='content')
	mars_weather = soup.find('div', 'js-tweet-text-container')

	return mars_weather.text.strip()


def get_mars_facts():
	url = 'https://space-facts.com/mars/'

	# Retrieve page 
	response = requests.get(url)

	# Create Beautiful Soup object; parse with 'html.parser'
	soup = bs(response.text, 'html.parser')


	rows = soup.find_all('tr')

	names = []
	values = []

	for r in rows:
	    name = r.find('td', class_='column-1')
	    value = r.find('td', class_='column-2')
	    names.append(name.text.strip())
	    values.append(value.text.strip())

	facts_df = pd.DataFrame ({"name": names,
	               "value": values})

	facts_df.set_index("name", inplace=True)

	facts_html = facts_df.to_html("Mars_facts.html")
	url = 'https://space-facts.com/mars/'

	# Retrieve page 
	response = requests.get(url)

	# Create Beautiful Soup object; parse with 'html.parser'
	soup = bs(response.text, 'html.parser')


	rows = soup.find_all('tr')

	names = []
	values = []

	for r in rows:
	    name = r.find('td', class_='column-1')
	    value = r.find('td', class_='column-2')
	    names.append(name.text.strip())
	    values.append(value.text.strip())

	facts_df = pd.DataFrame ({"description": names,
	               "value": values})

	facts_df.set_index("description", inplace=True)
	facts_df.to_html("Mars_facts.html")

	# pass name of html file created
	return "Mars_facts.html"

def get_mars_hemisphere():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)

    # array list
    image_urls = []
    image_titles = []
    hempisphere_image_urls = []

    #  scrape all refernces to images in page
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = bs(html, 'html.parser')	

    pictures = soup.find_all('a', class_="item product-item")
    for p in pictures:    
        image_urls.append("https://astrogeology.usgs.gov%s" % p['href'])  
        
        #  find title of image
        image_titles.append(p.find('div', class_="description").h3.text)


    # read each page reference and capture large image 
    for i, t in zip(image_urls, image_titles):
        try:
            # click to get enhanced image
            response = requests.get(i)

            soup = bs(response.text, 'lxml')            
            
            title = t

            # find url of image
            mars_images = soup.find('img', class_='wide-image',attrs={'src':True})
            image_url = "https://astrogeology.usgs.gov%s" % mars_images['src'].strip()    

            url_dict = {"title":title, "image_url":image_url}
            hempisphere_image_urls.append(url_dict)
        except Exception as e:
            print(e)	# return dictionary of mars hemisphere 
    return hempisphere_image_urls
