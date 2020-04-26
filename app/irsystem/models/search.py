import numpy as np
import json
import math
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer 
import re
import random

def search_tfdf_method(query, input_tfidf_matrix, input_inverted_index, input_doc_norms, tokenize_method):
    n_docs = len(input_tfidf_matrix)
    q_tokens = tokenize_method(query)
    totals = np.zeros(n_docs)
    for t in set(q_tokens):
        if (input_inverted_index.get(t) is not None):
            for tup in input_inverted_index.get(t):
                doc_id = tup[0]
                totals[doc_id] += input_tfidf_matrix[doc_id][t]
    sim = []
    for i in range(n_docs):
        val = 0
        if (input_doc_norms[i] != 0):
            val = totals[i]/(input_doc_norms[i])
        if(val > 0):
            sim.append((val, i))
    sim.sort(key = lambda x: x[0], reverse = True)
    return sim

def get_top_k(results, k, input_data):
    output = []
    for i in range(min(k, len(results))):
        doc_id = results[i][1]
        # ['title', 'url', 'date', 'source', 'summary']
        title = (input_data[doc_id]['title'], input_data[doc_id].get('url'),
        input_data[doc_id].get('date'), input_data[doc_id].get('source'),
        input_data[doc_id].get('summary'))
        output.append(title)
    return output

def get_random(input_data):
    doc_id = random.randint(0,len(input_data))
    return [(input_data[doc_id]['title'], input_data[doc_id].get('url'))]


