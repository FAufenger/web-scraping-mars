#!/usr/bin/env python
# coding: utf-8

# ## Mission to Mars

# In[1]:


# Import dependencies
import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser
import time


# In[2]:


# Choose the executable path to driver 
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=True)


# ### NASA Mars News

# Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

# In[3]:


# Open desired site in browser with splinter
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Added time to allow page to fully load
time.sleep(3)


# In[4]:


# HTML Object
html = browser.html
# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')


# In[5]:


# Retrieve the latest element that contains news title and news_paragraph
results = soup.find('li', class_="slide")

# Extract first title and paragraph, and assign to variables
news_title = results.find('div', class_='content_title').text
news_p = results.find('div', class_='article_teaser_body').text
news_date = results.find('div', class_='list_date').text

# Print results
print(f'Article date: {news_date}')
print(f'Title: {news_title}')
print(f'Abstract: {news_p}')


# ### JPL Mars Space Images - Featured Image

# In[6]:


# Visit the url for JPL Featured Space Image.
#Use splinter to navigate the site and find the image url for the current Featured Mars Image 
image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html#'
browser.visit(image_url)


# In[7]:


# HTML Object
html = browser.html
# Parse HTML with Beautiful Soup
soup = BeautifulSoup(html, 'html.parser')


# In[8]:


# Locate image with splinter
image_tag = soup.find('img', class_='headerimage')
image_location = image_tag.get('src')

# Combine base url with uri
featured_image_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{image_location}'
# Show address in full
featured_image_url


# ### Mars Facts

# In[9]:


# Use Pandas to scrape data
mars_facts_url = 'https://space-facts.com/mars/'
# Take first table for Mars facts
mars_facts_df = pd.read_html(mars_facts_url)[0]
# Print sample of df 
print(mars_facts_df)


# In[10]:


# Clean:
# Column names
mars_facts_df.columns=["Description", "Mars"]

# Table for viewing
mars_facts_df.set_index("Description", inplace=True)

# Show df
mars_facts_df


# In[11]:


# Convert table to html
mars_table_html = mars_facts_df.to_html(index=True, header=True, border=0, justify="left")
mars_table_html.replace("\n","")
print(mars_table_html)


# In[12]:


# Used below code to save fil3e
mars_facts_df.to_html('mars_table_html', index=True, header=True, border=0, justify="left")


# ### Mars Hemispheres

# In[13]:


# Visit Mars hemispheres website
usgs_astrogeology_mars_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

#Use splinter to navigate the site and find the image url for the current Featured Mars Image 
browser.visit(usgs_astrogeology_mars_url)


# In[14]:


# HTML Object
landing_html = browser.html
# Parse HTML with Beautiful Soup
soup = BeautifulSoup(landing_html, 'html.parser')


# In[15]:


# Create a list to store our dictionaries
hemisphere_image_urls = []
# Set base url to add to extension later
hemisphere_base_url = 'https://astrogeology.usgs.gov/'
#Look on developer tool and find where each hemisphere is stored
hemisphere_locate = soup.find_all('div', class_='item')
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
    # Looked on click page to fnd where full res image is stored
    image_partial_url = soup.find('img', class_='wide-image')['src']
    # combine partial and pre url
    img_url = hemisphere_base_url + image_partial_url
    # Append list with title and full size url to hemisphere_image_urls using a Python dictionary
    hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    
    # Add count
    count += 1
    
    # If not last search navigate back before starting loop over
    if len(hemisphere_locate) > count:
        browser.back()
        time.sleep(1)
    # Help save time by cutting last back and sleep
    else:
        break
        
# Print list of dictionaries
hemisphere_image_urls


# In[16]:


browser.quit()

