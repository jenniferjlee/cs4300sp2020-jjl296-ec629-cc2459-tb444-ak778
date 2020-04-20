import praw
import pandas as pd
import json
import datetime as dt
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import newspaper
from newspaper import Article 
import re
from newspaper import Config
import random
import requests
import datetime

def get_date(created):
    return dt.datetime.fromtimestamp(created)

# Get 50 articles per month from this from UpliftingNews
# Epoch dates (Jan 2015-Jan2019)

before_dates = [] #28th of each month
after_dates = [] #1st of each month

# subreddit created in 2012
# years = [2013, 2014, 2015, 2016, 2017, 2018, 2019]
# years = [2020]

for year in years:
  for month in range(1,5):
    b_date = str(year) + "-" + str(month) + "-" + "28"
    a_date = str(year) + "-" + str(month) + "-" + "1"
    b_timestamp = int(time.mktime(datetime.datetime.strptime(b_date, "%Y-%m-%d").timetuple()))
    a_timestamp = int(time.mktime(datetime.datetime.strptime(a_date, "%Y-%m-%d").timetuple()))
    before_dates.append(str(b_timestamp))
    after_dates.append(str(a_timestamp))

posts = []

for index,before_date in enumerate(before_dates):
  after_date = after_dates[index]
  scrape = 'https://api.pushshift.io/reddit/search/submission/?subreddit=upliftingnews&before=' + before_date + '&after=' + after_date + '&size=50'

  r = requests.get(scrape)
  r_json = r.json()

  for article in r_json['data']:
    title = article['title']
    created = article['created_utc']
    
    date = get_date(created)
    year = date.year
    month = date.month
    day = date.day
    date_formatted = str(year) + "-" + str(month) + "-" + str(day)

    thumbnail = article['thumbnail']
    url = article["url"]
    score = article["score"]
    comments = article["num_comments"]

    #to get past the 403 errors
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
    config = Config()
    config.browser_user_agent = user_agent
    page = Article(url, config=config)
    
    try:
      page.download()
      page.parse()
      transcript = page.text

      posts.append({'title': title, 'score': score, 'url': url, 
      'comments': comments, 'date':date_formatted, 'transcript': transcript,
      'source': 'reddit.com/r/UpliftingNews', 'thumbnail': thumbnail})
      
    except:
      print('***FAILED TO DOWNLOAD AND ADD***', url)
      continue

with open('REDOLD.json', 'w') as json_file:
    json.dump(posts, json_file)