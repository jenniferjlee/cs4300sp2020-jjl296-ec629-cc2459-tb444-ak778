import numpy as np
import json
import math
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
import re
import random

def search_tfdf_method(query, input_inverted_index, 
        input_doc_norms, input_idf_values, tokenize_method):
    n_docs = len(input_doc_norms)
    q_tokens = tokenize_method(query)
    totals = np.zeros(n_docs)
    query_norm = 0
    for t in set(q_tokens):
        query_df = q_tokens.count(t)
        if (input_inverted_index.get(t) is not None):
            for tup in input_inverted_index.get(t):
                doc_id = tup[0]
                doc_df = tup[1]
                idf = input_idf_values[t]
                totals[doc_id] += doc_df*idf*query_df*idf
                query_norm += math.pow(query_df*idf, 2)
    sim = []
    query_norm = math.sqrt(query_norm)
    for i in range(n_docs):
        val = 0
        if ((input_doc_norms[i] != 0) & (query_norm != 0)):
            val = totals[i]/(input_doc_norms[i] * query_norm)
        if(val > 0):
            sim.append((val, i))
    return sim

def search_keyword_method(query, n_docs, input_inverted_index, tokenize_method):
    q_tokens = tokenize_method(query)
    scores = np.zeros(n_docs)
    for t in set(q_tokens):
         if (input_inverted_index.get(t) is not None):
            for tup in input_inverted_index.get(t):
                doc_id = tup[0]
                scores[doc_id] += tup[1]
    sim = []
    for i in range(n_docs):
        if(scores[i] > 0):
            sim.append((scores[i], i))
    sim.sort(key = lambda x: x[0], reverse = True)
    return sim



def get_top_k(results, k, input_data):
    results.sort(key = lambda x: x[0], reverse = True)
    output = []
    for i in range(min(k, len(results))):
        doc_id = results[i][1]
        doc_info = {'title' : input_data[doc_id].get('title'), 'url': input_data[doc_id].get('url'),
                    'date':input_data[doc_id].get('date'), 'score':input_data[doc_id].get('score'),
                    'source':input_data[doc_id].get('source'), 'summary':input_data[doc_id].get('summary')}
        output.append(doc_info)
    return output

# def sort_by_recency(results):
#     results.sort(key = lambda x: x['date'], reverse = True)
#     return results

def sort_by_recency(results, k, input_data, isRecent):
    output = []
    for i in range(min(k, len(results))):
        doc_id = results[i][1]
        doc_info = {'title' : input_data[doc_id].get('title'), 'url': input_data[doc_id].get('url'),
                    'date':input_data[doc_id].get('date'), 'score':input_data[doc_id].get('score'),
                    'source':input_data[doc_id].get('source'), 'summary':input_data[doc_id].get('summary')}
        output.append(doc_info)
    output.sort(key = lambda x: x['date'], reverse = isRecent)
    return output


# def sort_by_popularity(results, input_data):
#     results.sort(key = lambda x: x['score'], reverse = True)
#     return results

# need to change this for the future because a maj of the sources don't have scores bc
# they aren't from reddit and then are placed last

def sort_by_popularity(results, k, input_data, isPopular):
    output = []
    for i in range(min(k, len(results))):
        doc_id = results[i][1]
        doc_info = {'title' : input_data[doc_id].get('title'), 'url': input_data[doc_id].get('url'),
                    'date':input_data[doc_id].get('date'), 'score':input_data[doc_id].get('score'),
                    'source':input_data[doc_id].get('source'), 'summary':input_data[doc_id].get('summary')}
        output.append(doc_info)
    output.sort(key = lambda x: (x['score'] is None, x['score']), reverse = isPopular)
    return output

def get_combined_results(output_A, output_B, weight_A, weight_B):
    i = 0
    j = 0
    combined_output = []
    if (len(output_A)==0):
        return output_B
    if (len(output_B)==0):
        return output_A
    while ((i < len(output_A)) & (j < len(output_B))):
        doc_A = output_A[i][1]
        doc_B = output_B[j][1]
        score_A = output_A[i][0]
        score_B = output_B[j][0]
        if (doc_A == doc_B):
            combined_score = weight_A*score_A + weight_B*score_B
            combined_output.append((combined_score, doc_A))
            i+=1
            j+=1
        elif (doc_A < doc_B):
            combined_output.append((weight_A*score_A, doc_A))
            i+=1
        else:
            combined_output.append((weight_B*score_B, doc_B))
            j+=1
    return combined_output


def get_random(input_data):
    output = []
    for i in random.sample(range(len(input_data)), 1):
        doc_info = {'title': input_data[i].get('title'), 'url':input_data[i].get('url'),
                'date':input_data[i].get('date'), 'score':input_data[i].get('score'),
                'source':input_data[i].get('source'), 'summary':input_data[i].get('summary')}
        output.append(doc_info)
    return output


