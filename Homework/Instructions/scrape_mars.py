#!/usr/bin/env python
# coding: utf-8



from splinter import Browser
from bs4 import BeautifulSoup
import re
import time
import pandas as pd


def scrape_info():


  browser=Browser('chrome')

  mars={}
  url = 'https://mars.nasa.gov/news/'
  browser.visit(url)



  soup=BeautifulSoup(browser.html, 'html.parser')
  results = soup.find_all('div', class_="content_title")
  results= results[1]
  news_title=results.a.text




  results = soup.find('div', class_="article_teaser_body").text
  news_para=results




  mars["news_title"]=news_title
  mars["news_p"]=news_para


  # In[7]:


  mars


  # In[8]:


  url= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars" 
  browser.visit(url)


  # In[9]:


  browser.find_by_id('full_image').click()
  browser.find_link_by_partial_text('more info').click()
  soup = BeautifulSoup(browser.html, 'html.parser')
  result=soup.find('figure',class_="lede")
  featured_image_url="https://www.jpl.nasa.gov"+result.a.img["src"]
  mars["featured_image"]=featured_image_url
  mars["featured_image"]        





  df=pd.read_html('https://space-facts.com/mars/')[0]
  df.columns=['description', 'value']
  df.set_index('description', inplace=True)
  df


  df.to_html()

  html_table = df.to_html()
  html_table=html_table.replace('\n', '')
  mars['facts'] = html_table



  mars




  url = 'https://twitter.com/marswxreport?lang=en'
  browser.visit(url)
  time.sleep(5)
  html = browser.html
  weather_soup = BeautifulSoup(html, 'html.parser')





  pattern = re.compile(r'sol')
  mars_weather = weather_soup.find('span', text=pattern).text
  mars_weather




  mars["weather"] = mars_weather





  url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
  browser.visit(url_hemi)    
  time.sleep(5)       
  usgs_soup = BeautifulSoup(browser.html, 'html.parser')
  headers = []
  titles = usgs_soup.find_all('h3')  
  time.sleep(5)
  for title in titles: 
    headers.append(title.text)
  images = []
  count = 0
  for thumb in headers:
      browser.find_by_css('img.thumb')[count].click()
      images.append(browser.find_by_text('Sample')['href'])
      browser.back()
      count = count+1
  hemisphere_image_urls = []  #initialize empty list to collect titles
  counter = 0
  for item in images:
      hemisphere_image_urls.append({"title":headers[counter],"img_url":images[counter]})
      counter = counter+1
  # closeBrowser(browser)
  browser.back()
  time.sleep(1)
  mars["hemisphere"]=hemisphere_image_urls
  print(hemisphere_image_urls)





  return mars
if __name__ == "__main__":
  print(scrape_info())






