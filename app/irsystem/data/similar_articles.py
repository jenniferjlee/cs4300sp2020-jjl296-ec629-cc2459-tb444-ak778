from __future__ import print_function
import numpy as np
import json
import math
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from numpy import linalg as LA

data_file_name = "final_data.json"

def load_json_file(name):
    current_directory = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_directory, name)
    with open(file_path, encoding = 'utf-8') as json_file:
        data = json.load(json_file)
    return data

data = load_json_file(data_file_name)
uniqueData = list({v['title']:v for v in data}.values())
data = uniqueData

num_articles = len(data)
# print(num_articles)
# print(str(num_articles) + ' articles loaded')
# print('Each article has the following features:')
# print(data[0].keys())
#['title', 'url', 'date', 'transcript', 'source']


# From A5

# Assign an index for each article. This index will help us access data in numpy matrices.
article_title_to_index = {article_title:index for index, article_title in enumerate([d['title'] for d in data])}
article_index_to_title = {v:k for k,v in article_title_to_index.items()}

# import operator
# sorted_d = sorted(article_title_to_index.items(), key=operator.itemgetter(1))
# print(sorted_d)

n_feats = 10000 # 5,000 in A5
article_by_vocab = np.empty([len(data), n_feats])

# It only considers words that appear in at least ten documents, but in no more than 80% of all documents.
# It computes a maximum of 10000 features, and doesn't include english stopwords.
# It should normalize all tfidf vectors to have an l2 norm of 1.

def build_vectorizer(max_features, stop_words, max_df=0.8, min_df=10, norm='l2'):
    """Returns a TfidfVectorizer object with the above preprocessing properties.
    Returns: TfidfVectorizer
    """
    return TfidfVectorizer(max_df=max_df, max_features=max_features, min_df=min_df, stop_words=stop_words)

tfidf_vec = build_vectorizer(n_feats, "english")
article_by_vocab = tfidf_vec.fit_transform([d['transcript'] for d in data]).toarray()
index_to_vocab = {i:v for i, v in enumerate(tfidf_vec.get_feature_names())}

def get_sim(art1, art2, article_by_vocab, article_title_to_index):
    """Returns a float giving the cosine similarity of 
       the two article transcripts.
    Returns: Float (Cosine similarity of the two article transcripts.)
    """
    art1vec = article_by_vocab[article_title_to_index[art1]]
    art2vec = article_by_vocab[article_title_to_index[art2]]
    num = art1vec.dot(art2vec)
    denom = np.linalg.norm(art1vec) * np.linalg.norm(art2vec)
    return num/(denom+1)

articleTitle1 = 'After 13 Years of Social Distancing, Giant Pandas Finally Mate During Peaceful COVID-19 Zoo Closures'
articleTitle2 = '16-Year-Old Has Been Using His Flying Lessons to Deliver Medical Supplies to Rural Hospitals Fighting COVID'
articleTitle3 = "Trebek to Special Jeopardy! Guest: 'I Don't Normally Do This'"

print("Similarity: pandas in covid vs flying lessons in covid")
print("======")
test1 = get_sim(articleTitle1, articleTitle2, article_by_vocab, article_title_to_index)
print(test1)

print("Similarity: pandas in covid vs jeopardy")
print("======")
test2 = get_sim(articleTitle1, articleTitle3, article_by_vocab, article_title_to_index)
print(test2)

def top_terms(movs, article_by_vocab, index_to_vocab, article_title_to_index, top_k=10):
    """Returns a list of the top k similar terms (in order) between the
        inputted article transcripts.
    Returns: List 
    """
    n = len(index_to_vocab)
    top_list = np.zeros(n)
    for index in index_to_vocab.items():
        val = 1
        for mov in movs:
            val *= article_by_vocab[article_title_to_index[mov]][index[0]]
        top_list[index[0]] = val
        
    tops = np.argsort(top_list)[::-1]
    top = list()
    for n in range(top_k):
        top.append(index_to_vocab[tops[n]])
    return top

# print("Top ten terms between: pandas in covid and flying in covid")
# print("======")
# term_test_1 = top_terms([articleTitle1, articleTitle2], article_by_vocab, index_to_vocab, article_title_to_index)
# for term in term_test_1:
#     print(term)

def build_article_sims_cos(n_arts, article_index_to_title, article_by_vocab, article_title_to_index, get_sim_method):
    """Returns an articles_sims matrix where for (i,j):
        [i,j] should be the cosine similarity between the article with index i and the article with index j
    Returns: Numpy Array 
    """

    articles_sim = np.zeros((n_arts, n_arts))
    for i in range(n_arts):
        for j in range(n_arts): 
            if i <= j:
                if i == j:
                    articles_sim[i][j] = 1
                else:
                    val = get_sim_method(article_index_to_title[i], article_index_to_title[j],
                                                            article_by_vocab, article_title_to_index)
                    
                    articles_sim[i][j] = val
                    articles_sim[j][i] = val
    return articles_sim


articles_sims_cos = build_article_sims_cos(num_articles, article_index_to_title, article_by_vocab, 
article_title_to_index, get_sim)

def get_ranked_articles(article, matrix):
    """
    Return sorted rankings (most to least similar) of articles as 
    a list of two-element tuples (title, score)
    Returns: List<Tuple>
    """
    # Get article index from article title
    art_idx = article_title_to_index[article]
    
    # Get list of similarity scores for article
    score_lst = matrix[art_idx]
    article_score_lst = [(article_index_to_title[i], s) for i,s in enumerate(score_lst)]
    
    # Do not account for article itself in ranking
    article_score_lst = article_score_lst[:art_idx] + article_score_lst[art_idx+1:]
    
    # Sort rankings by score
    article_score_lst = sorted(article_score_lst, key=lambda x: -x[1])
    
    return article_score_lst


def print_top(art, matrix, sim_type, k=10):
    """
    Print the k most and least similar movies to articleTitle1 (pandas in covid)
    """
    
    art_score_lst = get_ranked_articles(art, matrix)
    
    print("Top {} most similar articles to {} [{}]".format(k, articleTitle1, sim_type))
    print("======")
    for (art, score) in art_score_lst[:k]:
        print("%.3f %s" % (score, art))

    print()
    
    print("Top {} least similar articles to {} [{}]".format(k, articleTitle1, sim_type))
    print("======")
    for (art, score) in art_score_lst[-k:][::-1]:
        print("%.3f %s" % (score, art))


print_top(articleTitle1, articles_sims_cos, 'cosine sim')