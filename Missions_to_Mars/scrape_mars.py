from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import time
import pandas as pd

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)

db = client.mars_db
collection = db.scrape


def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():

    db = client.mars_db
    collection = db.scrape

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'lxml'
    soup = BeautifulSoup(response.text, 'lxml')

    # find articles to scrape
    articles = soup.find_all('div', class_='slide')

    # loop through what was scraped to find the title and paragraph clip for articles
    for article in articles:
        article_title = article.find('div', class_='content_title').text
        paragraph = article.find(
            'div', class_='rollover_description_inner').text

    # url to visit and scrape
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    # click on full image button to scrape the link
    browser.click_link_by_id('full_image')

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # find the image info to scrape
    image_link = soup.find('img', class_='fancybox-image')['src']

    # add the scraped destination for the image to the prefix for the url
    featured_image = ('https://www.jpl.nasa.gov/' + image_link)

    # take html and make into df with str data type
    df = pd.read_html(str('http://space-facts.com/mars/'))[0]

    # clean up columns in df
    df.columns = ['Description', 'Mars']

    table_html = df.to_html()

    url4 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url4)

    # identify links for each hemisphere to click
    links = browser.links.find_by_partial_text("Hemisphere")

    # loop through each hemisphere link
    for i in range(len(links)):

        browser.links.find_by_partial_text("Hemisphere")[i].click()

        time.sleep(1)

        html = browser.html

        soup = BeautifulSoup(html, 'html.parser')

        # find & scrape info where image location is nested
        images = soup.find_all('div', class_='downloads')

        browser.back()

        # loop through what was scraped and pull out the img url and title
        for image in images:
            ul = image.find('ul')
            li = ul.find('li')
            link = li.find('a')
            img_url = link['href']

        title = soup.find('h2', class_='title').text

    mars_dict = {
        'article_title': article_title,
        'paragraph': paragraph,
        'image': featured_image,
        'title': title,
        'img_url': img_url,
        'table_html': table_html
    }
    # {{mars.df_html|safe}} - for displaying html from mongo

    collection.insert_one(mars_dict)

    browser.quit() 

    return mars_dict

    print("Data Uploaded!")
