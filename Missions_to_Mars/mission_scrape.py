from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo


def init_browser():
    executable_path = {'executable_path': '/Users/philipwewiora/Downloads/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    articles = {}
    
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    articles['title'] = soup.find('div', class_='content_title').get_text()
    articles['paragraph'] = soup.find('div', class_= 'article_teaser_body').get_text()
    
    return articles
    