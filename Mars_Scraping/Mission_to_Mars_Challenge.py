#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import the dependencies
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


# Set up executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Visit the Mars NASA news site
# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[4]:


# Set up html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[5]:


# Begin Scraping
slide_elem.find('div', class_='content_title')


# In[6]:


# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[7]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[8]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[9]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[10]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[11]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[12]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts 

# In[13]:


# Use Pandas to create a DataFrame from website data table
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[14]:


# Convert DataFrame back to html for the web app
df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[15]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(url)


# In[16]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []
images = browser.find_by_css('a.product-item h3')

for image in range(len(images)):
    #create empty dictionary
    hemispheres = {}
    #a) click on each hemisphere link
    browser.find_by_css('a.product-item h3')[image].click()
    # b) navigate to the full-resolution image page
    element = browser.find_link_by_text('Sample').first
    # c) retrieve the full-resolution image URL string
    img_url = element['href']
    # c) retrieve the full-resolution image Title
    title = browser.find_by_css("h2.title").text
    # Save the full-resolution image URL string as the value for the img_url key 
    hemispheres["img_url"] = img_url
    # Save the hemisphere image title as the value for the title key
    hemispheres["title"] = title
    # Add the dictionary with the image URL string and the hemisphere image title to the list
    hemisphere_image_urls.append(hemispheres)
    # d) Use browser.back() to navigate back to the beginning to get the next hemisphere image
    browser.back()


# In[17]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[18]:


# End Session
browser.quit()

