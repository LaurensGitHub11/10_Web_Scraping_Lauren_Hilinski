from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd

def scrape():

    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    news_response = requests.get(news_url)
    news_soup = bs(news_response.text, 'lxml')
    news_title = news_soup.select(".content_title")[0].text
    news_paragraph = news_soup.select('.rollover_description_inner')[0].text

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    nasa_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(nasa_url)
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, 'html.parser')
    browser.is_element_present_by_text("FULL IMAGE", wait_time=1)
    browser.click_link_by_partial_text("FULL IMAGE")
    browser.is_element_present_by_text("more info", wait_time=1)
    browser.click_link_by_partial_text("more info")
    time.sleep(2)
    nasa_html = browser.html
    nasa_soup = bs(nasa_html, 'html.parser')
    figure = nasa_soup.select('figure.lede a')[0]['href']
    url_front = 'https://www.jpl.nasa.gov'
    featured_image_url = url_front+figure

    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    twitter_html = browser.html
    twitter_soup = bs(twitter_html, 'html.parser')
    mars_weather = twitter_soup.select("p.TweetTextSize.TweetTextSize--normal.js-tweet-text.tweet-text")[0].text

    astro_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astro_url)
    astro_html = browser.html
    astro_soup = bs(astro_html, 'html.parser')
    links_to_click = ["Cerberus Hemisphere Enhanced", "Valles Marineris Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced", "Syrtis Major Hemisphere Enhanced"]
    astro_img_url = []
    astro_title = []
    for x in range(len(links_to_click)):
        browser.is_element_present_by_text(links_to_click[x], wait_time=1)
        browser.click_link_by_partial_text(links_to_click[x])
        astro_html = browser.html
        astro_soup = bs(astro_html, 'html.parser')
        astro_img_url.append(astro_soup.select('div.wide-image-wrapper li a')[0]['href'])
        astro_title.append(astro_soup.select('h2.title')[0].text)
    browser.quit()
    cerberus_dict = {"title": astro_title[0], "img_url": astro_img_url[0]}
    valles_dict = {"title": astro_title[1], "img_url": astro_img_url[1]}
    schiaparelli_dict = {"title": astro_title[2], "img_url": astro_img_url[2]}
    syrtis_dict = {"title": astro_title[3], "img_url": astro_img_url[3]}
    hemisphere_image_urls = [cerberus_dict, valles_dict, schiaparelli_dict, syrtis_dict]

    table_url = "https://space-facts.com/mars/"
    mars_table = pd.read_html(table_url)
    mars_table

    planet_mars = {"current_news_title": news_title, "current_news": news_paragraph, "featured_image": featured_image_url, "mars_weather": mars_weather, "mars_info": "need to update", "hemispheres": hemisphere_image_urls}

    return planet_mars