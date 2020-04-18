#!/usr/bin/python3

import praw
import requests
import urllib.request
import datetime as dt
import time
import numpy as np
from bs4 import BeautifulSoup
import pandas as pd
import json


def tag2md(tag):
    if tag.name == 'p':
        return tag.text
    elif tag.name == 'h1':
        return f'{tag.text}\n{"=" * len(tag.text)}'
    elif tag.name == 'h2':
        return f'{tag.text}\n{"-" * len(tag.text)}'
    elif tag.name in ['h3', 'h4', 'h5', 'h6']:
        return f'{"#" * int(tag.name[1:])} {tag.text}'
    elif tag.name == 'pre':
        return f'```\n{tag.text}\n```'


reddit = praw.Reddit(client_id='VQCjkp30UcsrPQ',
                     client_secret='6vJ9buTBEKVr1gPW6s2ztUYl1aU', user_agent='test')

posts = []
subreddit = reddit.subreddit('UpliftingNews').hot(limit=100)
for post in subreddit:
    temp = {}
    temp['title'] = post.title
    temp['score'] = post.score
    temp['num_comments'] = post.num_comments
    temp['url'] = post.url
    posts.append(temp)
print(len(posts))
for post in posts:
    url = post['url']
    res = requests.get(url)
    if (res.status_code == 200 and 'content-type' in res.headers and
            res.headers.get('content-type').startswith('text/html')):
        html = res.text
    # content = response.content
        soup = BeautifulSoup(html, "html.parser")
        h1 = soup.body.find('h1')
        root = h1
        if root is None:
            break
        while root.name != 'body' and len(root.find_all('p')) < 5:
            root = root.parent
        if (len(root.find_all('p')) < 5):
            break
        ps = root.find_all(['h2', 'h3', 'h4', 'h5', 'h6', 'p', 'pre'])
        ps.insert(0, h1)
        content = [tag2md(p) for p in ps]
        post['transcript'] = content
# json_dump = json.dumps(posts)
with open('reddit.json', 'w') as json_file:
    json.dump(posts, json_file)
# print(json_dump)

# print({'title': h1.text, 'content': content})

# body = soup.find_all('p')
# print(body)
# x = body[0].find_all('p')
# print(x)
# # list_paragraphs = []
# # for p in np.arange(0, len(x)):
# #     # print(p)
# #     paragraph = x[p].get_text()
# #     list_paragraphs.append(paragraph)
# #     final_article = " ".join(list_paragraphs)
# break

# print(posts)
