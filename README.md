

```python
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
```

## Nasa Mars News


```python
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
```

## JPL Mars Space Images - Featured Image


```python
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
    
    images = soup2.find('figure', class_='lede')
    mars_large = images.a['href']
    mars_link = '%s%s' % (base_url, mars_large)

    return mars_link
```

## Mars Weather


```python
def get_mars_weather():
    url = 'https://twitter.com/marswxreport?lang=en'

    # Retrieve page 
    response = requests.get(url)

    # Create Beautiful Soup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')


    content = soup.find('div', class_='content')
    mars_weather = soup.find('div', 'js-tweet-text-container')
    return mars_weather.text.strip()

```

## Mars Facts


```python
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

    facts_df = pd.DataFrame ({"name": names,
                   "value": values})

    facts_df.set_index("name", inplace=True)
    facts_df.to_html("Mars_facts.html")

    # return link to html
    return("Mars_facts.html")   
```

## Mars Hemispheres


```python
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
```


```python
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# define datbase and collection
db = client.mars_db
mars_info = db.mars_db

# mars news
news = get_mars_news_title()
print(news['title'])
print(news['text'])

# featured image
featured_image = get_mars_featured_image()
print(featured_image)

# mars weather
mars_weather = get_mars_weather()

# mars facts
mars_facts_filename = get_mars_facts()
htmlFile = open(mars_facts_filename, 'r')
marsHtml = htmlFile.read() 
print(marsHtml)

# mars hemispherses
mars_hemisphere = get_mars_hemisphere()

post = {
    "news": news,
    "featured_image":featured_image,
#     "mars_facts": mars_facts_filename,
    "mars_weather": mars_weather,
    "mars_facts": marsHtml,
    "mars_hemisphere": mars_hemisphere,
    'date': datetime.datetime.utcnow()
  }



db.mars_info.insert_one(post)
```

    Martian Ridge Brings Out Rover's Color Talents
    On a part of "Vera Rubin Ridge" where rover-team researchers sought to determine whether dust coatings are hiding rocks' hematite content, the Mast Camera (Mastcam) on NASA's Curiosity Mars rover took this image of a rock surface that had been brushed with the rover's Dust Removal Tool.
    https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16837_hires.jpg
    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>value</th>
        </tr>
        <tr>
          <th>name</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>Equatorial Diameter:</th>
          <td>6,792 km</td>
        </tr>
        <tr>
          <th>Polar Diameter:</th>
          <td>6,752 km</td>
        </tr>
        <tr>
          <th>Mass:</th>
          <td>6.42 x 10^23 kg (10.7% Earth)</td>
        </tr>
        <tr>
          <th>Moons:</th>
          <td>2 (Phobos &amp; Deimos)</td>
        </tr>
        <tr>
          <th>Orbit Distance:</th>
          <td>227,943,824 km (1.52 AU)</td>
        </tr>
        <tr>
          <th>Orbit Period:</th>
          <td>687 days (1.9 years)</td>
        </tr>
        <tr>
          <th>Surface Temperature:</th>
          <td>-153 to 20 °C</td>
        </tr>
        <tr>
          <th>First Record:</th>
          <td>2nd millennium BC</td>
        </tr>
        <tr>
          <th>Recorded By:</th>
          <td>Egyptian astronomers</td>
        </tr>
      </tbody>
    </table>
    




    <pymongo.results.InsertOneResult at 0x20ade596f88>




```python
results = list(db.mars_info.find().sort('date',pymongo.DESCENDING).limit(1))[0]
print(results)
```

    {'_id': ObjectId('5a0546895976e3360c0fade6'), 'news': {'title': "Martian Ridge Brings Out Rover's Color Talents", 'text': 'On a part of "Vera Rubin Ridge" where rover-team researchers sought to determine whether dust coatings are hiding rocks\' hematite content, the Mast Camera (Mastcam) on NASA\'s Curiosity Mars rover took this image of a rock surface that had been brushed with the rover\'s Dust Removal Tool.'}, 'featured_image': 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16837_hires.jpg', 'mars_weather': 'Sol 1868 (Nov 07, 2017), Sunny, high -24C/-11F, low -80C/-112F, pressure at 8.48 hPa, daylight 05:55-17:38', 'mars_facts': '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>value</th>\n    </tr>\n    <tr>\n      <th>name</th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Equatorial Diameter:</th>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <th>Polar Diameter:</th>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <th>Mass:</th>\n      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n    </tr>\n    <tr>\n      <th>Moons:</th>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <th>Orbit Distance:</th>\n      <td>227,943,824 km (1.52 AU)</td>\n    </tr>\n    <tr>\n      <th>Orbit Period:</th>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <th>Surface Temperature:</th>\n      <td>-153 to 20 °C</td>\n    </tr>\n    <tr>\n      <th>First Record:</th>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>Recorded By:</th>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>', 'mars_hemisphere': [{'title': 'Cerberus Hemisphere Enhanced', 'image_url': 'https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg'}, {'title': 'Schiaparelli Hemisphere Enhanced', 'image_url': 'https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg'}, {'title': 'Syrtis Major Hemisphere Enhanced', 'image_url': 'https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg'}, {'title': 'Valles Marineris Hemisphere Enhanced', 'image_url': 'https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg'}], 'date': datetime.datetime(2017, 11, 10, 6, 26, 17, 642000)}
    


```python
results['mars_facts']
```




    '<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>value</th>\n    </tr>\n    <tr>\n      <th>name</th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Equatorial Diameter:</th>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <th>Polar Diameter:</th>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <th>Mass:</th>\n      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n    </tr>\n    <tr>\n      <th>Moons:</th>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <th>Orbit Distance:</th>\n      <td>227,943,824 km (1.52 AU)</td>\n    </tr>\n    <tr>\n      <th>Orbit Period:</th>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <th>Surface Temperature:</th>\n      <td>-153 to 20 °C</td>\n    </tr>\n    <tr>\n      <th>First Record:</th>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>Recorded By:</th>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>'


