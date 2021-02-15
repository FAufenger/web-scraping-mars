#!/usr/bin/env python
# coding: utf-8

# Import Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def master_scrape():
    # Start browser
    browser = init_browser()
    # Pause to allows browser to open
    time.sleep(1)
    # Dictionary to hold all desired scraped variables
    mars_news = {}

    ################ NASA Mars News #####################

    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    try:
        # Open desired site in browser with splinter
        url = 'https://mars.nasa.gov/news/'
        browser.visit(url)
        # Added time to allow page to fully load
        time.sleep(3)

        # HTML Object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Retrieve the latest element that contains news title and news_paragraph
        results = soup.find('li', class_="slide")

        # Extract first title and paragraph, and assign to variables
        news_date = results.find('div', class_='list_date').text       
        news_title = results.find('div', class_='content_title').text
        news_p = results.find('div', class_='article_teaser_body').text        

        # Append image to collection dictionary
        mars_news['news_date'] = news_date
        mars_news['news_title'] = news_title
        mars_news['news_abstract'] = news_p
        print('news success')
    except:
        mars_news['news_date'] = '1news_date'
        mars_news['news_title'] = '2news_title'
        mars_news['news_abstract'] = '3news_p'
        print('news failure')

    ############## JPL Mars Space Images - Featured Image ##############

    # Visit the url for JPL Featured Space Image.
    #Use splinter to navigate the site and find the image url for the current Featured Mars Image 
    try:
        image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html#'
        browser.visit(image_url)
        # HTML Object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')
        # Locate image with splinter
        image_tag = soup.find('img', class_='headerimage')
        image_location = image_tag.get('src')
        # Combine base url with uri
        featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_location}'
        
        # Append image to collection dictionary
        mars_news['featured_image_url'] = featured_image_url
        print('space image success')
    except:
        mars_news['featured_image_url'] = '5eatured_image_url'
        print('space image failure')

    ################### Mars Facts ################################

    try:
        # Use Pandas to scrape data
        mars_facts_url = 'https://space-facts.com/mars/'
        # Take first table for Mars facts
        mars_facts_df = pd.read_html(mars_facts_url)[0]
        # Column names
        mars_facts_df.columns=["Description", "Mars"]
        # Table for viewing
        mars_facts_df.set_index("Description", inplace=True)
        # Convert table to html
        mars_table_html = mars_facts_df.to_html(index=True, border=1, header=True, justify="left")
        
        # Append to collection dictionary
        mars_news["mars_table_html"] = mars_table_html
        print('facts success')
    except:
        mars_news["mars_table_html"] = 'mars_7able_htm'
        print('facts failure')

    ##################### Mars Hemispheres ##########################

    try:
        # Visit Mars hemispheres website
        usgs_astrogeology_mars_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        #Use splinter to navigate the site and find the image url for the current Featured Mars Image 
        browser.visit(usgs_astrogeology_mars_url)
        # HTML Object
        landing_html = browser.html
        # Parse HTML with Beautiful Soup
        soup = BeautifulSoup(landing_html, 'html.parser')

        # Set base url to add to extension later
        hemisphere_base_url = 'https://astrogeology.usgs.gov/'
        #Look on developer tool and find where each hemisphere is stored
        hemisphere_locate = soup.find_all('div', class_='item')
        # Create a list to store our dictionaries
        hemisphere_info = []
        # Add a count to shorten overall run time
        count = 0

        # Create for  loop to pull out each hemisphere title and http address
        for title in hemisphere_locate:
            
            # Store title
            title = title.find('h3').text
            # Click on title (link) to find full resolution image
            browser.links.find_by_partial_text(title).click()
            # Use time to delay after click
            time.sleep(1)
            
            # Locate image partial url
            image_html = browser.html
            # Parse HTML with Beautiful Soup
            soup = BeautifulSoup(image_html, 'html.parser')
            # Looked on new page to fnd where full res image is stored
            image_partial_url = soup.find('img', class_='wide-image')['src']
            # combine partial and pre url
            img_url = hemisphere_base_url + image_partial_url
            # Append list with title and full size url to hemisphere_image_urls using a Python dictionary
            hemisphere_info.append({'title' : title, 'img_url' : img_url})
            
            # Add count
            count += 1
            
            # If not last search navigate back before starting loop over
            if len(hemisphere_locate) > count:
                browser.back()
                time.sleep(1)
            # Help save time by cutting last back and sleep
            else:
                break
                
        # List of dictionaries
        mars_news['hemisphere_info'] = hemisphere_info
        print('hemisphere_success')
    except:
        mars_news['hemisphere_info'] ='h3misphere_info' 
        print('hemisphere failure')
    
    # Quit Browser
    browser.quit()
    print('Quitting Browser')

    print('Scraping Complete')
    return mars_news
    