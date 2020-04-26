import os
import json
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
import re
import numpy as np
import math
import nltk

# data_file_name = "total_data.json"

def load_json_file(name):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, name)
    with open(file_path, encoding = 'utf-8') as json_file:
        data = json.load(json_file)
    return data

# data = load_json_file(data_file_name)
# num_articles = len(data)
# print('pre-processing: ' + str(num_articles) + ' articles loaded')

# articles = []

# remove duplicate articles (a lot seem to be in goodnewsnetwork my b)
# seen = []
# for post in data:
#   if post['title'] not in seen:
#     articles.append(post)
#     seen.append(post['title'])

# with open('cleaned_total_data.json', 'w') as json_file:
#     json.dump(articles, json_file)

# data2 = load_json_file('cleaned_total_data.json')
# num_articles2 = len(data2)
# print('post-processing: ' + str(num_articles2) + ' articles loaded')


# with open('final_data.json', 'w') as json_file:
#     json.dump(total_articles, json_file)

def main():
    # finaldata = load_json_file('final_data.json')
    # num_articles = len(finaldata)
    # print(num_articles)

    # #combine all data sets to one final one
    # total_articles = []

    # extraData1 = load_json_file('moreReddit.json')

    # for post in finaldata:
    #     total_articles.append(post)
    # for post in extraData1:
    #     total_articles.append(post)
  
    
    # with open('cleanthis.json', 'w') as json_file:
    #     json.dump(total_articles, json_file)

    #remove dups
    articles = []
    seen = []
    data = load_json_file('cleanthis.json')
    for post in data:
        if post['title'] not in seen:
            articles.append(post)
            seen.append(post['title'])

        with open('lang.json', 'w') as json_file:
            json.dump(articles, json_file)


if __name__ == "__main__":
    main()

