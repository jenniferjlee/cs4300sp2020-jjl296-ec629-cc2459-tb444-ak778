from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import os
import json
import nltk
from nltk import tokenize
import re

# nltk.download('punkt')

def load_json_file(name):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, name)
    with open(file_path, encoding = 'utf-8') as json_file:
        data = json.load(json_file)
    return data

# Steps based off of https://towardsdatascience.com/understand-text-summarization-and-create-your-own-summarizer-in-python-b26a9f09fc70
# 1. Input document
# 2. Rank sentences similarity
# 3. Weigh sentences
# 4. select sentences with higher rank


# return transcript given article_title
def find_transcript(article_title, data):
  for article in data:
    if article['title'] == article_title:
      return article['transcript']

def read_article(transcript):
  return tokenize.sent_tokenize(transcript.rstrip())
    # article = transcript.split(". ")
    # sentences = []
    # for sentence in article:
    #   modified_sentence = sentence.replace("[^a-zA-Z]", " ").split(" ")
    #   sentences.append(modified_sentence2)
    # return sentences

def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
    return 1 - cosine_distance(vector1, vector2)    

def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix

def generate_summary(transcript, top_n=5):
    stop_words = stopwords.words('english')
    summarize_text = []

    sentences =  read_article(transcript)
    sentence_similarity_martix = build_similarity_matrix(sentences, stop_words)
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_martix)
    scores = nx.pagerank(sentence_similarity_graph)
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    # print("Indexes of top ranked_sentence order are ", ranked_sentence)    
    
    for i in range(top_n):
      summarize_text.append(ranked_sentence[i][1])

    return summarize_text

def main2():

    # Load in data
    data_file_name = "final_data1.json"
    data = load_json_file(data_file_name)

    # #   title = "A tiny Colorado town opened its arms to over 700 stranded travelers this weekend"
    # #   title2 = "16-Year-Old Has Been Using His Flying Lessons to Deliver Medical Supplies to Rural Hospitals Fighting COVID"
    title_and_transcripts = []
    for article in data:
        transcript = article['transcript']
        title = article['title']
        summary = generate_summary(transcript, 1)
        seperator = ' '
        summary_string = seperator.join(summary)
        summary_string.encode('ascii', 'ignore')
        summary_string.rstrip()

        # print(summary_string)
        # print('\n')
        print(title)

        title_and_transcripts.append({'title':title, 'summary': summary_string})

    with open('summaries.json', 'w') as json_file:
        json.dump(title_and_transcripts, json_file)

def main3():
    # Load in data
    data_file_name = "summaries.json"
    data = load_json_file(data_file_name)

    new_data = []
    for post in data:
        new_title = post['title'].replace(r"[a-z]+", ' ')
        new_title = (new_title.encode('ascii', 'ignore')).decode("utf-8")
        new_sum = post['summary'].replace(r"[a-z]+", ' ')
        new_sum = (new_sum.encode('ascii', 'ignore')).decode("utf-8")
        new_data.append({'title': new_title, 'summary': new_sum})

    with open('summaries2.json', 'w') as json_file:
        json.dump(new_data, json_file)

# add summaries to final_data1.json
def main4():
    total = []
    data_file_name = "summaries2.json"
    data_summaries = load_json_file(data_file_name)

    data_file_name2 = "final_data1.json"
    data = load_json_file(data_file_name2)
    for i, post in enumerate(data):
        title_name = post['title']
        summary = data_summaries[i]['summary']
        total.append(
            {'title':post['title'], 'url': post['url'],
        'date': post['date'],'transcript': post['transcript'], 'source': post['source'],
        'summary': summary})

    with open('final_data2.json', 'w') as json_file:
        json.dump(total, json_file)
        
# add links to the similar articles
# dictionary: title: [ [title, score, link] ]
# change to dictionary: title {title, score, link }

def get_post_off_title(title, data):
    for post in data:
        post_title = post['title']
        # print('post_title is ' + post_title)
        if post_title == title:
            # print(post)
            return post

def main():
    total = dict()
    data = load_json_file("final_data4.json")
    data_file_name = "similars.json"
    data_summaries = load_json_file(data_file_name)

    for title_key in data_summaries:
        total_similars = []
        similars = data_summaries[title_key]
        for article in similars:
            title = article[0]
            sim = article[1]
            # roudn and make to percentage
            rounded_sim = str(round(sim * 100, 2)) + '%'

            post = get_post_off_title(title, data)
            source = post['source']
            summary = post['summary']
            score = post['score']
            date = post['date']

            total_similars.append({'title': title, 'sim': rounded_sim, 'source': source, 'summary': summary,
            'score': score, 'date': date})
        total[title_key] = total_similars
    
    with open('similars_final.json', 'w') as json_file:
        json.dump(total, json_file)




    # data_file_name2 = "final_data1.json"
    # data = load_json_file(data_file_name2)
    # for i, post in enumerate(data):
    #     title_name = post['title']
    #     summary = data_summaries[i]['summary']
    #     total.append(
    #         {'title':post['title'], 'url': post['url'],
    #     'date': post['date'],'transcript': post['transcript'], 'source': post['source'],
    #     'summary': summary})



if __name__ == "__main__":
    main()
