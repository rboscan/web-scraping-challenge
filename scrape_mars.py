from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from splinter import Browser
import pandas as pd


def init_browser():

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    return browser

def scrape():

    browser = init_browser()
    
    mars_dict={}

    mars_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    #Parse url with splinter and beautifulsoup

    browser.visit(mars_url)
    mars_html = browser.html
    soup = bs(mars_html, 'lxml')

    #Most recent article from Mars website

    recent_article = soup.find('div',class_='content_title').a.text
    mars_dict['recent.article'] = recent_article
    
    recent_teaser = soup.find('div', class_='article_teaser_body').text
    mars_dict['recent.teaser'] = recent_teaser
    
    # Change URL to JPL website

    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    # Parse url with splinter and beautifulsoup

    jpl_html = browser.html
    soup = bs(jpl_html, 'lxml')

    # Find background image url through the use of splinter and soup, then creating a functioning link to said image in full res.

    jpl_article = soup.find('article').attrs
    jpl_string = jpl_article['style'].split("'")[1]
    featured_image_url = 'https://www.jpl.nasa.gov' + jpl_string
    mars_dict['featured.image'] = featured_image_url

    # Change url to mars weather twitter

    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)

    # Parse website with beautiful soup and splinter

    mars_weather_html = browser.html
    soup = bs(mars_weather_html, 'lxml')

    # Use BeautifulSoup to parse through latest tweet and obtain text without children inside parent tag
    # and then turning the NavigableString object into a python string, as well as removing new lines.

    weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    weather = weather.contents[0]
    weather_string = str(weather)
    current_mars_weather = weather_string.replace('\n','')

    mars_dict['weather'] = current_mars_weather
    # Get URL for Mars Facts and use pandas to scrape the necessary table

    mars_facts_url = "https://space-facts.com/mars/"
    mars_facts = pd.read_html(mars_facts_url)[1].to_html()
    mars_facts = mars_facts.replace('/n','')

    mars_dict['mars.table'] = mars_facts

    # Mars hemisphere url

    mars_hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mars_hemisphere_url)

    mars_hemisphere_html = browser.html
    soup = bs(mars_hemisphere_html, 'lxml')

    hemisphere_thumbs = soup.find_all('div',class_="item")

    base_url = "https://astrogeology.usgs.gov"

    hemispheres = []

    for item in hemisphere_thumbs:
        
        # Finds hemisphere titles from menu
        hemisphere_title = item.h3.text
        hemisphere_title = hemisphere_title.replace(' Enhanced','')
        
        # Finds hemisphere main paige image links and sets them to a variable
        image_link = item.a.get('href')
        image_url = base_url + image_link
        
        # Parses through URL to obtain main image
        browser.visit(image_url)
        url_html = browser.html
        soup = bs(url_html, 'lxml')
        
        parent_url = soup.find('div',class_='downloads').a.get('href')
        
        # Appends dictionary with titles and urls
        hemispheres.append({'title':hemisphere_title, 'img_url':parent_url})
    
    mars_dict['hemispheres'] = hemispheres
    
    browser.quit()
    return mars_dict

